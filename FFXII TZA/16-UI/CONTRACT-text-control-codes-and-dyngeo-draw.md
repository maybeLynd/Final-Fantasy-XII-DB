---
contract: interpret the control codes embedded in game text - one interpreter for both measuring and drawing, with the cursor advanced by the parser's own return - and draw the result through the dynamic-geometry instance family, whose shadow and screen-space variants are a prefix plus a tail call into one shared body
category: 16-UI
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 16-UI/Text-And-Number-Rendering/the-text-control-code-language.md, 16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md
entries: ["002AC5F0", "003FFAB0", "003FFD70", "002142A0", "00214210", "00214540", "002143E0", "00214890", "002148B0"]
registry_slots: []
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every body and every table named in sections 2, 3, 4 and 7 was read from the authority
    image on 2026-09-21 (OPUS) - the interpreter's prologue and dispatch, all eleven parsers'
    returns, the three jump tables decoded byte for byte, the four variant prefixes, both slot-11
    bodies, the identity constant pool and the four 12-slot vtables read out of `.rdata`. The
    per-arm semantics of the 34 escape arms are FABLE's and are carried with attribution rather than
    re-derived; this contract states the dispatch, the extents and the invariants across them.
last_reviewed: 2026-09-21
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_state: opus-falsification-pass-1-2026-09-29-exe-73461d08
  crossref_clean: false
  reopened_count: 0
---

# Contract — the text control-code language and the DynGeo draw

