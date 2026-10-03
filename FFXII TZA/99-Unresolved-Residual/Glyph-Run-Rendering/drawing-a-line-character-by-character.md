---
system: Drawing a line of text, character by character
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Text
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001C2980`, `002AF960`, `002F0280`, `004EDB50`, `004F5360`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: residual-walk-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Drawing a line of text, character by character

**`002AAE40` is the loop.** 2,440 bytes, residual when this folder was surveyed — classified at GN161 `Presentation.Text.GlyphRunCharacterWalkAndScreenWidthBatchSplit` — and it is the thing that sits between
the two halves the rest of this folder documents: **it walks a string, hands control codes to the
interpreter, and turns everything else into a call to the font painter.**

## 1. What the player sees

**This is the function that puts one character after another.** Every time a line of dialogue
appears, this loop runs once per character in it — deciding, for each one, whether the byte is an
instruction to the text system or a letter to draw.

**Two things it does are visible if you know to look for them.**

**A line of text is cut into batches every 1,920 pixels of pen travel.** When the right edge of the
next glyph passes a moving threshold, the renderer **flushes what it has drawn so far, starts a new
batch, and moves the threshold one screen-width further** — then carries on in the middle of the
word. **A very long line is not one drawing operation; it is several, split at screen-width
boundaries.**

**And the loop stops at a hard limit that comes from the text record, not from the string.** A count
in the state record bounds how many characters this call will process, and the walk ends when the
count is reached whether or not the string has.

## 2. The shape

```c
state = copy of *param_1;                    // ~0xD0 bytes, taken onto the stack
if (DAT_0209CC48 == 0) return;               // nothing to draw into
ctx = DAT_0209CC40;
ctx[0x10E8] = FontPainter_Metric();          // 0017F880 -- the 23.0f-fallback metric
cursor = state.text;

loop:
  c = *(byte *)cursor;
  if (c < 0x10) {                            // an instruction
      if (c == 3) { ...measure, finish, return; }
      if (!TextControlCode_Interpret(&state_copy, &cursor, pen, &advance))   // 002AC5F0
          goto finish;
      ...copy the mutated state back...
  } else {                                   // a character
      ch    = decode(&state, &cursor);       // 002AC2F0
      glyph = FontPainter_LookupGlyph(ch);   // 0017F8C0
      cell  = 0020E600(...);
      ...build two render commands into DAT_0209CC50...
      FontPainter_SetCornerGradient(u, v, 1.0f, 1.0f);   // 0017FC90
      ...if the pen crossed a screen width, flush and re-begin (§4)...
      FontPainter_DrawGlyph(&record);                    // 0017F7C0
  }
  if (count_drawn >= state.limit) goto finish;
  pen.x += DAT_0209CC68;
  goto loop;