> **Why this exists, and the honest thing it has to say about its own scope.** S-37 carried **no
> contract at all** — its L2 verdict read `NOT MET` with the contract cell as the binding gap, and it
> was the last `supporting`-tier system in that position. The registry credits it with two halves:
> [the control-code language](Text-And-Number-Rendering/the-text-control-code-language.md) and
> [the DynGeo instance family](Dynamic-Geometry-Instances/dyngeo-instance-family.md).
>
> **The two halves are joined by construction and ownership; the draw call itself is not observed.**
> (Restated 2026-09-25 from FABLE's `AS-3` answer, every site re-read by OPUS - §6.) The interpreter
> calls `0017F850`, the `display : draw Font` wrapper, which calls the text flush `001E8580`; **the
> flush is the only code in the image that constructs DynGeo instances** - four `new` sites, three
> classes. What stays unseen is the other end: the four slot-10 draw bodies have **no direct caller**
> and each is reachable only through the single pointer to it in `.rdata`, so *that* the flush's
> objects are drawn through slot 10 is still inference until a dispatch is observed. The first
> version of this paragraph said the halves were "not joined by any route this database can see";
> that was true of the direct-call graph it measured, and the construction route was not measured.
>
> **Provenance.** The dispatch, the extents, the tables, the parser returns, the variant prefixes and
> the vtables are **NATIVE/STATIC**, read here on 2026-09-21. The per-arm semantics of the escape
> catalogue and the authored-text census behind `UQ-177` are FABLE's, carried with attribution.
> Section 13 is **empty**: nothing here is observed live.

## 1. Purpose

Game text is not a plain string: a line of dialogue carries codes inside it that change colour,
insert a party member's name or an icon, indent, justify, wait for a button, or start a new page.
One function interprets all of them, and the same function runs when a line is being **measured** for
a text box as when it is being **painted** — so a code that changes the layout is accounted for
before anything is drawn. What finally puts pixels on the screen is a small family of
dynamic-geometry objects, whose drop-shadow and screen-space variants are the same draw invoked with
different state.

## 2. Interface

| | |
|---|---|
| entry point(s) | `002AC5F0` (7,489 B) the interpreter · `003FFAB0`–`003FFF10`, eleven parsers · `002142A0` (306 B) the shared DynGeo draw and its three variants `00214210` (139 B), `00214540` (82 B), `002143E0` (352 B) · `00214890` / `002148B0` / `00214860`, slot 11 |
| calling convention | Microsoft x64. **`002AC5F0(rcx = text context, rdx = char **cursor, r8 = float *out, r9 = int *out2)`** — read off the prologue at `002AC625`–`002AC63F`. The cursor is passed **by reference** because the function advances it past whatever it consumes. `r9`'s target is zeroed on entry at `002AC628`. |
| parameters | `rdx` is a pointer to the cursor, never the cursor. `r8` receives measured floats; `r9` receives a count. |
| return type | `int`, and it is a **loop condition**, not a result. |
| return semantics | **1 = "I consumed a code, call me again"** (`002ACFC2 mov eax, 1`). **0 = stop** — either an ordinary character (`002AC6CA xor eax, eax`, taken for any byte `>= 0x10` and for `0x0B`–`0x0D`) or the end of the run (`002AE32A`). ~~All seven callers use the identical `call / test eax, eax / je` shape.~~ **Five callers loop on it with `test eax, eax / je`; two (`002B1FB0`, `002B5730`) call once, discard it and read the cursor delta** *(CORRECTED 2026-09-29, falsification pass 1; see I-1)*. |
| callbacks / indirect dispatch | Two indirect jumps, both table-driven and both decoded in §3. The DynGeo half is *entirely* indirect: its bodies are reached only through vtable slots. |

## 3. Types

**The dispatch tables, decoded from the image and verified to tile exactly.**

| table | at | extent | contents |
|---|---|---|---|
| token arms | `002AE334` | 15 × dword | image-relative targets for bytes `0x01`–`0x0F` |
| escape arms | `002AE370` | 35 × dword | image-relative targets, indexed by the case table |
| case index | `002AE3FC` | `0x51` bytes | one byte per selector `0x20`–`0x70`, values `0..34` |

`002AE334 + 15*4 = 002AE370`; `+ 35*4 = 002AE3FC`; `+ 0x51 = 002AE44D`, and the next function begins
at `002AE450`. **The three lengths are fixed by three separate `cmp` bounds inside the body
(`002AC694 cmp eax, 0xe`, `002AD026 cmp eax, 0x50`) and they tile end to end with a two-byte gap
after the body's last instruction at `002AE32C` and a three-byte gap before the next function.** All
15 and all 35 targets land inside `002AC5F0`'s own extent. That is the check that the tables were
read correctly, and it reproduces.

```
text context (rcx)         reached by the interpreter; fields cited by the pages, not carved here
  +0x34, +0x38, +0x3C  f32   scale terms every width is multiplied by
  +0x40  u8    fixed-advance switch      +0x44  u32  flag word, bit 11 widens token 0x04
  +0x4C  f32   letter-spacing term       +0x70  ptr  argument array, 16-byte entries
  +0x78  ptr   the context's actor       +0x88  u16  page-wait tick count
  +0x94  f32   the width justification subtracts from
  +0x99  u8    margin       +0x9A  u8  justification selector      +0xAA  s8  indent
  +0xB0  u32   flag word; bit 19 waiting, bit 21 unread, bit 25 guards `$`, bit 26 write-only

painter singleton          [0209CC40], reached through a GLOBAL, not passed
  +0x10C8  ptr  a terminator word - see I-8
  +0x10E8  f32  line gap        +0x10EC/+0x10F0/+0x10F4/+0x10F8  f32  column marks
  +0x10FC  reset by token 0x03  +0x1102  u8  line-start flag   +0x1104  u8  justification

advance pair               [0209CC60], [0209CC68] - zeroed on EVERY entry (I-7)
```

**The DynGeo variant vtables, read out of `.rdata`.** Four contiguous 12-slot tables at a **`0x68`
stride** — an RTTI-locator qword followed by twelve slots:

| vtable base | class | slot 2 | slot 6 | slot 10 | slot 11 |
|---|---|---|---|---|---|
| `00906DE8` | `…SpecialInstance` | `00213AD0` | `00213D10` | `002142A0` | `00214890` |
| `00906E50` | `…SpecialShadowInstance` | `00213B00` | `00213D10` | `00214540` | `002148B0` |
| `00906EB8` | `…SpecialFinalInstance` | `00213AA0` | `00213B40` | `00214210` | `00214860` |
| `00906F20` | `…SpecialShadowFinalInstance` | `00213B00` | `00213D10` | `002143E0` | `00214860` |

**And the object behind them is three parallel ten-entry arrays, carved here from the shared draw.**
`002142A0` sets `r12d = 0xA` (`002142B4`), `r14 = this + 0x08` (`002142C9`) and `r15 = this + 0xA8`
(`002142BA`), and advances `r14 += 8` / `r15 += 4` once per iteration (`002143A0`–`002143A8`):

```
DynGeoFontTextSpecialInstance          0x160 (0x170 Final, 0x168 Shadow and ShadowFinal)
  +0x00        void*   vftable
  +0x08..0x57  void*[10]  layerSource   ten qwords; entry i is tested non-null and handed to
                                        the target's slot 8 (`[rax+0x40]`, 0021432A)
  +0x58..0xA7  void*[10]  layerVertices ten qwords; entry i is the vertex array base
                                        (`r13 = [r14+0x50]`, 00214332)
  +0xA8..0xCF  uint32[10] layerCount    ten dwords; entry i is that layer's vertex count
                                        (`esi = [r15]`, 0021432D)
  +0xD0..      unobserved
```

**The vertex stride is 48 bytes and the batch ceiling is 480 vertices**, both read rather than
assumed: `0021433A mov r12d, 0x1e0` clamps the per-call count (`0021434B cmovg`), and the source
offset is `lea r8, [rcx + rcx*2]` then `shl r8, 4` — count × 3 × 16 (`00214356`–`0021435D`). A layer
of more than 480 vertices is drawn in several passes, the loop subtracting at `00214394`.

**Those four columns are the only ones that differ**; the other eight slots hold identical pointers
in all four tables, which is the slot-by-slot diff the page reports, confirmed here from the bytes.
Slot 0 of every one of them is **`0016D6A0`** — the three-byte `ret 0` that `/OPT:ICF` folded every
empty function in this image onto. `DynGeoFontTextInstance`'s vtable at `00906DC8` is **3 slots**
(`0016D6A0`, `00213140`, `00213110`), confirming the three-shape split.

## 4. Preconditions · postconditions · invariants

**I-1 — THE RETURN VALUE IS A LOOP CONDITION ~~AND EVERY CALLER TREATS IT AS ONE~~ FOR FIVE CALLERS; TWO USE ONLY THE
CURSOR.** Seven callers (`002A8C50`, `002A9F00`, `002AAE40`, `002AF340`, `002B1FB0`, `002B2150`, `002B5730`).
**CORRECTED 2026-09-29 (falsification pass 1): they are not one shape.**
- **Five loop on the return:** `002A9726`, `002AA6A8`, `002AB5B0`, `002AF783` and `002B2393` each follow the call with
  `test eax, eax` / `je`.
- **Two are single-shot length probes:** `002B1FB0` at `002B207E` and `002B5730` at `002B5823` call the interpreter
  once, never test `eax`, and read the advanced cursor (`[rsp+0x28] − start`) as the length of the code at the
  cursor.

So the protocol has two halves:
- a reimplementation that returns a token or a length breaks the five loopers;
- one that advances the cursor differently breaks the two probes, even if its return is right.

**I-2 — THE CURSOR IS ADVANCED BY THE PARSER'S RETURN, SO THE INTERPRETER ENCODES NO CODE LENGTHS.**
Every arm ends `lea rdx, [rsp+0x40]` / `call <parser>` / `add qword ptr [rdi], rax`
(`002AE308`–`002AE314` is the worked copy). **Measured across all eleven parsers**, that return is:

| parser | returns |
|---|---|
| `003FFAB0`, `003FFB90`, `003FFC60`, `003FFDA0`, `003FFEE0` | the constant **3**, on every path |
| `003FFCE0`, `003FFF10` | the constant **4** |
| `003FFD70` | **`word[payload] + 3`** — a length carried in the code itself (`003FFD91`–`003FFD95`) |
| `003FFB00`, `003FFBC0` | a computed value in `ebx` |
| `003FFDF0` | a scanned length, `ecx - r11d` (`003FFED3`) |

So the language really is variable-length, and the variation is genuine rather than nominal: two
fixed widths, one self-describing width and two scanned ones.

**I-3 — THERE ARE 34 DISTINCT ESCAPE ARMS, NOT 35.** The 35-entry target table contains `002ACFC2`
**twice**, at indices 13 and 34, which the case table maps from the selectors `0` and `_`. The case
table's 0x51 bytes carry 35 distinct values covering `0..34` with no gap. *(This confirms the page's
own falsification-pass correction from its 2026-09-13 audit; it is re-derived here rather than
carried.)* *The do-nothing arm does not swallow its selector: the selector byte is drawn by the next call (I-6, corrected 2026-09-25).*

**I-4 — MEASUREMENT AND DRAWING ARE THE SAME CODE PATH, AND THE RECURSION IS THE MECHANISM.**
`002B2150` and `002A9F00` are both callers **and** callees of `002AC5F0` — the interpreter calls
`002B2150` seven times and `002A9F00` four. That mutual recursion is how a code that splices text in
(a name, a number, an argument) gets that text measured and emitted by the machinery currently
interpreting it, and it is why one function is 7,489 bytes. **A reimplementation that separates
measuring from drawing must reproduce the recursion or it will mis-lay-out every inserted string.**

**I-5 — THE PAINTER IS SHARED THROUGH A GLOBAL, NOT THE SIGNATURE.** `002AC650` loads
`[0209CC40]`, and the interpreter, the emitter and the line layout all reach the same object that
way. **The function's four parameters are not its full input**, which is the single most misleading
thing about its signature.

**I-6 — AN UNRECOGNISED SELECTOR IS NOT AN ERROR — AND IT IS PRINTED.** Outside `0x20`–`0x70` ~~the escape is consumed and
the run continues~~ **only the `0x0F` byte is consumed** (`002AD029 ja 0x2acfc2`). Inside the range, every one of the
0x51 selectors has a case index, and two of them land on the do-nothing arm. **There is no error path and no diagnostic.**
*Corrected 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 313, which executed it; `002AD01A`–`002AD029` re-read.*
- `002AD01A inc rcx` / `002AD01D mov [rdi], rcx` leave the cursor **on the selector byte**, and the exit `002ACFC2`
  returns 1 without advancing further.
- The next interpreter call therefore reads the selector as an ordinary character and the caller draws it.
- **So an escape with an unknown selector prints its selector byte.** So does an escape with either do-nothing
  selector, `0` or `_` (I-3), which reach the same exit with the cursor in the same place.
- Also measured: the end of run (`002AE31C`) and token `0x03` call a one-store setter that writes `+0x28` of the
  `[01F811F8]` singleton.

**I-7 — THE ADVANCE PAIR IS PER-CALL, NOT PER-LINE.** `002AC62E` and `002AC638` store zero into
`[0209CC60]` and `[0209CC68]` **in the prologue, before the first byte is examined**. The line break
clears them again, but the entry clear means a caller cannot accumulate an advance across two calls
of the interpreter.

**I-8 — THERE IS A SECOND STOP CONDITION, AND IT IS NOT NUL.** `002AC650`–`002AC669`: if
`[0209CC40 + 0x10C8]` is non-null and the `word` at that address equals the `word` under the cursor,
the function jumps to `002AE31C` — **the same exit NUL takes**. So a terminator word held on the
painter stops the run exactly as end-of-string does. Neither primary page records this; a
reimplementation that stops only at NUL will run past the intended end of every line that uses it.

**I-9 — THE DYNGEO VARIANT MATRIX IS PREFIX-PLUS-TAIL-CALL, WITH ONE EXCEPTION.**
`00214210` (`Final`) ends `jmp 0x2142a0` at `00214296`; `00214540` (`Shadow`) ends `jmp 0x2142a0` at
`0021458D`. Both do their own setup and then **literally jump into the base implementation** — they
are not copies. `002143E0` (`ShadowFinal`) is the exception: it performs both prefixes inline and
does **not** tail-call, drawing layer 0 by itself. **The base `002142A0` is therefore a single choke
point for three of the four variants and not for the fourth**, which is the distinction a detour has
to respect.
*Executed 2026-09-26 (OPUS, `s37-opus-replay-text-interpreter/i5_i9_i13.py`, NATIVE-REPLAY).* `Final`'s and
`Shadow`'s draws equal a direct base call on the same ten layers. **`ShadowFinal`'s layer-0 draw is not the base's
walk inlined:** it draws with primitive `3` (`00214520 mov edx, 3`), where the base uses `2`. It maps and copies the
whole count at once, with no 480-vertex batches, and it has no null-source skip (layer 0 with a null source still
binds 0, maps 0 and draws 0). Its slot-15 call passes `(1, 6, 7, [6, 7, 10])`, where `Shadow` passes
`[6, 7, 9]` (`BC-1`'s third constant).

**I-10 — THE `Final` PREFIX IS FOUR ROWS SELECTED OUT OF A SIGNED POOL, WITH ROW 0'S SCALE REPLACED BY
AN ASPECT RATIO.** The four rows loaded are `008C5F80` `(1,0,0,0)`, `008C5F90` `(0,1,0,0)`, `008C5FB0` `(0,0,1,0)`
and `008C5FD0` `(0,0,0,1)` — **verified by decoding the floats**. The spacing is uneven because the
skipped slots hold the **negated twins**: `008C5FA0` is `(0,-1,0,0)` and `008C5FC0` is `(0,0,-1,0)`.
It is four rows selected from an axis-vector pool, not a contiguous matrix literal, and the whole
prefix is gated on the predicate `00182F50` (`00214227 je`).
~~A literal identity matrix~~ — *corrected 2026-09-26 (OPUS), on its execution
(`s37-opus-replay-text-interpreter/i5_i9_i13.py`).* **The matrix handed to the target's slot 6 (`+0x30`,
`00214283`) is not the identity.** After the pool load, `0021426C movss [rsp+0x20], xmm0` replaces row 0's first
element with the result of `00229DE0` → `00183280`, and `00214272` / `0021427B` rezero the rest of the row. That
result is `height × 1.7777778 / width`: the constant is `008C5B38` (16/9), the width comes from `00182EB0`
(`[display+0x10]`, default 0x780 without a display object), and the height from `00182E80` (`[display+0x14]`,
default 0x438). The display object is `[01F82D18]`, and the predicate reads it as well (`+0x00 == 1`).
- **Executed:** on 1920×1080 the matrix is the identity; **on 1280×1024 row 0 is `(1.4222223, 0, 0, 0)`**; with the
  predicate false, slot 6 is not called at all.