```

**The loop head, read at instruction level:**

```asm
002AAFD2  mov   rax, qword ptr [r14]      ; the cursor, by reference
002AAFDB  movzx edx, byte ptr [rax]       ; the character
002AAFDE  cmp   dl, 0xf
002AAFE1  jbe   0x002AB4F0                ; <= 0x0F -> the token arm
002AAFE7  mov   byte ptr [rcx + 0x1102], 0x0   ; the draw arm clears a mode byte
```

**`<= 0x0F` is the same boundary the interpreter uses** — bytes `0x01`–`0x0F` are tokens, `0x10` and
up are text. **`0x03` is handled here rather than there**, and it ends the run. The call into the
interpreter is `002AB5B0`, and **its result is tested immediately** (`002AB5B5`, `002AB5B7`) — the
`call / test eax,eax / jz` shape all seven of its call sites share.

## 3. The 160-byte glyph record, assembled in front of the call

**This document's strongest result is a confirmation, not a discovery.** The
[API document](the-font-painters-public-api.md) derived the glyph record's layout from how the
*emitter indexes it*. Here is the same record being **built by the caller**, and the two agree:

| the caller writes | the emitter reads |
|---|---|
| `fStack_258`…`fStack_24c` — four floats from the glyph cell (`cell+8`, `cell+0x10`+`cell+8`, `cell+0xC`, `cell+0x14`+`cell+0xC`) | `+0x00`–`+0x0F` — **source U and V** |
| `fStack_23c`…`fStack_230` — four floats built from `*param_3` and the advance | `+0x1C` — **screen X per corner** |
| `fStack_22c`…`fStack_220` — four floats built from `param_3[1]` and `DAT_0209CC64` | `+0x2C` — **screen Y per corner** |
| `auStack_1fc`, `auStack_1ec`, `auStack_1dc` — four copies each of three channel bytes | `+0x5C`, `+0x6C`, `+0x7C` — **per-corner colour** |
| `auStack_1cc` — four copies of `0x80` | `+0x8C` — **per-corner alpha**, and `0x80` is `1.0` in 1/128 fixed point |
| `iStack_1bc` — the palette selector | `+0x9C` — the index taken **mod 28** |

> **Both halves were read independently and neither was written from the other.** The emitter's
> reading came from `pfVar16[k*4]` indexing; this one from a stack block filled in source order.
> **`0x80` at `+0x8C` closes the fixed-point reading**: the caller writes the literal that the
> emitter divides by 128 to get `1.0`.

**And the corner gradient is set immediately before the draw**, from two values computed out of the
glyph's own cell coordinates, with `1.0f` for the other two — exactly the "set once, consumed once"
behaviour the API document inferred from the emitter's unconditional reset.

## 4. The screen-width flush

```c
if (DAT_01E0CDF4 < (glyph_right / 1920.0) && state.transform != 0) {
    FontPainter_Flush();                               // 0017F850
    FontPainter_Begin(state[+0xB8], 0x44, 1);          // 0017FA10 -- offscreen = 1
    FontPainter_Select(DAT_0209CC30, DAT_0209CC34, DAT_0209D480);   // 0017FD30
    FontPainter_SetTransform(state.transform);         // 0017FB00
    DAT_01E0CDF4 += 1.0;
}
```

**`DAT_01E0CDF4` is a screen-width counter, not a flag, and it starts at exactly `1.0`:**

```asm
002B034D  mov   dword ptr [0x01E0CDF4], 0x3f800000   ; = 1.0f, in 002B0280
002AB33D  comiss xmm0, dword ptr [0x01E0CDF4]        ; glyph_right / 1920 > counter ?
002AB3A7  movss  xmm0, dword ptr [0x01E0CDF4]
002AB3BD  movss  dword ptr [0x01E0CDF4], xmm0        ; counter += 1.0
```

**The comparison is against the glyph's right edge divided by 1920**, so the unit is literally
*screen widths of pen travel*, and the first flush falls at 1,920 pixels.

> **And it is not this function's mechanism — it is the cluster's.** 14 sites image-wide, in the
> same `comiss` / `movss` / `movss` triple, across **five** functions: `002A9F00` (`002AA4EF`),
> `002AAE40`, `002AF960` (`002AF9E9`), `002B0280` (`002B0B35`), and one at `002AABDB` that Ghidra
> attributes to no function at all. **Every text-drawing entry in the cluster splits its batches on
> the same counter**, and `002B0280` is where the counter is armed.

**Everything the new batch needs is re-established immediately:** the two handles, the font
selection, and the transform — because `0017FA10` resets the whole record (see
[painting a line of text](painting-a-line-of-text-into-a-render-target.md) §3).

> **This is the fourth call site of `0017FA10` and the third to pass the offscreen flag as a literal
> `1`.** It also resolves what the other sites were loading: **`state + 0xB8` is a field of the text
> state record**, not of some unrelated object — the same `[r14 + 0xb8]` seen at `002AC7F1`,
> `002AA51A` and `002AD7B3`.

**And `state + 0x20` is a pointer to the 4×4 transform**, null-checked before the whole block.

## 5. What this cost the instruments

**`get_function_callees(002AAE40)` returns an empty list.** The decompilation contains **~~fifteen~~ sixteen
distinct calls** *(corrected 2026-10-02, OPUS: the sixteen listed, `00808C40` included; the image body has the same sixteen)* — `0039C4A0`, `0017F880`, `002B2150`, `002B1F20`, `002AC5F0`, `002AC2F0`,
`0020E600`, `0017F8C0`, `0017FC90`, `0017F850`, `0017FA10`, `0017FD30`, `0017FB00`, `0017F7C0`,
`002B4730`, `00808C40`.

**And `get_function_by_address(002AAE40)` reports `body_start == body_end == 002AAE40`** — a
zero-byte body — for a function the exported function list records as **2,440 bytes** and which
decompiles in full.

> **The project's standing rule is that a negative from a call-graph query is not proof of absence.**
> This is that rule with a number on it: **0 reported, ~~15~~ 16 present** *(corrected 2026-10-02, OPUS: sixteen distinct callees)*, in the function the residual
> survey called *"the purest example of why a call-context classifier cannot touch these — no
> caller, and all three of its data references banned exception metadata."*
>
> **That reading was checked and it does not hold — the characterisation is correct.** The snapshot
> call graph the residual survey used, `Tools/work/graph/edges.tsv`, records `002AAE40` with
> **16 outgoing edges and 0 incoming**, against `002AC5F0`'s 44 and 7. ~~**The missing callers are a
> real property of the function; only the live program's view of it is empty.**~~

**Qualified 2026-09-15 (FABLE): the zero is right and the function is still reached.** The count is
correct — `002AAE40` has no `rel32` caller, no stored pointer to it and no image-base reference. What
the struck sentence lets a reader carry away is that nothing enters it, and that is not so. **It is
entered through a table.** Its single reference in the image is one quadword at `00916518`, slot 2 of
kind 3 in the four-group drawer table at `009164C0`, and `002AF960` calls
`[00120000 + 0x7F64D0 + kind × 24]` — the image base plus a displacement, which is why no
address-based scan finds the edge. The kind byte reaches 3 at exactly one site image-wide,
`002A49CA` in `002A4830`, which `002A6190`'s case-4 update calls and which then hands `002AF960` the
object it just stamped. `002A6190` is the message window, so this loop is the message window's
variant of the character walk. The chain is derived in full on
[numeric formatting and character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md),
§7.

**The section's own lesson survives intact and gains a second edge.** *"A negative from a call-graph
query is not proof of absence"* was written here about a live-program query returning `[]` for a
function with fifteen calls in it. The same sentence now covers the static direction too: **zero
incoming edges in `edges.tsv` is not proof that nothing calls it**, because a call through a table
reached by displacement from the image base is not an edge any of those instruments can see.

**The caveat that does survive is operational.** Sampling 15 residuals, **8 have a zero-byte body in
the live program** — `002AAE40`, `004EDB50`, `004F5360`, `002B8EE0`, `002F0280`, `0020AC30`,
`001D72F0`, `001C2980` — and every call-graph query against those returns nothing.

> **Use `edges.tsv` for call-graph questions about residuals. `get_function_callees` will answer
> `[]` for roughly half of them and will not say why.**

**And a note on the doubt itself.** This section first said the "no caller" claim *"may be an
artifact"*, hedged as *"not a claim that the characterisation is wrong"*. The hedge was right and
the doubt was still worth withdrawing rather than leaving attached: **an unfounded doubt hung on
someone else's correct finding is its own defect**, and it costs the next reader the same check.
*That withdrawal stands unchanged — it was about the live query being an artifact, and it was.* It
is not a re-assertion that nothing reaches `002AAE40`; the 2026-09-15 qualifier above settles that
separately, and settles it the other way.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `002AAE40` really the per-character loop, or one branch of something larger? | Two `goto`s back to `LAB_002AAFD2`, one from each arm, and the arm split is `*(byte *)*param_2 < 0x10` — **the interpreter's own token boundary.** |
| Is the glyph-record confirmation independent, or did this reading assume the API document? | The API layout came from the **emitter's indexing** (`pfVar16[k*4]`); this from a **stack block filled in source order** in a different function. **Neither derivation uses the other**, and they agree on all six field groups. |
| Is `0x80` really 1.0 rather than a coincidence? | The emitter multiplies by `0.0078125` = **1/128**, and `0x80` = 128. **The caller writes the literal the emitter divides by.** |
| Is `DAT_01E0CDF4` a counter or a configured threshold? | It is **incremented by `1.0` inside the branch it guards** (`002AB3A7`/`002AB3BD`) and **initialised to `1.0f` by a literal store** at `002B034D`. A configured threshold is not written by its own consumer. |
| Is the screen-width flush peculiar to this function? | **No — 14 sites in five functions**, all the same triple. This document originally said only that this loop does it; the census says the cluster does. |
| Does the flush really happen mid-line? | It is inside the per-character arm, after the render commands are built and **before** `0017F7C0` draws the glyph. **Nothing waits for a line end.** |
| Could the empty callee list mean the calls are indirect? | **No** — they are direct `CALL` instructions with literal targets; `002AB5B0  call 0x002AC5F0` was read in the disassembly. |

> *AC-9 note, 2026-09-12 (FABLE):* the pen advance in this loop is the spacing-global pair only —
> `[0209CC6C]` added before each glyph (~~`002AA0D2`~~ `002AAE40`+0x1BE) and `[0209CC68]` after (~~`002AA734`~~ `002AAE40`+0x82A) *(corrected 2026-10-02, OPUS: the two cited sites are `002A9F00`'s, +0x1D2 and +0x834; this loop's own reads are at the offsets given)*; the glyph
> descriptor's width sets the quad's right edge (`002AA4BB`–`002AA4C1`) and never the pen. Both
> globals are written by the callers as a qword pair (the numeric formatter zeroes them and
> stores its running total in `0209CC68`), so the pitch is per call, not per glyph.

## 7. What this document does not claim

What `DAT_0209CC40`'s fields mean beyond the four touched here (`+0x10D4` a counter reset at 20,
`+0x10E8` a line height, `+0x10FC` and `+0x1102` mode bytes). ~~What `002AC2F0` decodes.~~ *(answered: see the glyph-quads page §7: `002AC2F0` resolves the object bytes to glyph indices, and `+0x1102` is the line-start flag (UQ-370); 2026-10-02, OPUS)* What
~~`0020E600` returns.~~ *(answered: see §7 note: `0020E600` returns `ecx` plus the qword at `01F83530`, an image address — `mov eax, ecx; add rax, [01F83530]; ret`; 2026-10-02, OPUS)* What the two render commands written into `DAT_0209CC50` mean — their bit layout
is transcribed in the body and **not** decoded here. ~~Why the counter at `+0x10D4` triggers~~
~~`002B4730(1)` every twenty characters.~~ *(answered: see the flush note below and the glyph-quads page's emit row: the queue is flushed at `0x14` items; 2026-10-02, OPUS)* What `state + 0xB8` holds.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named these bodies only at their entries. Each interior address was read in the shipping
image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `004EDB50` | `004EDE5A` | `mov dword ptr [rip+…], 0x437F0000` — one of the repeated `255.0f` writes into the `02064B04`–`02064E3C` VU state bank the twin shares with `004F5360` |
| `004F5360` | `004F53FE` | `call r10` — invokes the `code *` visitor callback, the same contract `004EF860` documents for `004EDB50` |
| `002B8EE0` | `002B9162` | `call sinf` — first of two sine calls bracketing `002D8C80`/`002DD7E0`; a transform/easing path that also stores `0209E5A8`/`0209E5AC` |

*(Pass 22 adjacency, 2026-09-14: the glyph procs this page reads do not draw in one breath —
`002A9F00`, `002AAE40`, `002AC2F0` and `002AE610` call the `CoreRuntimeScheduling` ~~yield~~
`0020E600`, and `002AC5F0` calls `00229E40` (8 edges). ~~The account the pass asks for is that~~
~~these are the walk's yield points — the draw loop defers to the scheduler mid-glyph, which is~~
~~why a text pass can be preempted between characters.~~ `00229E40` is itself called by
`Rewards_Progression_Economy` `00317ED0` — the shared ~~yield accessor~~ getter has economy-side callers
too.)* *(corrected 2026-10-02, OPUS: neither is a yield: `0020E600` is `mov eax, ecx; add rax, [01F83530]; ret` (10 B), the image-address resolver, and `00229E40` is `mov eax, [01E02814]; ret` (7 B); no text pass is preempted through them)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — CLIENT.** `FUN_00581930`, owned by that layer, calls `002DD7E0` on this page. That caller is a 110-byte step that asks for message `0xD1`, then stores its argument into `dword[+0xD8]` and hands `[+0xF0]` on; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT.** `FUN_0033fed0`, owned by that layer, calls `00229E40` on this page. That caller is a 37-byte forwarder that reads the frame-mode getter and **maps the single value `0xA` to zero** before passing it on; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (1 edge, 2026-09-15 (FABLE)).** `002A6190`, named in §5 as the message window
whose case-4 update reaches `002AAE40`, calls `00249C60`, which the ledger owns as Audio. It is the
shared Audio accessor the shared-neighbours page measures at **99 callers**, and
[the message-window layout readers](../../16-UI/Message-Windows/the-message-window-layout-readers.md)
already adjudicates the same edge for `002A3960`, `002A6190` and `002A70B0` alike: **one accessor, not
a relationship.** Nothing about the kind-3 route depends on it. Tier 2 — `edges.tsv` and the ledger's
owner column; no body read for this note.

**StoryEvent — SERVICE.** `0020AC30` on this page calls `FUN_0020a800`, owned by that layer. What it reaches is a 554-byte routine in a `0x100`-byte frame that opens by calling an import through `008C2448`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## Interior citation — frontier hub `002B2150` (2026-09-18, SWE2-EC7)

`002B2150` — 861 B, 7 A-measured callers; the sweep that walks a command list against a
copied `0xD0`-byte state record. Interior verified: the record copies to the stack verbatim
(`002B2175`–`002B223B`), `[gbl+0x10FC]`/`+0x10FF` mode bytes are read before `0017F940` /
`0017FAE0` reset the three `0209CC60`-band accumulators; the loop over `rbx` list nodes runs
`002AC2F0` context-build + `0020E600` resolve + `0017F8C0` table-index per entry
(`002B22D9`–`002B22FE`), folds `dword[rdi + rsi*8]` against `0x80000000` to flip
`[gbl+0x10FC]` between 2 and 1 ([`002B22F4`](../../_index/ADDRESS-INDEX.md) region), and accumulates a weighted
`x*y*const` product into `xmm6` when the mark bit is set — a score-summing pass over the
line's elements, not a draw.


## Interior citation — frontier hub `0017FD30` (2026-09-18, SWE2-EC7)

`0017FD30` — 63 B, ~~6 A-measured callers~~ 8 calling functions, 18 sites *(corrected 2026-10-02, OPUS: rel32 sweep; the render-target page's eight)*; the arg-marshal in front of `001E9D20`. Interior
verified: `001B5FA0()` supplies the shared text object twice gated on the `dl` flag
(`0017FD43`/`0017FD50`), `r8d = 1` or `0` follows it ([`0017FD48`/`0017FD55`](../../_index/ADDRESS-INDEX.md)),
then `jmp 001E9D20` at `0017FD69` tail-calls with `(obj, edi, r8d, ebx)` — the caller's
two dwords plus the flag-derived selector. Pure adapter; no state.


### Interior citation — frontier hub `002B4730` (2026-09-18, SWE2-EC7)

`002B4730` — 218 B, 7 callers. Read from the shipping image: the render buffer
gets a 16-byte record appended — the cursor backs up by 0x10, `[+0xC]=1`, then a
header word `0x6c008150 | count<<16` is OR'd at
[`002B477B`](../../_index/ADDRESS-INDEX.md) (the same packet-header shape
`0036D400` emits for the graphics handshake), a
`0x10000000/0x15000000/0x13000000` trailer record follows, the end pointer at
`[rcx+8]` is advanced past the 16-alignment, and
`RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is invoked. When
`ebx != 0` a 24-byte-stride row selected by `dword[02F3EF54]` is published into
three globals. The `002B4730(1)` call every twenty characters is this emit.
## SWE2-EC7-34 update (2026-09-19) - `001C2980`

`001C2980` (897 B) is a cookie-protected text-record body - `01F44830` cookie, the `0x20` bound at `001C2A0E`, then the `001EAEA0`/`001EADB0`/`001EAD20`/`001EAC40`/`001EAC30` string family plus `00861EC0`/`00808C40`. Interior anchor `001C2AB2` (an `001EADB0` call).

## SWE2-EC7-52 update (2026-09-19) - `001EAEA0`

`001EAEA0` (613 B) is a text-record helper - `001EA770`/`001EAC60`/`001EAAB0`/`0067C5A0` calls. Interior anchor `001EAEC4` (a `001EA770` call).

## SWE2-EC7-53 update (2026-09-19) - `001EAAB0`

`001EAAB0` (369 B) is a call-free text-record integrator - `edx`->float scale-adds `+0xD8`/`+0xDC`/`+0xE0` into `+0x88`/`+0x8C`/`+0x90`, then `+0x58..` copied to `+0x98..`. Interior anchor `001EAB04` (the first store-back).

## SWE2-EC7-56 update (2026-09-19) - `001EAC60`

`001EAC60` (189 B) is a call-free vector scatter - `[rdx]`/`+0x10`/`+0x20`/`+0x30` vectors republished component-wise into `[rcx+0x20C]`-`[rcx+0x234]`. Interior anchor `001EAC79` (the `+0x20C` store).