- So the prefix is **a horizontal aspect correction toward 16:9**, and it equals the identity only on a 16:9
  display. A reimplementation that hardcodes the identity draws correctly only at 16:9.

**I-11 — SLOT 11 SHIFTS ITS ARGUMENTS AND THE VARIANTS DIFFER ONLY IN THE THIRD.** Both
`00214890` and `002148B0` tail-jump into slot 35 (`+0x118`) of the target object, both move the
incoming `r8b` into `edx`, and they differ in what they pass as the new third argument: a hardcoded
`0` (`0021489A xor r8d, r8d`) against the boolean `(r8b != 0)` (`002148B5`–`002148C6`). `Final` and
`ShadowFinal` share a third implementation, `00214860`.
*Executed 2026-09-26 (OPUS, `i5_i9_i13.py`):* for `r8b` ∈ {0, 1, 0x80, 0xFF}, all three call slot 35 once with
`rcx` = the target and `edx` = `r8b`. **`00214860`'s third argument is `2 × (r8b != 0)`**
(`0021486B`–`00214878`, `neg`/`sbb`/`and 2`), and it writes only `r8w`.

**I-12 — THE SHARED DRAW IS A TEN-LAYER WALK AND A LAYER WITH NO SOURCE IS SKIPPED WHOLE.** The
outer loop runs exactly ten times regardless of content; an entry whose `layerSource` is null jumps
straight to the advance at `002143A0` (`002142D6 je`), and so does a layer whose count is zero
(`00214338 je`). **Nothing accumulates across layers** — `ebp` and `esi` are re-initialised per
layer — so a reimplementation may draw the ten in any order without changing the result, which is
exactly the opposite of the render command list's ordering discipline.

**I-13 — THE DELETING DESTRUCTORS DO NOT IDENTIFY THEIR CLASS; THEIR SIZE DOES.** All three of
`00213AD0`, `00213AA0` and `00213B00` stamp **the same vtable `00906DE8`** — the plain
`SpecialInstance` table — before the `dl & 1` free (`00213AE0`, `00213AB0`, `00213B10`). They differ
only in the size immediate passed to `free`: `0x160`, `0x170` and `0x168`. So the object size is the
only thing in those bodies that tells the four classes apart, and a reader identifying a class by
the vtable a destructor writes will get `SpecialInstance` for all of them.

**Postcondition.** After the interpreter returns 0, the cursor points at the first byte it did not
consume and `*out2` holds the unit count for that run. After a DynGeo slot-10 call, the target's
draw state has been mutated by the variant's prefix and the shared body has run — except on the
`ShadowFinal` path, where only layer 0 is drawn.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `[0209CC40]` the painter and `+0x10C8`; the three dispatch tables; the text context's scale, flag and justification fields; the identity pool `008C5F80`–`008C5FD0` | `002AC650`, `002AC657`, `002AC6A2`, `002AD02D`, `002AD035`, `00214229`–`0021423E` |
| written | `[0209CC60]`, `[0209CC68]` (zeroed on entry, then written per unit); `*out2` (zeroed on entry); painter `+0x10FC`, `+0x1100`–`+0x1104`; the context fields the arms set | `002AC62E`, `002AC638`, `002AC628` |
| allocated | **nothing in the interpreter.** Its 0x1D8-byte frame is stack, with a stack cookie from `01F44830` (`002AC60A`–`002AC614`). The DynGeo instances are allocated by the text flush `001E8580` (heap singleton `[01F7F4C0]`, `call 001A1470`, then the constructor): `0x168` Shadow at `001E86BB` and `001E88C4`, `0x168` ShadowFinal at `001E8A7D`, `0x170` Final at `001E8F84`. **Those sizes agree 4 of 4 with the slot-2 sized deleting destructors** (`0x170` Final, `0x168` Shadow and ShadowFinal) - two instruments reading opposite ends of the object's life. The plain `Special` (`0x160` by its destructor) **is never constructed**: no instruction in the image stamps `00906DE8` except the three destructors' reset-to-base | `002AC603`, `00213AD0`/`00213AA0`/`00213B00`, `001E86BB`/`001E88C4`/`001E8A7D`/`001E8F84` |
| deallocated | nothing here | — |

## 6. Relationships

```
the text pipeline - seven callers, one interpreter
  002A8C50 (markup parser)  at 002A9726
  002A9F00 (glyph emitter)  at 002AA6A8     <- also a CALLEE, x4
  002AAE40 (draw)           at 002AB5B0
  002AF340                  at 002AF783
  002B1FB0                  at 002B207E
  002B2150 (measure)        at 002B2393     <- also a CALLEE, x7
  002B5730                  at 002B5823
        |
   002AC5F0  -- 15-way token table --> 15 arms
             -- 0x0F -> case table -> 35-entry target table --> 34 distinct arms
             -- every arm --> one of eleven parsers (003FFAB0..003FFF10, 32 sites)

the DynGeo family - CONSTRUCTED by the text flush, DRAWN only through the vtable
  002AC5F0 --call 002AC7EC / 002AD7AE--> 0017F850 'display : draw Font' (38 B; 12 call
           sites in 8 functions, the interpreter's two among them)
           --call 0017F868--> 001E8580 the text flush (its ONLY caller)
                 --new 0x168 --> 00213A00 Shadow       at 001E86BB, 001E88C4
                 --new 0x168 --> 00213960 ShadowFinal  at 001E8A7D
                 --new 0x170 --> 002138C0 Final        at 001E8F84
  (no constructor anywhere stamps 00906DE8: the plain Special is a base and a
   destructor reset target only)
  00214210 (Final)  --tail--> 002142A0        the only two edges edges.tsv carries
  00214540 (Shadow) --tail--> 002142A0
  002143E0 (ShadowFinal)      inline, no tail call
  each body has EXACTLY ONE pointer to it in the whole image, in .rdata,
  inside its own class's 12-slot vtable
```