## SWE2-EC7-57 update (2026-09-19) - `001EA770`

`001EA770` (183 B) is a text-record helper - `0067AF00` single call plus `008F3F58`. Interior anchor `001EA799` (a `0067AF00` call).

## SWE2-EC7-58 update (2026-09-19) - `0067AF00`

`0067AF00` (196 B) is a text-record helper - `00627BD0` single call plus one vcall, `008C2A18`/`00D6CF18`/`00D6CF20` and the `"NULL Pointer"` literal. Interior anchor `0067AF3F` (a `00627BD0` call).



## SWE2-EC7-65 update (2026-09-19) - `00627BD0`

`00627BD0` (135 B) is a text-record helper - `00584730`/`0067AFD0`. Interior anchor `00627BFD` (a `0067AFD0` call).


## SWE2-EC7-78 update (2026-09-20) - `0067C5A0` strlen + forward measured

`0067C5A0` (62 B) is the string forward the glyph callers use:
`0067BF70(rbx)` vetoes (nonzero return exits early); otherwise it
counts `byte[rbx+0x248]` to NUL (the `inc rax`/`cmp` loop from
`-1`) and tails `0067B530(rbx, len)` - length-then-delegate.
Interior anchor `0067C5C0` (the strlen loop's `inc rax`).

## SWE2-EC7-79 update (2026-09-20) - `00671B20` flag getter measured

`00671B20` (7 B) is the `+0x6C` bit-0 getter the `0067BF70` veto
reads: returns `[rcx+0x6C] & 1`.
Interior anchor `00671B23` (the `and eax, 1`).

## SWE2-EC7-101 update (2026-09-20) - `002A27C0` measured

`002A27C0` (38 B) is the registered-slot dispatch
`002A5CC0`, `002A6190` and `00474100` call: a null rcx
returns; `byte[+0x3B8]` indexes the `0209C4D0` table and
only when the entry's first dword equals `rcx` does the
tail `jmp 00244F00` fire - the identity-checked forward
the per-character draw shares.
Interior anchor `002A27D6` (the table compare).

## SWE2-EC7-118 update (2026-09-21) - the text-layout family measured

`0067B180` (529 B) is the
0x270-byte line-object
constructor `001EA3C0`
calls: zeroes `+0..+0x78`,
inits the `+0x80` sub-record
(kind 6, `-1` fields),
`00662A80` on `+0xC0` and
`001B6CE0` on `+0x140`, the
`+0x208` block carries three
1.0f fields and `0.65f` at
`+0x260`; `[+8]` latches the
inline buffer (`+0` =
`0x80000001`), and when
`dword[+0xB0] != 2` it
allocates two 0x88 records
through `0017D260` +
`006629F0` and swaps them in
via `001B8100`, `0060DF70`
resizing `+0x140` last.
Interior anchor `0067B2EC`
(the `0017D260` call).

`0067B4C0` (105 B) is the
kerning lookup `0067B530`
runs: walks the
`[+0x238]->+0x40->+0x28`
table in three-dword rows
(`count` at `rdx + 4`,
start `rdx + 8`) matching
`[r8]` against `row[0]`;
the hit returns `row[2] *
0.015625` - 1/64-unit
advance in ems.
Interior anchor `0067B4F0`
(the row compare).

`0067BEC0` (171 B) is the
slot dispatch `0067BF70`
calls: `esi = (+0x10 + 1)
mod btr(+0x18, 31)` picks
the round-robin slot in the
`+0x20` array (inline under
count 1), spins
`005CCB80(1)` while
`dword[slot + 0x20] > 0`,
then `00671D80(rbx, esi,
rbp)`; a 0 return sets
`byte[+0xE] = 2`.
Interior anchor `0067BF35`
(the spin call).

`0067BB30` (544 B) is the
bitmap-font bind `0067BD50`
runs: `006CCCE0` allocates
`+0x48`, the `+0x18` header
gets mode bytes
`5/1/2/2/2` keyed off
`dword[+0x1C] >> 7 & 1`,
`0061D9C0` gates, then
`00600120`/`00861EBA` build
`[rbx]` and `[rax + 8]`;
`0018D240` resolves
`"BitmapFontTexture"` and
`"LinearClampSampler"` by
name for `001B81B0`/
`00194540` application,
`0067C440` runs with three
1.0f, and the bit-31
`+8`/`+0x10` vector resets.
Interior anchor `0067BC34`
(the `0018D240` call).

`0067B040` (187 B) is the
grow-and-append `0067AF00`
calls: when `+0x10` length
plus `r8` (plus the
empty-flag) exceeds
`btr([rsi], 31)` it grows
through `00627BD0`,
`00861EBA` copies `r8` bytes
to `+8 + +0x10`, the length
relatches and NULs, and IAT
`008C2A18` re-measures for
the truncation case.
Interior anchor `0067B0B0`
(the `00861EBA` call).

`0067AFD0` (102 B) is the
byte-string dup `00627BD0`
calls: `ecx ? 0017D260(ecx,
align 1)` then copies `r8`
bytes from `rbx`, else 0.
Interior anchor `0067AFEB`
(the `0017D260` call).

`0067CBD0` (31 B) zeroes the
0x30-byte record
`0067B530` uses: `+0`, `+8`,
`+0x10`, `+0x14`, `+0x1C`,
`+0x24` and `byte +0x2C`.
Interior anchor `0067CBD9`
(the `+0x14` store).

Cross-reference note (batch
83): `0061D9C0` is also
called from the platform
side by `00625830` and the
resource side by
`00686DE0`, and `001EA3C0`
reaches resource callee
`00796350` - mechanical
fan-in on shared helpers,
dispositioned in-section
per the pass-22 rule.

## SWE2-EC7-119 update (2026-09-21) - the row-table bind family measured

`006CCCE0` (126 B) is the
name-to-object intern
`0067BB30` calls for its
`"BitmapFontTexture"` slot:
`ecx` indexes the pointer
cache at `02E5BE50`; an
empty slot walks the
`02CBF998` linked list,
byte-comparing each node's
name against the
`0xDE9BE0`-table string for
that index, then caches the
match.
Interior anchor `006CCD30`
(the compare loop).

`006747D0` (129 B) is the
row-slot write `006497E0`,
`0064A500` and `0067BF70`
call: under `btr(+0x18, 31)`
count the `edx*0x48` row of
the `+0x20` array (inline
under count 1) gets `r8` at
`+0x28` and `edx` at
`+0x30`, then
`0062EB90(01F7F5B8,
01F7F590)` notifies.
Interior anchor `00674845`
(the `0062EB90` call).

`00671D80` (254 B) is the
slot-target fill `0067BEC0`
calls per round-robin row:
on a null `row+0x40` the
`row[0]` object's
`vtable[+0x50]` sizes it,
`0017D260` allocates, and
the pointer lands at
`row+0x40`; the out-pair
gets `row+0x40 + dword[+0x68]`
and `dword[+0x70]`.
Interior anchor `00671E28`
(the `0017D260` call).

`00670070` (589 B) is the
`PDataBlock` creation loop
`00686DE0` runs: over
`btr(+0x20, 31)` rows of
the `+0x28` array it calls
`vtable[+0x18]` on the
`005FD050()` context's
`+0x108` device with
`{count, 1, 9, 0x20}`, then
after a `0061C550`
`"PDataBlock"` RTTI check
`vtable[+0x38]` with
`{0x27, 0xB, count>>2, 1}`;
HRESULT < 0 returns 9, else
`+0x74 |= 1`.
Interior anchor `00670171`
(the first device call).

`0066FAB0` (318 B) is the
index-data bind behind
`006497E0`/`0064A500`/
`0067BEC0`: a `+0x70` count
of zero logs `"Binding
0-sized index data block
has no effect. No D3D11
buffers were created."` and
returns 0; else each
`0x48`-stride row gets the
`+0x108` device's
`vtable[+0x18]` with
`{edi, 2, 2, 0x10000}` and
its `+0x40` cell zeroed,
ending `+0x6C |= 1`.
Interior anchor `0066FB85`
(the device call).

## SWE2-EC7-123 update (2026-09-21) - the four stage-gated shader creates measured

`00629AA0` and `00686DE0`
call four bodies that share
one create-if-absent shape on
a shader-set object: the
`+0x78` (or `+0x90`) slot
non-null exits early through
`0061F650`; otherwise
`005FD050` gives the context
and `[+0x108]` the device.
The `+0x70` fourcc gates the
stage - `vs`, `gs`, `ps`,
`cs` families (`0x??733530`
= `..50`, `0x??733431` =
`..41`) - and the device's
`+0x168` feature level must
reach `0xB000`/`0xA100`; a
mismatch logs the `"Unable
to..."` strings at
`00D550A0`/`00D550E0`/
`00D55140`/`00D55198` through
`005CDAA0` and falls through
to `0061F650`. Otherwise the
device's stage create -
`vtable[+0x60]`, `+0x68`,
`+0x78` or `+0x90` - runs
over the `+0x18`-count
`+0x20` records with the
`+0x78` out slot, and a
negative result exits 9.

`0061DFE0` (202 B) is the
`vs`-family create into
`+0x90` (`vtable[+0x60]`),
and alone of the four calls
`0061E0B0(+0x78, rbx)` after
`0061F650` returns.
`0061DD60` (183 B) is the
`gs`-family create
(`vtable[+0x68]`).
`0061DCA0` (183 B) is the
`ps`-family create
(`vtable[+0x78]`).
`0061DBE0` (186 B) is the
`cs`-family create
(`vtable[+0x90]`).
Interior anchor `0061E092`
(the `vs` device call);
interior anchor `0061DDFF`
(the `gs` device call);
interior anchor `0061DD3F`
(the `ps` device call);
interior anchor `0061DC7F`
(the `cs` device call).

## SWE2-EC7-124 update (2026-09-21) - the shader-create finish and its helpers measured

`0061F650` (186 B) is the
shared tail the four
stage-creates (`0061DFE0`/
`0061DD60`/`0061DCA0`/
`0061DBE0`) fall into: when
`[rcx]` is null and `+0x28`
names a size it builds a
`{size, 4, ...}` descriptor,
`005FD050`'s `+0x108` device
`vtable[+0x18]` creates it
into `[rcx]`, `0061C550`
names it
`"PShaderProgramConstantBuffer"`
(`00D54E18`), and
`0067B100(+8, +0x28)` runs.
A negative create exits 5.
Interior anchor `0061F6B2`
(the `vtable[+0x18]`
create).

`0061E0B0` (323 B) is the
binding-table build
`0061DFE0` runs after the
`vs` create: it walks the
`+8` list (count `[rcx]`
under `&0x7fffffff`,
0x20-stride records) and for
each entry with a live
pointer collects
`{ptr & ~flag, +0x10,
+0x14, +0x18, 0, flagA,
flagB}` into a stack table,
then the `+0x108` device's
`vtable[+0x58]` consumes
the table (count `[rbp+0x18]`
under `btr 0x1f`) and its
result lands at `[rsi+0x10]`.
Interior anchor `0061E1B9`
(the `vtable[+0x58]`
call).

`0061C080` (182 B) is the
format mapper `0061D9C0`
calls: `r9d > 1` returns
`0x55`; otherwise a 6-case
jump table on `ecx` returns
`4`/`0`, `0x10`/`0x14`,
`1`/`5`, `0x11`/`0x15`
(selected by `edx`), and
bit 7 is set on the result
unless `r8b` says otherwise.
Interior anchor `0061C0B1`
(the jump-table load).

`0059D510` (50 B) is the expected-size check `00686DE0` applies before committing a glyph-cell write: calls the object's `vtable+0x28` getter, adds the result into `[rbx+0x18]` (the running cursor), and returns `9` when the getter's value does not equal `r8d` — `9` is the caller's `size-mismatch` status, not a count.

Interior anchor `0059D523` (function `0059D510`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Platform — MECHANICAL, 10 edges.** `005FD050` is called by `0061F200`, `0061F710`, `006209C0`, `006239C0`; `00625830` calls `00623320`, `00624F70`, `00625210`, `00628690`; `0061D9C0` is called by `00625830`; `00625830` is called by `006253D0`.

**Resource — MECHANICAL, 18 edges.** `00686DE0` calls `00686830`, `006868C0`, `00686950`, `006869E0` and 4 more; `00796350` calls `0063B010`, `0063DA50`; `001EA3C0` calls `00796350`; `0059D510` is called by `00686DE0`; `0061D9C0` is called by `00686DE0`; `0061DBE0` is called by `00686DE0`; `0061DCA0` is called by `00686DE0`; `0061DD60` is called by `00686DE0`; `0061DFE0` is called by `00686DE0`; `00670070` is called by `00686DE0`.

**Rewards_Progression_Economy — MECHANICAL, 3 edges.** `00229E40` is called by `EnemyChain_UpdateOnDefeat` (`00317ED0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls `EnemyChain_TryAdvanceRank` (`003183D0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) is called by `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`).

**UI — MECHANICAL, 83 edges.** `002DD7E0` is called by `00280DE0`, `0028B140`, `002986E0`, `002A86A0` and 16 more; `0017FAE0` is called by `002AC5F0`, `002AE610`, `002AF340`, `002AF960` and 1 more; `0017F880` is called by `002A4830`, `002AC5F0`, `002AE610`, `002AF960`; `0017F940` is called by `002AC5F0`, `002AE610`, `002AF340`, `002B2150`; `0017F850` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017FA10` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017FB00` is called by `002AC5F0`, `002AF960`, `002D28E0`; `002AC2F0` is called by `002AE610`, `002AF340`, `002B2150`; `002B2150` is called by `002AC5F0`, `002AF340`, `002AF960`; `0017F8C0` is called by `002AF340`, `002B2150`; `0017FD30` is called by `002AC5F0`, `002AF960`; `00229E40` is called by `0028AAA0`, `002AC5F0`; `002A6190` calls `002A4430`, `002A4830`; `002A9F00` is called by `002AC5F0`, `002AE610`; `002AAE40` calls `002AC5F0`, `002B2150`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `002B0280` calls `002AE610`, `002B2150`; `002B0280` is called by `00243860`, `002A86A0`; `002B1F20` is called by `002AC5F0`, `002AF960`; `0039C4A0` is called by `002AC5F0`, `002AE610`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `002AC5F0`, `002AF960`; `002A4830` calls `002AF960`; `002A9F00` calls `002AC5F0`; `002AE610` is called by `002AC5F0`; `002AF960` calls `002B2150`; `002B2150` calls `002AC5F0`; `002B4730` is called by `002AC5F0`; `002D8C80` is called by `0055B6D0`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-drawing-a-line-character-by-character-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001EADB0` | 92 B | calls p = `001C26B0(rdx)`; unless `rdx` is non-null while p is null, it calls `00584730` on the old qword `rcx+0x38` when that is non-null with bit 0 clear, and stores p to qword `rcx+0x38`; on every path it stores 1 to byte `rcx+0xE8` | `001EADC8`, `001EADD8`, `001EADEC`, `001EADF1`, `001EADFF` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-drawing-a-line-character-by-character-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002CB4B0` | 733 B | dispatches on dword `[rdx]`: 1 calls `002CB4B0`+0x178 (`rcx+0x50`, qword `+0x38` of qword `0209AC30`, 9, `rcx`), copies the result's words `+4`..`+0xa` to `+0x98`..`+0x9e` if `rcx` is non-null, stores dword `[rdx+8]` at `+0xd4` and qword `[rdx+0x10]` at `+0xd8`, and if dword `+0x168` of that qword has no bit of `0xf0000` clears bit `0x1` of dword `+0x50`, else sets it, sets bit `0x1` of dword `+8` of the objects in qword `[rcx+0x60]` slots `+0x58` and `+0`..`+0x40` (stride 8) and clears it for slots `+0x80`, `+0x50`, `+0x48`; then stores `002DD7E0(0xf5)` in dwords `+0x28`..`+0x34` of the slot `+0x50` object and `002DD7E0(0xf4)` in those of slot `+0x48`, clears bit `0x800` of dword `+0x40` and calls +0x2C6 (`rcx`, 0x65); 2 calls +0x3E (`rcx`) and tests qword `+0xd8` the same way: no bit clears bit `0x1` of `+0x50`, else sets it and bit `0x1` of the slot `+0x58` object and copies bit `0x1` of dword `+0xe4` into bit `0x1` of dword `+8` of the slot `+0`..`+0x40` objects; 4 does nothing; these return 0, and other values tail-jump to `002CB4B0`+0x36 (`rcx`) | Interior anchor `002CB628`; Interior anchor `002CB674`; Interior anchor `002CB738`; Interior anchor `002CB53B`; Interior anchor `002CB4E6` |
| `00559910` | 192 B | with `E` = `rcx` + `r9d`*0x20 (signed) and `S` = qword `+8` of qword `[rdx+0x10]`, stores qword `E+0xe8` at `S+0x18`, the result of the call at `00559910`+0x38 (0) at `S+0x20` and `002DD7E0(0 if word E+0xf4 is non-zero, else 2)` at `S+0x24`; sets bit `0x1` of dword `+8` of `T` = qword `[[rdx+0x10]]` when word `E+0xf0` is not `0xffff` and byte `E+0xf2` is not `0xff`, and clears it otherwise; in the set case also writes byte `E+0xf2` to word `T+0xa` and byte `+7` of that 8-byte entry of qword `T+0x20` to byte `T+0x39`; returns 1 | Interior anchor `00559944`; Interior anchor `00559962`; Interior anchor `00559985`; Interior anchor `00559998`; Interior anchor `005599B6` |
| `005639D0` | 316 B | with `B` = qword `+8` of qword `[rdx+0x10]`: when qword `rcx+0xe0` is null calls `005639D0`+0x2F (`rdx`, 0), sets bit `0x1` of dword `B+8` and stores the result of call +0x45 (0x7d8) at `B+0x18`, that of call +0x50 (0) at `B+0x20`, word `[B]+4` minus `0x14` at `B+0xc` and word `[B]+6` at `B+0xe`; otherwise, with `E` = `[rcx+0xe0]` + `r9d`*0x20 and `T` = qword `[[rdx+0x10]]`, clears bit `0x1` of dword `T+8` when byte `E+0xa` is `0xff`, else sets it and writes that byte to word `T+0xa` and byte `+7` of that 8-byte entry of qword `T+0x20` to byte `T+0x39`, stores qword `[E]`, the result of call +0xC3 (0) and words `[B]+4`/`[B]+6` at `B+0x18`/`+0x20`/`+0xc`/`+0xe`, stores `002DD7E0(6 if bit 0x100 of dword rcx+0x180 is set and signed word rcx+0x17c equals r9d, else 0)` at `B+0x24`, and calls +0x117 (`rdx`, `E`, 2, 7); returns 1 on both paths | Interior anchor `005639F8`; Interior anchor `00563A33`; Interior anchor `00563A57`; Interior anchor `00563ACF`; Interior anchor `00563AE7` |
| `00563C00` | 274 B | with `B` = qword `+8` of qword `[rdx+0x10]`: when qword `rcx+0xe0` is null calls `00563C00`+0x29 (`rdx`, 0), sets bit `0x1` of dword `B+8` and stores the result of call +0x3F (0x7d8) at `B+0x18`, that of call +0x4A (0) at `B+0x20`, word `[B]+4` minus `0x14` at `B+0xc` and word `[B]+6` at `B+0xe`; otherwise, with `E` = `[rcx+0xe0]` + `r9d`*0x20 and `T` = qword `[[rdx+0x10]]`, clears bit `0x1` of dword `T+8` when byte `E+0xa` is `0xff`, else sets it and writes that byte to word `T+0xa` and byte `+7` of that 8-byte entry of qword `T+0x20` to byte `T+0x39`, stores qword `[E]`, the result of call +0xBA (0) and words `[B]+4`/`[B]+6` at `B+0x18`/`+0x20`/`+0xc`/`+0xe`, and stores `002DD7E0(6 if bit 0x100 of dword rcx+0x180 is set and signed word rcx+0x17c equals r9d, else 0)` at `B+0x24`; returns 1 on both paths | Interior anchor `00563C22`; Interior anchor `00563C5D`; Interior anchor `00563C7C`; Interior anchor `00563CF5`; Interior anchor `00563CFA` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-drawing-a-line-character-by-character-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00686830` | 138 B | zeroes qwords [rcx], +8, +0x10 and dword +0x18; stores `h` = `rdx`+0x38 at qword +0x20, qword [h] at qword +0x28 (0 when it equals `h`) and the static `02D39A40` at qword +0x30; then, while `001B7CE0(rcx)` returns a zero byte (there is no other exit), replaces a non-null qword +0x28 by the qword it points at (0 when that equals qword +0x20); then calls `001AA0A0(rcx)` and returns `rcx` | `0068683F`, `0068684D`, `0068685B`, `0068686D`, `0068689B` |
| `006868C0` | 138 B | zeroes qwords [rcx], +8, +0x10 and dword +0x18; stores `h` = `rdx`+0x38 at qword +0x20, qword [h] at qword +0x28 (0 when it equals `h`) and the static `02CB78A0` at qword +0x30; then, while `001B7CE0(rcx)` returns a zero byte (there is no other exit), replaces a non-null qword +0x28 by the qword it points at (0 when that equals qword +0x20); then calls `001AA0A0(rcx)` and returns `rcx` | `006868CF`, `006868DD`, `006868EB`, `006868FD`, `0068692B` |
| `00686950` | 138 B | zeroes qwords [rcx], +8, +0x10 and dword +0x18; stores `h` = `rdx`+0x38 at qword +0x20, qword [h] at qword +0x28 (0 when it equals `h`) and the static `02CF1C40` at qword +0x30; then, while `001B7CE0(rcx)` returns a zero byte (there is no other exit), replaces a non-null qword +0x28 by the qword it points at (0 when that equals qword +0x20); then calls `001AA0A0(rcx)` and returns `rcx` | `0068695F`, `0068696D`, `0068697B`, `0068698D`, `006869BB` |
| `006869E0` | 138 B | zeroes qwords [rcx], +8, +0x10 and dword +0x18; stores `h` = `rdx`+0x38 at qword +0x20, qword [h] at qword +0x28 (0 when it equals `h`) and the static `02CF1A40` at qword +0x30; then, while `001B7CE0(rcx)` returns a zero byte (there is no other exit), replaces a non-null qword +0x28 by the qword it points at (0 when that equals qword +0x20); then calls `001AA0A0(rcx)` and returns `rcx` | `006869EF`, `006869FD`, `00686A0B`, `00686A1D`, `00686A4B` |