**Construction and ownership are joined; the draw dispatch is not observed.** The route above is
NATIVE/STATIC and complete for construction: an image-wide sweep of references into the four-vtable
window `00906DE8`-`00906F88` returns exactly six sites, all in `00213xxx` - three constructors
(`002138F9`, `00213999`, `00213A39`) and three destructor resets to `00906DE8` - and the only call
sites of those three constructors are the four inside `001E8580`. (FABLE's `AS-3` answer, re-measured
by OPUS 2026-09-25 with the same result. One correction to that answer: the interpreter is **not**
"the only thing that reaches" the flush - `0017F850` has 12 call sites in 8 functions, the
interpreter's two among them; the flush's only caller is `0017F850`.) **What the direct-call graph
still cannot show is the draw**: `edges.tsv` carries direct calls, the slot-10 bodies are reached only
through the vtable, and nothing here observes that dispatch being taken. `PROPOSED-OPUS-S37-1` is
rescoped to that half; see §14.

## 7. State transitions

The interpreter is a cursor machine with one state — the cursor — and three exits.

| previous | resulting | condition, and the exact test |
|---|---|---|
| cursor at byte `b` | consumed, return 1 | `1 <= b <= 0x0F` and the arm reaches `002ACFC2` |
| cursor at byte `b` | not consumed, return 0 | `b >= 0x10`, or `b` in `0x0B`–`0x0D` — `002AC694 cmp eax, 0xe` / `ja`, plus table indices 10–12 |
| cursor at `0x03` | consumed **and** return 0 | the only arm that does work and still stops (`002AC6AE`) |
| cursor at `0x00` | stop | `002AC648 test dl, dl` / `je` |
| cursor at the terminator word | stop | I-8, `002AC666 cmp ax, word ptr [rcx]` / `je` |
| cursor at `0x0F` + selector | consumed, return 1 | selector in `0x20`–`0x70`; ~~outside, consumed anyway (`002AD029`)~~ outside, **only the `0x0F` is consumed**: the cursor stops on the selector, which the next call prints (I-6; *corrected 2026-09-29, pass 1, propagating FABLE's 2026-09-25 correction*) |

## 8. Script · resource · event interactions

**The codes are authored data, and their population over the shipped archive is measured**
([the language page](Text-And-Number-Rendering/the-text-control-code-language.md) §6, `UQ-177`,
FABLE 2026-09-18): a census of every `.bin`/`.dat` under the nine language trees, kept to the text
formats by magic — 407 `st2e` banks, 101 `hdat` handbooks, 53 bank-format files, with 24,702 `)`
escapes as the control. Its three load-bearing results, carried: **selector `9` is authored by no
shipped text**, so the state it sets can never fire; **`#` is authored 16 times in `st2e` plus 27 in
`texpack_ys.bin`** and is the page wait; and **`+` is authored 30 times** and leaves a write-only
nibble behind.

**The dispatch is data too, in the same sense**: the three tables of §3 are `.text` payload after the
body, not code, and editing a target moves an arm without touching an instruction.

**No script verb reaches either half.** The interpreter's seven callers are all inside the text
pipeline, and the DynGeo bodies have no direct caller at all.

## 9. Determinism

**RNG — none.** No body on either half draws from any generator.

**Timing / update ordering.** The interpreter is re-entrant by design (I-4) and is called in a loop
by each of its seven callers. Nothing here is frame-paced; the page wait (`#`) is a **tick** count
consumed by the stepper `002ABF70`, not a wall-clock delay.

**Threading.** No lock, no atomic, no barrier appears in the interpreter, and its shared state is a
global painter (I-5) and a global advance pair (I-7). **That is safe only because one thread walks
text**, which this contract does not establish and does not assume.

## 10. Failure paths and edge conditions

1. **Selector outside `0x20`–`0x70`** → ~~consumed and skipped~~ the `0x0F` is consumed and the selector is **printed**
   by the next call, no diagnostic (I-6; *corrected 2026-09-29, pass 1: this item still carried the reading I-6 had
   already withdrawn*).
2. **Selector inside the range with no behaviour** → indices 13 and 34, selectors `0` and `_`, land
   on the shared do-nothing arm `002ACFC2` and still return 1 (I-3).
3. **Bytes `0x0B`–`0x0D`** → routed to the ordinary-character arm, so they are *not* codes even
   though they are below `0x10`.
4. **Token `0x03`** → the only arm that acts and then returns 0 (§7).
5. **The terminator word** → stops the run indistinguishably from NUL (I-8).
6. **A parser that scans** (`003FFDF0`) or reads its own length (`003FFD70`) → the cursor advance is
   attacker-controlled in the sense that a malformed authored code can advance it arbitrarily; no
   bound check exists at the call site, which is `add qword ptr [rdi], rax` and nothing else.
7. **The `Final` predicate `00182F50` returns 0** → the whole identity-matrix prefix is skipped and
   the body still runs (`00214227`).
8. **`ShadowFinal`** → no tail call, so a detour on `002142A0` does **not** see it (I-9).

## 11. Observable behaviour

- **Colour, size, indent, justification, page waits and inline glyphs** are all directly visible in
  any line of game text; the escape catalogue in the language page §2.6 names which selector does
  which.
- **The drop shadow is a separate draw with its own object**, so it appears and disappears with the
  class instantiated rather than with a shader uniform.
- **I-8 is externally observable and is the differential test this contract most wants run**: set the
  painter's `+0x10C8` terminator and confirm that a line stops there exactly as at NUL.
- **I-7 is observable from a hook**: read `[0209CC68]` immediately before and after a call and
  confirm the entry clear.
- `#`'s authored page waits are visible as the button prompt in dialogue; `9`'s absence from the
  shipped text is visible as *nothing*, which is the point.

## 12. Reproduction formula

```
interpret(ctx, char **cursor, float *out, int *out2):     # 002AC5F0
    *out2 = 0                                             # 002AC628
    [0209CC60] = [0209CC68] = 0                           # 002AC62E, 002AC638  (I-7)
    c = *cursor
    if *c == 0: return 0                                  # 002AC648
    term = painter[0x10C8]                                # 002AC657
    if term and *(u16*)term == *(u16*)c: return 0         # 002AC666           (I-8)
    b = *c
    if b - 1 > 0x0E: return 0                             # 002AC694  ordinary character
    goto tokenTable[b - 1]                                # 002AE334 + (b-1)*4, + image base

  arm 0x0F (002AD01A):                                    # the escape prefix
    c += 1 ; *cursor = c
    s = *c
    if s - 0x20 > 0x50: return 1                          # 002AD029  consume and continue
    idx = caseTable[s - 0x20]                             # 002AE3FC
    goto escapeTable[idx]                                 # 002AE370 + idx*4, + image base

  every arm ends:                                         # 002AE308-002AE317
    n = parser(c, &payload)                               # one of eleven; see I-2
    *cursor += n
    return 1

caller:                                                   # five of seven (I-1, corrected); the other two call once
                                                          # and read cursor - start as the code's length
    while (interpret(ctx, &cursor, &f, &n)) { spend n ; advance the pen by [0209CC68] }

DynGeoFontTextSpecialFinalInstance::slot10(this, target): # 00214210
    if (!00182F50()) goto tail                            # 00214227
    m = identity from 008C5F80 / 008C5F90 / 008C5FB0 / 008C5FD0
    00229DE0(m) ; target->vtbl[6](...)                    # 0021425C, 00214283
  tail:
    jmp DynGeoFontTextSpecialInstance::slot10             # 00214296  (I-9)

DynGeoFontTextSpecialShadowInstance::slot10(this,target): # 00214540
    target->vtbl[15](target, 1, 6, 7, [sp]=6, [sp+8]=7, [sp+0x10]=9)
    jmp DynGeoFontTextSpecialInstance::slot10             # 0021458D

slot11(this, target, flag):                               # 00214890 / 002148B0
    arg2 = flag
    arg3 = 0                (Special)                     # 0021489A
    arg3 = (flag != 0)      (Shadow)                      # 002148C3
    jmp target->vtbl[35]                                  # +0x118
```

## 13. Runtime validation

**Empty. Nothing in this contract has been observed on a running game.** Every claim is static —
the shipping image, plus the authored-text census carried from the language page, which is a
file-corpus reading and not an execution.

| claim | how it was observed live | date | result |
|---|---|---|---|
| — | — | — | — |

**Native replay: not live, and kept separate from the table above.** The following ran as shipped code under unicorn
(NATIVE-REPLAY, `live_game` false, no application stub), in `_index/candidates/s37-opus-replay-text-interpreter/`:
- **`check.py` (block 313):** I-1, I-2, I-3, I-6, I-7, I-8 (`B_end_of_run`) and I-12 (`F_dyngeo_draw_layout`).
- **`i5_i9_i13.py` (2026-09-26):** I-5 (interpreter half), I-9, I-10 (corrected above), I-11 and I-13.
- **`i4.py` (2026-09-26): I-4.** Tokens `02`, `05` and `0A` hand `002B2150` the text after the token (cursor + 1), and
  `002B2150` calls the interpreter on its control bytes. `02 05 0A 09 00` nests interpreter → `002B2150` → … to depth
  four, and every level returns. A `0x02` in the splice ends it.
- **Not executed:** `002A9F00`'s re-entry, which reaches the glyph measure `002AC2F0` and its font object before any
  control byte.

## 14. Unresolved

The first three are new with this contract and are **PROPOSED, not yet registered**: `OPEN-QUESTIONS.md` carried a peer's uncommitted section when this contract was published, so publishing that file would have committed their work. The three rows are parked in `_index/_inbox/OPUS.md` under `## OPEN-QUESTIONS` and take real ids at the next publication claim, per the inbox README's proposal rule. Items 4 and 5 are existing register ids.

1. **Is the slot-10 draw of the flush's DynGeo objects actually dispatched, and for which class?**
   *Rescoped 2026-09-25:* construction and ownership are closed statically (§6 - the text flush
   `001E8580` is the sole constructor); what remains is the live half - whether slot 10 is taken at
   run time, and which of Shadow / ShadowFinal / Final draws a given line of text. *Resolved by:* a
   runtime capture of the slot-10 dispatch, or an instrument that follows vtable dispatch. Routed to
   ASTRA. (`PROPOSED-OPUS-S37-1`)
2. ~~**What is the painter's `+0x10C8` terminator word?**~~ **ANSWERED 2026-09-25 (OPUS).** The painter is
   **not a heap singleton**: `002B3550` zeroes a **static 0x1108-byte object at `0209D490`** (`lea rbx`, memset
   through `008620A0`) and publishes it in `[0209CC40]` (`002B356A`, the cell's only writer) - `TextPainter` in the
   type store. Every field access goes through that pointer, which is loaded in 26 functions and never passed (GJ-3),
   so a census of those 26 is complete: **`+0x10C8` is NULL at creation and is set, then RESTORED, around a
   draw by seven functions** - to the constant control code `0F 23` (`&0x230F` at `00916548`) by `002ABB20`, to
   `0F 2F` (`00916544`) by `002B3E90`, to a stack-built word by `002B2970`/`002B41F0`/`002B43C0`, to the second
   argument by `002B24B0`, and explicitly to NULL by `002AF960`. So a run can be drawn **up to a chosen escape
   code**; I-8 is the mechanism. (`PROPOSED-OPUS-S37-2` - answered in the parked row.)
3. **The cursor advance is unbounded at the call site.** Two parsers return a length the payload
   controls, and `add qword ptr [rdi], rax` is the whole of the bounds checking. *Resolved by:*
   deciding whether any caller re-validates the cursor against the string end — none of the seven
   was read for that here. (`PROPOSED-OPUS-S37-3`)
4. **`BC-1`** — what `6`, `7`, `9` select in the `Shadow` prefix. PARTIAL in the register since
   2026-09-15; the last constant is bounded and not named.
5. **Which glyph `002AEB20` draws for each of the 42 inline-glyph letters**, and `+`'s state nibble —
   both owned by the language page's `UQ-177` residue.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The signature and the two out-parameters | prologue `002AC625`–`002AC63F`, with `*r9 = 0` at `002AC628` | 1 | PROVEN |
| I-1 — the return is a loop condition | `002ACFC2`, `002AC6CA`, `002AE32A`, and the seven call sites tabulated on the language page | 1 | PROVEN |
| I-2 — the advance is the parser's return, and what each returns | the arm tail `002AE308`–`002AE317`; all eleven parsers read — `003FFAE0`/`003FFAF0` (3), `003FFD60`/`003FFF39` (4), `003FFD91`–`003FFD95` (payload+3), `003FFED3` (scanned) | 1 | PROVEN |
| I-3 — three tables, tiling, 34 distinct arms | the tables decoded from the image: 15 and 35 dwords, 0x51 case bytes, `002ACFC2` at indices 13 and 34, all targets inside the body, `002AE44D` immediately before `002AE450` | 1 | PROVEN |
| I-4 — mutual recursion with measure and emit | the caller/callee census on the language page, re-checked against `edges.tsv` | 1 | PROVEN |
| I-5 — the painter is global | `002AC650` `mov r8, qword ptr [rip -> 0209CC40]` | 1 | PROVEN |
| I-7 — the entry clear | `002AC62E` and `002AC638`, with `eax` zeroed at `002AC61B` | 1 | PROVEN |
| I-8 — the terminator stop | `002AC650`–`002AC669`, branching to the same `002AE31C` the NUL test reaches | 1 | PROVEN |
| I-9 — prefix plus tail call, and the exception | `00214296` and `0021458D` are `jmp 0x2142a0`; `002143E0` has no such tail | 1 | PROVEN |
| I-10 — the identity rows and the signed pool | the sixteen floats at `008C5F80`–`008C5FE0` decoded; the four loads at `00214229`–`0021423E` | 1 | PROVEN |
| I-11 — slot 11 shifts and differs in one argument | complete bodies `00214890` (24 B) and `002148B0` (33 B) | 1 | PROVEN |
| The four 12-slot vtables and the four differing columns | the `.rdata` region `00906DC0`–`00906F80` dumped and resolved; stride `0x68`; slot 0 is `0016D6A0` in all four | 1 | PROVEN |
| Each DynGeo body has exactly one pointer in the image | an exhaustive 8-byte search of every section for each body's address | 1 | PROVEN |
| I-12 — three parallel ten-entry arrays, 48-byte vertices, 480-vertex batches | complete body of `002142A0` (306 B): `002142B4`, `002142BA`, `002142C9`, `0021432D`, `00214332`, `0021433A`, `00214356`, `0021435D`, `002143A0`–`002143A8` | 1 | PROVEN |
| I-13 — the destructors stamp one vtable and differ only in size | complete bodies of `00213AD0`, `00213AA0`, `00213B00`; all three `lea rax, [rip -> 00906DE8]` | 1 | PROVEN |
| the text flush `001E8580` is the sole constructor of the DynGeo instances (§5, §6) | image-wide sweep of rip references into `00906DE8`-`00906F88`: six sites (three constructors, three destructor resets); image-wide direct-call sweep: constructors called only at `001E86BB`, `001E88C4`, `001E8A7D`, `001E8F84`, each preceded by `mov edx, 0x168/0x168/0x168/0x170` and `call 001A1470`; `001E8580`'s only caller `0017F868`; `0017F850` called from 12 sites in 8 functions incl. `002AC7EC`, `002AD7AE`. FABLE (`AS-3`), re-measured by OPUS 2026-09-25 | 1 | PROVEN (construction; the draw dispatch is not observed) |
| The 34 arms' per-selector semantics | [the language page](Text-And-Number-Rendering/the-text-control-code-language.md) §2.6, FABLE 2026-09-14/17/18 | carried, tier 1 at source | VERY HIGH |
| The authored-text census behind `9`, `#` and `+` | the same page's `UQ-177` answer, an archive census over 561 text-format files | carried, DATA | VERY HIGH |

**Superseded or extended by this contract** — filed in `CONTRADICTIONS.tsv`:

- *Old:* the interpreter stops at NUL or at an ordinary character. *New:* there is a **third** stop,
  a terminator word held on the painter.
- *Old:* the parsers return "a byte count" (unquantified). *New:* measured across all eleven — two
  fixed widths, one self-describing, two scanned.

## 16. Parity plan

| dimension | tested how |
|---|---|
| **STRUCTURAL** | the three dispatch tables byte for byte, including the duplicate target; the four vtables' four differing columns |
| **CONTRACT** | I-1 (the loop protocol), I-2 (the advance is the callee's return) and I-11 (the argument shift) — none is visible in rendered output |
| **STATE-TRANSITION** | §7's six edges, especially `0x03`'s act-and-stop and the terminator stop |
| **EDGE-CASE** | §10's eight paths, including the two do-nothing selectors and the skipped `Final` prefix |
| **INTEGRATION** | the mutual recursion of I-4: assert that an inserted name is measured by the same interpreter instance that is running |

**Not tested, and why:**

- **RNG** — nothing on either half draws.
- **CALCULATION** — the width arithmetic belongs to the language page's own formulas and to the
  numeric-formatting page, not to this contract.
- **PRESENTATION** — what each inline glyph looks like is `002AEB20`'s and is unread.
- **TIMING** — the page wait is a tick count whose stepper is another page's.
- **FULL SUBSYSTEM** — cannot be claimed while §13 is empty **and** while the join between the two
  halves (`GD-1`) is unestablished; a subsystem parity claim over two halves that may not be
  connected would be asserting the connection.

`002B20B0` (150 B) is the string accumulator `002ABB20` runs: over the byte string `r15` it stops at index `r13` or a byte above `0x0F`, and per byte calls `002B1FB0(ptr)` for a delta `ebp`, then `002B41F0(ptr, 0)` after zeroing `byte[rbp + ptr]` (restored after the call); the return is `sum(ebp)` with `r12d` accumulating `002B41F0`'s results - a code-map checksum that temporarily blanks each mapped cell.

Interior anchor `002B2113` (function `002B20B0`).

`002B27E0` (149 B) is the field-extract `002A5F40` calls: the string base is `[rcx+0x28] + word[+0x8A]` and `002B20B0(base, word[+0x8C])` yields the stop index `edi`; if `edi` is inside the NUL-terminated length the byte there is temporarily cleared, `002B2970(rcx, base, &f, &f2)` parses into two float outs, the byte is restored, and `cvttss2si(f2)` lands as the caller's `word[rsi]` - the u16 read one message-window field needs.

Interior anchor `002B284C` (function `002B27E0`).

## Falsification pass 1 — 2026-09-29 (OPUS): the tables and the DynGeo half hold; the callers are two shapes

Every static claim was re-derived from the shipping image (`73461d08…`) by
[`falsify_text_control_codes.py`](../../Tools/analysis-kit/gfz-scripts/falsify_text_control_codes.py). Whole-image
sweeps decode every listed body. Each check states its killer first. `audit_crossrefs.py` ran on this contract first.
The executed replays of §13 are not repeated here.

| check | killer searched for | result |
|---|---|---|
| T0 §2 | a different extent | survives: all seven bodies |
| T1 I-1 | another caller, or a caller of another shape | **corrected**: the seven cited sites are the only callers image-wide; five loop on `test eax, eax / je`, and two are single-shot length probes (I-1) |
| T2 §3 | a target outside the body; tables that do not tile | survives: all 50 targets inside; `cmp eax, 0xe` / `cmp eax, 0x50`; last instruction `002AE32C`; `002AE450` begins the next function |
| T3 I-2 | a parser path returning another value | survives on **every** `ret` path: five return 3, two return 4, `003FFD70` returns `+3` on its word, and `003FFB00` / `003FFBC0` / `003FFDF0` return computed values |
| T4 I-3 | another duplicate target; a case gap | survives: `002ACFC2` only, at 13 and 34; case bytes 0..34; `0` → 13, `_` → 34 |
| T5 I-4 | the recursion missing on either side | survives: ×7 / ×4, and both call back |
| T6 I-5 / I-8 | a passed painter; the terminator exiting elsewhere | survives: `[0209CC40]` at `002AC650`; `cmp ax, [rcx]` / `je 0x2ae31c`, the NUL test's exit |
| T7 I-6 | the escape consuming the selector | survives: `inc rcx` / `mov [rdi], rcx` then `ja 0x2acfc2`, and the exit returns 1 |
| T8 I-7 | no entry clear | survives: `xor eax, eax`; `*out2` zeroed; both advance cells cleared |
| T9 I-9 | a third tail jump, or `ShadowFinal` reaching the base | survives: two `jmp 0x2142a0`; none from `002143E0`; primitive 3 at `00214520` |
| T10 I-10 | a pool row that differs | survives: all six rows, including both negated twins |
| T11 I-11 | a different slot or third-argument form | survives: `jmp [.. + 0x118]` ×3; `xor r8d, r8d`; `setne`; `neg` / `sbb` / `and 2` |
| T12 I-12 | a different bound, stride or skip | survives: every anchor |
| T13 I-13 | a destructor stamping another vtable | survives: all three stamp `00906DE8`; free sizes `0x160` / `0x170` / `0x168` |
| T14 §3 | another differing slot; a slot 0 that is not `ret 0` | survives: columns 2, 6, 10 and 11 only; `0016D6A0` = `C2 00 00`; `00906DC8` has 3 slots |
| T15 §5/§6 | a seventh window reference; another constructor site; a second pointer | survives: 6 references, all in `00213xxx`; constructors only at the four `001E8580` sites, sized `0x168` ×3 and `0x170`; the flush's only caller is `0017F850` (12 sites in 8 functions); one pointer per slot-10 body |
| T16 §7 / §10.1 | a cursor write after `002AD01D` on the out-of-range path | **corrected**: none, so §7's "consumed anyway" and §10.1's "consumed and skipped" contradicted I-6's 2026-09-25 correction. Both now agree with it, as does the language page's modding note |

**Two of my own checks were wrong first.** T1 expected one shape, which is the claim under test, and T15's window was
wider than the page's (it caught the plain `DynGeoFontTextInstance` table at `00906DC8`). The corrected T1 now asserts
the two-shape split, so the script is a regression for it.

**Crossref (audit_crossrefs): recorded rather than resolved.**
- Neighbour edges into Presentation (49) and UI (61) arrive almost wholly through `0017F850`'s 12 call sites and the
  heap singleton's allocator `001A1470`.
- Audio (2), CoreRuntime (3) and Input (3) arrive through the display getters and the glyph drawer `002AEB20`, which
  §14.5 leaves unread.

`crossref_clean` stays `false`.

**Not attacked by this pass:**
- the per-selector semantics and the authored-text census (the language page's);
- the replayed claims of §13, which ran as code.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Presentation — BOTH DIRECTIONS, 49 edges: the draw half of this contract is presentation machinery, shared
with the rest of the render path.**
- **Construction.** The text flush `001E8580` (the only constructor of DynGeo instances) allocates them through
  `001A1470` and builds them with `00213A00`, `00213960` and `002138C0`. `001A1470` has six other presentation
  callers.
- **Display object.** The `display : draw Font` wrapper `0017F850` has three callers. The display getters
  `00182EB0` / `00182E80` and the predicate `00182F50` are also read by `00186CD0`, `00187950`, `002DB080` and three
  more render bodies. The aspect result `00183280` has four presentation callers.
- **Submission.** The interpreter `002AC5F0` and `002AF960` submit through `RenderCommand_SubmitCurrentBufferAndSwap`.
- **The eleven parsers** (`003FFAB0`-`003FFF10`) and the interpreter's re-entries are also called by `002B0280` and
  the encoded-message formatter `002B4810`, both filed Presentation.

This contract owns the byte language and the three DynGeo shapes. The render pipeline they feed is
`CONTRACT-render-command-list-and-graphics-handshake`'s.

**Input — DEPENDENCY, three edges.** The inline-glyph drawer `002AEB20` calls `001E0C10` / `001E0C30` and the control-code
dispatch `002AB8F0`, which ask the input layer which button glyph a control maps to. The mapping is owned by the
input binding pages; the language page's `UQ-177` residue carries which glyph each letter draws.

**CoreRuntimeScheduling — MECHANICAL, three edges.**
- `001E8580` allocates through the heap singleton's `001A1470`.
- `002A8C50` asks the shared mode predicate `001EDDA0`.
- The interpreter `002AC5F0` reads the language id through `00229E40`.

All three are shared leaves, not a scheduling claim.

**Audio — a LABEL-UNSUPPORTED crossing, two edges.** The display getters `00182EB0` / `00182E80` call `00225680` /
`002256A0`, the 4-byte `mov eax, [rcx+0x10|0x14]; ret` width and height readers of the display object
(`the-aspect-fit-and-the-super-wide-bound`, UE-2). The ledger files those two readers under Audio, but nothing in them
touches audio. The edge is real, and the layer label on its far end is the ledger's.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
