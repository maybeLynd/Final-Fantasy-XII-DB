---
system: Glyph-run rendering — how a line of text becomes drawn characters
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Text
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001C2980`, `002AF960`, `0036A570`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  residual_sha256: c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff
  residual_regenerated: 2026-09-02, project GFZ_H9E, CHECKPOINT VERIFIED
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-d2 (author recused)
  falsification_result: 4 batch rows cleared, 1 address reading overturned
  crossref_clean: true
  reopened_count: 0
---

# Glyph-run rendering — how a line of text becomes drawn characters

> Four of the 158 unclassified functions are the machinery that turns a string of characters
> into drawn glyphs on screen, together with the markup language the game's authored text is
> written in.

---

## 1. What the player sees

**Text.** Every line of dialogue in a cutscene, every entry in the Battle Menu, every item name
in the Bazaar, the numbers over a character's head when they take damage, the yellow "Location"
banner when you cross into a new zone. If you can read it, this is what drew it.

The interesting part is not that the game draws text — it is what the game's writers were able
to *say* to the text system. FFXII's message data is not plain text. It is written in a small
markup language, and the interpreter for that language is one of the functions here. Inside a
line of authored text, the writers could:

- **change colour mid-sentence** — the reason a character's name or a key item can appear in a
  different colour inside an otherwise white line of dialogue, and the reason a menu entry you
  cannot currently pick is drawn dimmed rather than hidden;
- **right-align or centre** a line inside its box — how numbers line up in a column in the menus
  instead of drifting;
- **move the cursor** to an exact position, or nudge it sideways;
- **change size**, in whole percent, horizontally and vertically independently;
- **rotate** the text;
- **insert an icon** into the middle of a sentence — the little glyphs for elements, weapon
  types and gambit conditions that sit inline with words;
- **insert a blank exactly one digit wide**, which is how a number gets padded on the left
  without the digits themselves jittering;
- **choose a different font, and a different palette** for it.

The other thing worth knowing as a player is small and very visible once you have seen it:
**text drawn at its natural size is point-sampled and crisp; text the game has scaled is
filtered and soft.** That is a single bit in a single command, set only when the size is not
exactly 100 %, and it is why scaled-up text in this game looks blurry in a specific way rather
than blocky.

And there is a second text renderer. A string whose data begins with the two letters `ex` is
handed to ~~a completely different drawing path~~ this page's glyph-run path, and the others to `002B0280` *(corrected 2026-10-02, OPUS: `002D8690`+0x90 tests the prefix and an `ex` string goes to `003649A0` at +0xAC)*. ~~Which strings those are is not established here.~~ *(answered: see §7, ANSWERED 2026-09-25: an `ex` string is `ex00` and UTF-16LE text; 2026-10-02, OPUS)*

### Why it matters that these were unexplained

The residual is the 158 functions in the executable that carry no classification at all. The
database's standing description of them is that they are large, that they have no authored
strings, and that they must be read one at a time. For a modder that meant: somewhere in
`FFXII_TZA.exe` sat 180 KB of substantial code that nobody could name, and one of the things
hiding in it was *how the game draws words*. You cannot retime a message box, restyle a menu,
or add a language to a game whose text renderer you cannot find.

Four of them are now found. The other ~~153~~ 154 *(corrected 2026-10-02, OPUS: 158 − 4)* are not, and this document says so plainly.

---

## 2. Native mechanism

### The shape of the thing

Drawing one line of text is four functions cooperating over one small state record:

```
  a text-drawing request
     -> 0053E0B0   for each line in a scrolling window: cull it, draw a shadow pass,
        |          draw the real pass, or draw an inline icon
        v
     002D8690 / 002D87D0   pick a renderer: strings tagged "ex" go elsewhere   <- corrected 2026-10-02, OPUS: inverted - ex strings come here (002D8690+0xAC calls 003649A0); the others go to 002B0280
        |
        v
     003649A0   walk the characters, look each glyph up, emit a textured quad per character
        |
        +-> 003647E0   before each character: handle control codes and open '{'
        |      |
        |      +-> 00366110   interpret one {tag} and mutate the text state
        |
        +-> 00365FD0 / 00364210   glyph cache: hit-and-promote, or miss-and-fill
        |
        +-> RenderCommand_BeginSubpacket / FinalizeSubpacket / SubmitCurrentBufferAndSwap

  00364530   the same walk with no drawing: advance the cursor and measure
```

`00364530` exists because sometimes the game needs to know how wide a run *will* be before it
draws it — which is exactly what right-alignment and centring need.

### Reading the string

The text record's first four bytes are a header the renderers skip; the characters begin at
`+0x04` and are **16-bit, NUL-terminated**. Two independent facts prove they are text and not
a command list:

- `U+0020` (space) and `U+3000` (the CJK **ideographic space**, the full-width space used in
  Japanese typesetting) are *both* special-cased, and both take the same "advance the pen by a
  space's width" path. Nothing but a text stream reserves those two codes together.
- `{` (`0x7B`) opens a tag, `}` (`0x7D`) closes it, and the eleven tag letters are ASCII
  lowercase whose meanings match their initials.

Anything that is not a control code or a tag is a character, and gets a glyph.

### Finding the glyph

Every character is looked up twice-over. First in a **least-recently-used cache** kept as a
doubly-linked list (`00365FD0`): if the character is already resident for this font, its node
is unlinked and moved to the head of the list, and that is the whole cost. On a miss
(`00364210`) the *tail* of the list — the least recently used glyph — is evicted, and the new
glyph is filled into that node: its record is found by a linear scan of the font's glyph table,
and its cell dimensions are **rounded up to the next power of two** (8, 16, 32, 64, 128).

That rounding is not cosmetic. The graphics hardware this engine still speaks to takes texture
dimensions as **log2**, so a glyph cell has to be a power of two to be addressable at all. The
routine that converts back, `003666E0`, is a bit-scan that returns `log2(n)` for power-of-two
`n` — and its result is written straight into the texture-descriptor command.

The glyph's pixels are then uploaded to a fixed address in graphics local memory
(`0x3440`), which is the same base the texture descriptor points at.

**Player consequence:** a line of text using many distinct characters costs more than a line
that repeats them, because each new character evicts an older one and re-uploads pixels. In a
language with a large character set this is the difference between a cached run and a
continuously-thrashing one.

### Emitting the quad

For each character the renderer emits **one four-vertex textured triangle strip** — the two
triangles of a rectangle — into the render command buffer, as a sequence of 16-byte records
each carrying a payload and a command code. What each code carries is established from the
body itself:

| code | payload the body builds | so the record is |
|---:|---|---|
| `0x3F` | zero | a texture-cache flush |
| `0x42` | `0x44` | blending setup |
| `0x47` | `0x3001` | the pixel test setup |
| `0x08` | `5` | texture wrap/clamp setup |
| `0x06` | glyph base + `log2(texW)` + `log2(texH)` | **the texture descriptor** |
| `0x14` | `0x20` when scaled, `0` otherwise | **the filter mode** |
| `0x00` | `0x154` | the primitive setup |
| `0x01` | the four colour bytes + float `1.0` | **the colour** |
| `0x03` | the glyph's texel rectangle × 16 | **a texture coordinate** |
| `0x05` | the projected screen position | **a vertex position** |

The last two alternate: coordinate, position, coordinate, position — four times, one pair per
corner. The four corners are emitted in the order top-left, bottom-left, top-right,
bottom-right, and the four texture coordinates are emitted in exactly the matching order, which
is what makes the strip cover the glyph cell.

**The `0x154` primitive word is worth unpacking**, because every bit of it is visible in play:

```
0x154 = 0b101_0101_0100
  bits 0-2 = 4    -> triangle strip  (4 vertices = 2 triangles = 1 quad)
  bit  3   = 0    -> no per-vertex colour interpolation: the glyph is one flat colour
  bit  4   = 1    -> texturing on
  bit  5   = 0    -> no fog
  bit  6   = 1    -> alpha blending on, which is why glyph edges are soft against the scene
  bit  7   = 0    -> no anti-aliasing
  bit  8   = 1    -> texel-indexed coordinates rather than normalised ones
```

Flat colour plus alpha blending is the whole visual character of FFXII's text: a single tint
per glyph, composited over whatever is behind it.

> **Naming caveat, stated deliberately.** The *roles* above are proven from the body — the
> record carrying the glyph's texel rectangle is a texture coordinate whatever it is called.
> The command codes also match the PlayStation 2 Graphics Synthesizer register numbers
> (`0x00` PRIM, `0x01` RGBAQ, `0x03` UV, `0x05` XYZ2, `0x06` TEX0, `0x08` CLAMP, `0x14` TEX1,
> `0x3F` TEXFLUSH, `0x42` ALPHA, `0x47` TEST), and this database already documents that the
> engine kept its PS2 drawing vocabulary — see
> [gi-render-command-family](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md).
> That correspondence is **corroboration and is not load-bearing**: strike the PS2 names and
> every claim in this document still stands on the body.

### The renderer names itself

The strongest single piece of evidence is not structural. When `003649A0` closes its drawing
scope it calls `0017F850`, whose only three actions are to push a named marker, flush the font
device, and pop the marker. The name it pushes is an authored string in the executable:

```
008C5B18  .rdata   "display : draw Font"
```

It is the only string of its form in the binary, it is the target of exactly one instruction in
the whole `.text` section, and that instruction is inside `0017F850`. The marker is emitted
only while a capture is active, so it is instrumentation rather than a log line — but it is the
engine's own word for what the code above it does.

**Four residual-when-surveyed functions call `0017F850`**: `003649A0`, and also `002AC5F0`
(7,489 B — still the largest unclassified function in the game at GN161), `002AAE40` (2,440 B) and
`002AF960` (1,117 B). Three of the four are now classified; `002AC5F0` alone remains in the
certified 30. See §8; this is the most consequential thing this block found.

> **Corrected 2026-09-14 (OPUS): ~~two~~ three of the four are no longer residual** *(answered: see the paragraph above and the end of this note: `002AF960` followed at GN161; 2026-10-02, OPUS)*. The certified parent
> classified `003649A0` as `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance` and
> `002AAE40` as `Presentation.Text.GlyphRunCharacterWalkAndScreenWidthBatchSplit`, and both left
> the residual list when it went **158 → 139**. `002AF960` followed when the list went **139 → 30** at GN161 — classified `UI.Text.GlyphRunPositioner`. `002AC5F0` alone remains residual — it is the largest unclassified function in the game.
> **The call edges are untouched — all four still call `0017F850`**, and the finding this block
> reports stands; it is the word *unclassified* that has expired.
>
> **For `003649A0` the parent independently confirmed this page's reading.** §299 proposed the name
> `Text_EmitGlyphRunQuads` — *"walks the character stream, resolves each glyph, emits one textured
> quad per character"* — and the parent's tag is `GlyphRunTexturedQuadEmissionAndPenAdvance`. Two
> readings that did not consult each other, agreeing. **`002AAE40` gets no such support here**: this
> page lists it and never characterises it, so its tag is the parent's claim alone.

### The markup language

`00366110` reads the byte after `{`, dispatches on it, mutates the shared text state, and loops
until it sees `}`. Eleven tags, verified against the raw jump table in the binary (§8):

| tag | with no argument | with arguments | what a player sees |
|---|---|---|---|
| `{a}` | — | `1` right-align, `2` centre | a line pushed to the right edge of its box, or centred in it |
| `{c}` | restore the default colour | `A B G R` | a coloured word inside a white sentence |
| `{f}` | clear the cell-size override | `w h` | glyphs forced into a fixed cell |
| `{h}` | — | signed 16-bit | a horizontal nudge, in pixels |
| `{i}` | — | 3 bytes | an inline icon *(answered: see §7: the three bytes have no reader in this build; 2026-10-02, OPUS)* |
| `{k}` | font 0 | font index, bounds-checked | a different typeface |
| `{n}` | cursor back to the box origin | `dx`, `dy` from the origin | a line break, or an exact placement |
| `{p}` | palette `0x20` | index + `0x20`, bounds-checked | a different colour ramp for the same font |
| `{r}` | no rotation | signed angle | rotated text |
| `{s}` | 100 %, 100 % | `sx`, `sy` **in whole percent** | bigger or smaller text |
| `{v}` | cursor Y to 0 | signed 16-bit | a vertical placement |

Any other letter falls through to a shared do-nothing target, so an unrecognised tag is silently
ignored rather than drawn.

`{r}` is the one that does real work: it loads the 4×4 identity into the shared matrix at
`022CBE00+0x1E0` and multiplies in a rotation. `003649A0` then pushes each of the four glyph
corners through that matrix before projecting them — which is why rotated text stays a proper
rotated rectangle rather than a sheared one.

### The bare control codes

Below `{`, four single 16-bit codes are handled by `003647E0` directly, before any glyph lookup:

| code | effect |
|---:|---|
| `0x0001` | advance the pen by the advance width of the character `'0'` — **a figure space** |
| `0x0002` | set the alpha byte to `savedAlpha / 5` — **dim** |
| `0x0003` | restore the alpha byte from the saved copy — **undim** |
| `0x0020`, `0x3000` | advance the pen by a space's width |

Codes `2` and `3` are gated on bit 0 of the state byte at `+0x63`, so a caller can disable
dimming for a run.

**Code 1 answers a question this database had recorded as open.** The
[numeric formatting](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md)
document withdrew a claim that digits are laid out at the fixed width of `'0'`, and stated that
whether numbers produce even columns on screen "is not known — the measuring happens in a
function this document has not read." That function is `003647E0`, and the answer is: **digits
are drawn at their own advances; the *padding* is a control code that inserts a blank exactly
one `'0'` wide.** So a right-aligned number does line up in a column, and the withdrawn claim
stays withdrawn — the mechanism is a figure space, not a per-digit width override.

### Drawing a line in a message window

`0053E0B0` walks a window's line records (32 bytes each) and for each one:

1. **culls it against the scroll viewport** with a 32-pixel margin at both ends, so a line
   scrolled just off the top or bottom is skipped;
2. modulates the text colour by the window's own intensity — `(channel * intensity) >> 7`, a
   0x80-is-1.0 fixed-point multiply — which is why **text fades with its box** rather than
   staying solid while the frame dissolves;
3. if the record's shadow byte is non-zero, draws the *same string a second time* at an offset
   taken from a per-kind table, with both style indices incremented by one, **before** drawing
   the real pass;
4. for record kinds `>= 3`, takes an icon path instead, unpacking a texel rectangle from a pair
   of 12-bit fields.

Step 3 is the shape of a drop shadow. The offsets themselves live in runtime data this pass did
not observe, so the *mechanism* is established and the visual result is inferred; see §7.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `003649A0` | `Text_EmitGlyphRunQuads` | 3020 B | **classified GN161** `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance`. Walks the character stream, resolves each glyph, emits one textured quad per character |
| `00366110` | `Text_InterpretBraceTag` | 1318 B | **classified GN161** `Presentation.Text.BraceTagMarkupInterpreterAndTextStateMutation`. The `{tag}` interpreter, eleven tags |
| `00364530` | `Text_MeasureGlyphRun` | 684 B | **classified GN161** `Presentation.Text.NonDrawingGlyphRunAdvanceAndExtentMeasurement`. The same walk with no drawing: advance and measure |
| `0053E0B0` | `Text_DrawScrolledWindowLines` | 718 B | **classified GN161** `Presentation.Text.ScrolledWindowLineCullShadowAndGlyphRunDispatch`. Cull, shadow pass, text pass, icon path |
| `003647E0` | `Text_HandleControlCodes` | 366 B | Control codes `1`, `2`, `3`, the two spaces, and the `{` entry |
| `00364210` | `GlyphCache_FillOnMiss` | 367 B | Evicts the LRU tail, fills it from the font glyph table, rounds cell dims to powers of two |
| `00365FD0` | `GlyphCache_PromoteOnHit` | 171 B | Finds the node and moves it to the list head |
| `003666E0` | `Log2OfPowerOfTwo` | 88 B | Bit-scan returning `log2(n)`; feeds the texture descriptor |
| `00364980` | `Text_IsExPrefixed` | 28 B | Returns 1 iff the record's first two bytes are `'e'`,`'x'` — the renderer selector |
| `00202B90` | `Vec3TransformByMatrix` | 181 B | `out = in.x*row0 + in.y*row1 + in.z*row2`; rotates the four corners |
| `00203170` | `LoadIdentityMatrix4x4` | 44 B | Copies the 4×4 identity from `.rdata` |
| `0017F850` | `FontScope_CloseAndFlush` | 38 B | Pushes the marker `"display : draw Font"`, flushes, pops |
| `002D8690` | — | 306 B | Selects between the two renderers; modulates colour by window intensity |
| `002D87D0` | — | 306 B | Near-identical sibling of `002D8690` (matrix argument order differs) |
| `002B0280` | — | 6441 B | ~~The *other* text renderer, taken when the record is `ex`-prefixed~~ **The byte-charset renderer, taken when the record is NOT `ex`-prefixed** (polarity corrected 2026-09-25, FABLE, Claude Opus 5.5; see UQ-361) |
| `003A2090` | `RenderCommand_BeginSubpacket` | 39 B | Reserves and opens a command subpacket |
| `003A2020` | `RenderCommand_FinalizeSubpacket` | 102 B | Patches the record count into the subpacket header |
| `003A1DB0` | `RenderCommand_SubmitCurrentBufferAndSwap` | 84 B | Submits the filled buffer and swaps |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `008C5B18` | — | `.rdata` string | `"display : draw Font"`, the only string of its form; one code reference |
| `00366638` | — | `.text` jump table | 22 dword RVAs, the dispatch table of `00366110` |
| `01CEBC84` | — | `.rdata` float | `16.0` — texture-coordinate fixed-point scale |
| `01CEBB70` | — | `.rdata` float | `0.5` — half-texel inset |
| `01CEBBA8` | — | `.rdata` float | `1.0` — the "unscaled" comparand |
| `008F3134` | — | `.rdata` float | `100.0` — the `{s}` percent divisor |
| `008C5F80` | — | `.rdata` `float[4]` pool | **a pool of six ± axis vectors, not a matrix object.** *(answered: see §10, "Both readings are over-reads": `+0x60` is no axis vector and `+0x70` is past the pool; 2026-10-02, OPUS)* Four of them — `+0x00`, `+0x10`, `+0x30`, `+0x50` — are loaded here and do assemble to the identity; `+0x20` and `+0x40` hold the negations `0 -1 0 0` and `0 0 -1 0` and are not read by this path. **Corrected 2026-09-02** — see the note below |
| `00D10F40` | — | `.rdata` string table | `"RS=%p"`, `"M2/l"`, `"M2/U"`, `"M2/L"`, `"M /l"`, `"M /U"`, `"M /L"`, `"FREE"`, `"/I"`, `"/C"` — referenced by `0036A570` (§8; classified GN161 `Runtime.Diagnostics.MemUsageReport`) |

Addresses are Ghidra image base `0x00120000`.

---

## 4. Data structures and formulas

### The text state record

Passed to `003649A0`, `00364530`, `003647E0` and `00366110`. Three of those four decompile with
different pointer types over the same record and **agree on every field**, which is the check
that these are byte offsets and not array indices.

```
TextState
  +0x00  f32   masterScale        compared against 1.0 to decide filtering
  +0x04  f32   scaleX             from {s}, = percent / 100
  +0x08  f32   scaleY             from {s}
  +0x0C  f32   rotation           from {r}; non-zero enables the corner transform
  +0x20  ptr   matrix             4x4 float; NOT a callback (UQ-365, 2026-09-18): passed to the matrix setter 0017FB00
                                  and, as an argument, to a transform whose PC body is empty
  +0x28  ptr   textRecord         +0x00 4-byte header, +0x04 UTF-16 NUL-terminated
  +0x30  u8    colourR            }
  +0x31  u8    colourG            }  live colour, mutated by {c} and codes 2/3
  +0x32  u8    colourB            }
  +0x33  u8    colourA            }
  +0x34  u8[4] savedColour        the default {c} and code 3 restore from
  +0x38  f32   penX               accumulates advance widths
  +0x3C  f32   penY
  +0x40  f32   glyphWidth         last glyph's cell width
  +0x44  f32   glyphHeight
  +0x48  f32   widthOverride      from {f}; 0 = use the glyph's own
  +0x4C  f32   heightOverride     from {f}
  +0x50  s32   yOffset
  +0x54  u16   depth              written into every vertex position
  +0x56  u16   needsFiltering     1 iff any of masterScale/scaleX/scaleY != 1.0
  +0x58  s16   boxOriginX         {n} returns the pen here
  +0x5A  s16   boxOriginY
  +0x5C  s16   boxWidth           {a} right-aligns and centres against this
  +0x60  u8    fontId             from {k}
  +0x61  u8    palette            from {p}, biased by 0x20
  +0x62  u8    trailingTrimFlag   measure pass only
  +0x63  u8    flags              bit 0 gates control codes 2 and 3
```

### The font glyph table record — 12 bytes

`[022CBE00 + 0x10 + fontId*8]` points at a table: `+0x04` is an `int` count, records start at
`+0x10`.

```
GlyphTableRecord
  +0x00  u16   characterCode      UTF-16
  +0x02  u8    cellWidth          texels
  +0x03  u8    cellHeight         texels
  +0x04  u8    advanceWidth      the glyph's authored advance, in texels (§7 UQ-364)
  +0x08  u32   pixelOffset        offset into [022CBE00 + 0x110 + fontId*8]
```

The field at `+0x04` has exactly one reader in this block. At the NUL, if the state flag at
`+0x62` is set and the final glyph's `+0x04` byte is **less than** its `cellWidth`, the measure
pass extends the pen by the difference:

```c
if (flagAt0x62 && lastGlyph && lastGlyph[+0x04] < lastGlyph[+0x02])
    penX += (lastGlyph[+0x02] - lastGlyph[+0x04]) * scaleX;
```

The field is the glyph's **advance width** — the authored horizontal step, in texels —
settled by the shipped data (§7 `UQ-364`): it scales monotonically with the glyph's drawn width
(`i`/`l` = 4, `k`/`n`/`x` = 6, `o` = 7, `m`/`w` = 10, `M` = 12, `W` = 13 in the US `fs` pack),
where a bearing would anti-correlate — the narrowest glyphs would carry the *largest* side gaps.
So the correction reads `penX += cellWidth − advanceWidth`: when `+0x62` is set the last glyph is
measured by its full cell rather than by its advance — the authored trailing slack is counted into
the line's width. The remaining refinement — whether `+0x04` is the pen-step advance or the ink
width used as one — is unseparated; both are "advance-class" and a *bearing* is eliminated.

### The glyph cache node

```
GlyphCacheNode
  +0x00  ptr   next               LRU list, head at [022CBE00 + 0x230]
  +0x08  ptr   prev               free/tail at [022CBE00 + 0x228]
  +0x10  u16   characterCode
  +0x12  u8    fontId
  +0x13  u8    resident
  +0x14  u8    texWidth           cellWidth rounded up to a power of two
  +0x15  u8    texHeight
  +0x18  ptr   pixels
  +0x20  ptr   glyphTableRecord
```

### The cache-fill rounding

```c
// 00364210, applied independently to cellWidth and cellHeight
if      (dim <  9)  pow2 = 8;
else if (dim < 17)  pow2 = 16;
else if (dim < 33)  pow2 = 32;
else if (dim < 65)  pow2 = 64;
else                pow2 = 128;
```

### The texture coordinates

Texture coordinates are 12.4 fixed point, so a texel is 16 units. The glyph cell is sampled
**half a texel inside its own edges** at both ends, which is the correction that stops one
glyph bleeding into the next in the font sheet:

```c
U_min = V_min = 8;                                // 0.5 texel * 16
U_max = (int)((cellWidth  + 0.0f + 0.5f) * 16.0f);
V_max = (int)((cellHeight + 0.0f + 0.5f) * 16.0f);

// the four coordinate payloads, in emission order
//   TL: (V_min << 16) | U_min      == 0x00080008
//   BL: (V_max << 16) | U_min
//   TR: (V_min << 16) | U_max
//   BR: (V_max << 16) | U_max
```

### The four corners, before projection

```c
penX' = penX * masterScale;
penY' = (penY + yOffset) * masterScale;
w     = (widthOverride  ? widthOverride  : glyphWidth ) * masterScale;
h     = (heightOverride ? heightOverride : glyphHeight) * masterScale;

TL = ( penX',                 penY',                 0, 1.0f );
BL = ( penX',                 penY' + h * scaleY,    0, 1.0f );
TR = ( penX' + w * scaleX,    penY',                 0, 1.0f );
BR = ( penX' + w * scaleX,    penY' + h * scaleY,    0, 1.0f );

if (rotation != 0.0f)
    for (c in {TL, BL, TR, BR})
        c = Vec3TransformByMatrix(c, sharedMatrix_022CBE00_plus_0x1E0);

projectCallback(&packed[4], &TL);      // -> four packed screen positions   <- answered 2026-10-02, OPUS: no callback - a direct call of the empty 0016D6A0 (ret 0) at 003649A0+0x5D8 (UQ-365)
```

### The filter bit

```c
needsFiltering = (masterScale != 1.0f);
if (!needsFiltering)
    needsFiltering = (scaleX != 1.0f) || (scaleY != 1.0f);

filterPayload = needsFiltering ? 0x20 : 0x00;      // bit 5
```

### The pen advance

```c
// per drawn character
penX += advanceWidth(glyph) * scaleX;

// control code 1 — the figure space
penX += advanceWidth(glyphFor('0')) * scaleX;

// {s sx sy}
scaleX = sx / 100.0f;
scaleY = (sy != 0) ? sy / 100.0f : 1.0f;

// {a} alignment, against boxWidth at +0x5C
penX = boxWidth - measuredWidth;            // {a 1}  right
penX = (boxWidth - measuredWidth) / 2;      // {a 2}  centre
```

### The window colour modulate

```c
// 0053E0B0 and 002D8690, per channel
out = (channel * intensity) >> 7;           // 0x80 == 1.0
```

### The draw gate

Nothing is drawn at all unless the font's slot bit is set in a global mask:

```c
if (((*(uint *)(022CBE00 + 0x240) >> (fontId & 0x1F)) & 1) == 0)
        -> return, drawing nothing
```

### The subpacket length patch

After the glyph's records are written, the subpacket header is patched with the record count:

```c
records = ((writePtr - subpacketStart) >> 4) - 1;
header.payload = records | 0x10000000;
header.code    = (records == 0) ? 0 : ((records << 32) | 0x5000000011000000);
```

and the buffer is submitted and swapped whenever it exceeds `0x180` records.

---

## 5. Call chain

```
message / menu / HUD text request
  -> 0053E0B0  scrolled window line loop            (GN161: ScrolledWindowLineCullShadowAndGlyphRunDispatch)
     -> 002D8690 / 002D87D0  renderer selection   <- corrected 2026-10-02, OPUS: 0053E0B0 calls neither; it calls 003659F0 then 003649A0 twice (0053E0B0+0x159/+0x181 and +0x1B2/+0x1D6), without the ex test
        -> 00364980   "ex" prefix?  no  -> 002B0280  (the byte-charset renderer)
        -> 003649A0   yes -> glyph-run emitter over UTF-16 units  (GN161: GlyphRunTexturedQuadEmissionAndPenAdvance)
           -> 003647E0   control codes and '{'
              -> 00366110   {tag} interpreter          (GN161: BraceTagMarkupInterpreterAndTextStateMutation)
                 -> 003656A0  measure, for {a}
                 -> 00203170 + 00366690 + 00202F70  build the {r} matrix
           -> 00365FD0   glyph cache hit
           -> 00364210   glyph cache miss + fill
           -> 003666E0   log2 for the texture descriptor
           -> 00474650   upload glyph pixels to graphics local memory 0x3440
           -> 00202B90   rotate the four corners
           -> RenderCommand_BeginSubpacket / FinalizeSubpacket
           -> RenderCommand_SubmitCurrentBufferAndSwap
           -> 0017F850   close the scope named "display : draw Font"

  -> 00364530   measure-only walk, no drawing        (GN161: NonDrawingGlyphRunAdvanceAndExtentMeasurement)
```

*Corrected 2026-09-25 (FABLE, Claude Opus 5.5).* Until this date the two selection lines above read "`ex` prefix? yes → `002B0280`" and "no → glyph-run emitter". **The code branches the other way.** At `002D8720`, `00364980`'s result feeds `je 002D8752`. A zero (not `ex`) jumps to the arm that calls `002B0280` (`002D8791`), and a one falls through to `003649A0` (`002D873C` / `002D874B`). `002D87D0` is the same (`002D8860`, `002D88D1`), and `00243860` jumps *over* `002B3400` and `002B0280` when the string is `ex` (`00243AAA` `jne 00243B8F`). The emitter this section describes is the `ex` path, so everything below it describes how `ex` strings are drawn.

**Upstream (who causes this):** `0053E0B0` is entered from a window-drawing pass; its own
caller is outside what this block read. `002D8690`/`002D87D0` are the selection layer directly
above the renderer. Both are the *trigger*, not an owner transition — they hand over an already
built `TextState` and do not own it.

**Downstream (what this causes):** command records in the shared render command buffer, and
glyph pixel uploads into graphics local memory. The **owner transition** is at
`RenderCommand_BeginSubpacket`: past that point the render command buffer owns the work.

**Do not confuse with:**

- **`002B0280`, the other renderer.** Reached from the same two selection functions when the
  record is ~~`ex`-prefixed~~ **not `ex`-prefixed** (polarity corrected 2026-09-25, FABLE, Claude Opus 5.5; see UQ-361). It is 6,441 B, already classified `Presentation.Rendering.*`, and it
  *also* closes the `"display : draw Font"` scope. Two renderers, one scope name.
- **[numeric formatting and character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md).**
  That system turns a *number* into characters and maps them through a translation table. It
  ends where this one begins. It does not measure or draw; §2 here supplies the piece it
  recorded as missing.
- **The glyph cache is not a texture cache.** It caches *which* glyphs are resident in graphics
  local memory; the texture-memory budget itself is a different system, documented at
  [texture mip local memory budget](../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md).
- **`003666E0` is not a general log2.** It is a bit-run scan that returns the right answer only
  for powers of two, which is all it is ever given.

---

## 6. Modding notes

- **Best intervention point for restyling text: the authored markup, not the code.** Colour,
  size, alignment, position, font and palette are all reachable from `{c}`, `{s}`, `{a}`, `{n}`,
  `{v}`, `{h}`, `{k}` and `{p}` inside the message data. Changing a `{s 100 100}` to
  `{s 120 120}` is a data edit; patching `003649A0` to scale is not, and will fight the
  measure pass.
- **`{s}` is in whole percent.** There is no fractional precision below 1 %. A "1.5× " scale is
  `{s 150 100}`.
- **Alignment needs the measure pass to agree with the draw pass.** `{a}` calls a measurement
  routine and then sets the pen; if you change advance widths in the font table without
  changing them for the measure path, aligned text will land wrong. `00364530` and `003649A0`
  read the *same* glyph table, so editing the table is safe; editing one code path is not.
- **Regenerates itself — do not write directly:** `penX`/`penY` (`+0x38`/`+0x3C`) are rebuilt
  from the string on every pass; the `needsFiltering` flag at `+0x56` is derived from the three
  scale fields; the glyph cache list is rebuilt on demand. Set the scales and let the flag
  follow.
- **Breaks if:** the font slot bit in `[022CBE00 + 0x240]` is clear — the whole call returns
  having drawn nothing, silently. A "my text disappeared" bug will look like a data problem and
  be this bit.
- **Breaks if:** a glyph's cell exceeds 128 texels in either dimension. The power-of-two ladder
  in `00364210` has no rung above 128 and clamps there, so an oversized glyph will sample the
  wrong region rather than fail loudly. This is the practical ceiling on a replacement font.
- **Breaks if:** you add a `{tag}` letter. Unknown letters fall to a shared do-nothing target,
  so a new tag is *silently ignored*, not an error — and its argument bytes are then read as
  characters, which will corrupt the rest of the line.
- **Multiplayer / XIIOnline:** none of this is authoritative world state. A `TextState` is
  per-draw scratch and the command records are per-frame. Text rendering is purely local
  derived state and never needs replication.
- **Mod compatibility:** the font glyph table (`[022CBE00 + 0x10 + fontId*8]`) and the glyph
  pixel blob (`+0x110 + fontId*8`) are authored data two mods may legitimately both want. The
  12-byte record layout in §4 is the contract between them.

---

## 7. What is not known

- [x] **UQ-361.** **Which strings are `ex`-prefixed, and what `002B0280` does differently.**
      `00364980` proves a two-renderer split exists and how it is selected; nothing here says
      what distinguishes the two populations. **PROPOSED-repos9e-1.**
      **PARTIAL 2026-09-15 (FABLE) — the population is not in the image, which is why looking for it
      there has not worked.** Found while tracing the drawer kind byte, in a caller this row had not
      looked at. **`002D89E0` is an eleventh instance of the split**, and it adds a fact the row did
      not have: **the two arms differ by more than renderer.**

      | `00364980(str)` | what runs |
      |---|---|
      | **1** — `str[0] == 'e'` and `str[1] == 'x'` | `003659F0` builds the state, then `002DD5D0` |
      | **0** | **`002B3400`** — which stamps the drawer **kind 2** — then `002DD680` |

      So the non-`ex` arm also **selects a drawer kind**, and the split is *two renderers and a kind*,
      not two renderers. (`002B3400` and kind 2 are read on
      [numeric formatting and character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md),
      §7.)

      **And the string being tested is authored text.** In this instance the caller is `002A1B00`, and
      the bytes `00364980` reads never existed as a literal: `002A1BD9` takes the buffer at
      `[window + 0x3E0]`, `002A1BD3` takes the index `[window + 0x154]`, `002B2D90` walks to a slice,
      and `00861EBA` copies that slice into the scratch buffer `0209CB90`, which is what
      `002A1CCA` hands on as `r9`. **The first two bytes `00364980` compares are the first two bytes
      of a run of the game's own message text.** So the population this row asks for lives in the text
      data and not in `.rdata`, and a string search over the image cannot enumerate it — the same
      shape as the composed key names on the cutscene-sidecar page, where the search was evidence
      about the search.

      **And this is a census, not one instance.** The last write to `rcx` was tracked at **all twelve
      call sites** of `00364980`, across its eleven callers: `00243860`, `002D66D0`, `002D7A90`,
      `002D8690`, `002D87D0`, `002D8910`, `002D89E0`, `002D8B00`, `003937C0`, `00407450` and
      `00407720` (twice). **Not one of them passes a literal** — every argument is a runtime pointer
      (`mov rcx, rax` / `r8` / `r9`, or a field load), and the single unresolved site, `002D7ACD`, has
      no `rcx` write in its own body at all. Two of them are worth naming because they corroborate the
      field: `002D8720` and `002D8860` load `[r9 + 0x28]`, and **`+0x28` is the text state's string
      field** — the same offset `002B3C30` and `002B3400` write from their second argument. So the
      `ex` test reads the string a text state carries, and that string is never a compile-time
      constant at any site.

      ~~**Still open, and narrowed rather than answered:** *which* authored runs begin `ex`, and what
      `002B0280` does differently. What is settled is where to look and why the image search fails.~~

      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): an `ex` string is `ex00` followed by UTF-16LE text, and the
      question's premise was inverted: `002B0280` draws the strings that are NOT `ex`.**
      - **The population, from the shipped text.** Every st2e string table embedded in any file under a `us`
        directory of `ps2data` was read: 28 blocks with a valid row table, 7,081 rows. Of those, 1,628 rows begin
        with the four bytes
        `65 78 30 30`, ASCII `ex00`. They sit in four files:
        - `menu04.bin`, all 1,024 rows: the staff-credit names ("Hiroshi Minagawa", "Akihiko Yoshida" …);
        - `menu03.bin`, all 512 rows: the staff-credit roles ("Directors", "Main Character Design" …);
        - `menu_expansion.bin`, 88 of 303 rows: labels such as "HP", "MP", "TIME", "COMBAT LOG" and "TARGET INFO";
        - `menu_command_template.bin`, 4 of 457 rows: `{…}` format templates.

        After the prefix each row is UTF-16LE up to a zero unit. Read as zero-terminated bytes, a row therefore
        stops after `ex00` and one letter, because the next byte is that letter's zero high half. 519 of the rows are empty (just the prefix).
      - **Controls.** A raw scan of the same directory for `ex00` followed by one printable UTF-16 unit finds 1,109
        hits, exactly the non-empty rows (784 + 247 + 74 + 4). The same scan over all 2,261 files of
        `plan_master/us`, the map scripts, finds none.
      - **What the `ex` arm does differently.** `003649A0`, the `ex` arm's emitter, starts at the string pointer
        plus 4, past `ex00` (`00364AE2`–`00364AE6`). It assembles each character as `byte[1] << 8 | byte[0]`
        and stops at a zero unit (`00364AEF`–`00364AFD`), steps 2 bytes per unit (`00364B68`–`00364B88`), and
        looks the unit up through `00365FD0`. The
        byte path, `002B0280`, reads one byte at a time: a byte at or above `0x20` is glyph byte − `0x20`; a lower
        byte selects a page through a 16-entry table and combines with the next byte (`002B0564`–`002B05CB`).
        So the split is **UTF-16 text versus the game's own byte charset**, plus the drawer kind 2 that `002B3400`
        stamps on the byte arm.
      - **The census of the arms.** All twelve call sites of `00364980` were followed; three have no conditional
        after the test. Wherever an arm reaches a renderer, `ex` reaches the UTF-16 side (`003649A0`, or `003659F0`
        + `002DD5D0`) and not-`ex` the byte side (`002B0280`, or `002B3400` + `002DD680`). No site sends `ex` to
        `002B0280`.

      *Not established:* the other eight languages' files (only `us` was read); which runtime-composed strings
      carry the prefix (this page's `0053E0B0` calls `003649A0` without the test, and it would need them to); and any
      live observation. The evidence is a static reading plus a shipped-data census.
- [x] ~~**UQ-362.** **The shadow offsets in `0053E0B0`.** The second draw pass takes `(dx, dy)` from a table
      at `caller+0xCE + kind*8` as signed bytes. The mechanism is established; the values are
      runtime data this pass did not observe, so "drop shadow" is inferred from the shape.~~
      **ANSWERED 2026-09-14 (FABLE): they are set in code, `(+2, +2)` for all three line kinds.**
      - **Where the table lives.** `0053E0B0` is called with the widget by its procedure `0053E380` (message 4,
        `0053E44B`; installed by `0053ED10`). The table is in the widget's private area past the `0xC0` base
        ([the widget object](../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md)).
      - **The init path writes it.** On message 1, after allocating and clearing its 64 KB line buffer (stored at
        `+0xC0`, `0053E506`–`0053E51D`), the procedure writes word `0x0202` at `+0xCE`, `+0xD6` and
        `+0xDE`: byte pairs `(2, 2)` for kinds 0, 1 and 2. Each is followed by `1.0f` at `+0xD0`, `+0xD8` and
        `+0xE0` (`0053E527`–`0053E559`).
      - **The draw pass uses it.** It adds `dx` to the line's x (`[rsi − 0xA]`) and `dy` to the running y
        (`0053E1C7`–`0053E1ED`).

      So the shadow is a 2-pixel offset down and to the right, the classic drop shadow. **Not established:**
      whether an owner rewrites the pairs through the widget pointer after init. No write exists in the procedure,
      its draw pass or `0053E640` (interior read 2026-09-17, SWE2-FRONTIER: 1,251 B, single `0035B730` call at [`0053E7CA`](../../_index/ADDRESS-INDEX.md)). An image-wide census at these displacements finds 2,719 writes, which cannot be
      attributed to this widget type without type tracking. What the `1.0f` beside each pair scales is also not
      read.
      **PROPOSED-repos9e-2.**
- [x] **UQ-363.** **The `{i}` icon payload.** **ANSWERED 2026-09-27 (FABLE, propagated by
      SWE2-CONTRACT): the three bytes have no reader in this build — the kind-`>=3` record they
      feed is built from script-verb arguments, not from the tag.** The tag body encoding stands:
      `{` is a `u16` `0x007B`, bodies are `{letter:1B, args:nB}` closed by a `u16` `0x007D`.
      The `{i}` arm `0036618D` (letter table `00366638`) reads `u16[rdx]` for the shared no-args
      test and otherwise only advances the cursor (`[rsi] = tag + 3` at `003661A9`) — it stores
      **nothing**, so the tag's `{u16, u8}` bytes index nothing anywhere found. The kind-3
      record path is fully read: `rec+0x00` is the image object `[02CA8A88]`, created in
      `0053EB90` from the resource named **`sf_logo_c`** — the records are **staff-roll logo
      images**, not text icons. `rec+0x0C` (the u16 icon index added to the group base) is
      written by the staff-roll builder `0053F0D0`'s op-6 arm (`0053F218`, = its third argument),
      reached from script verb route `00511A40` (pop int via `00267E10`, op 6, tail-jump) — not
      from the `{i}` tag's `u16`. The group selector is the sheet header's own `u16` at `+0x14`
      self-indexed — draw arm `0053E29C`/`0053E2A7`, builder `0053F22D`/`0053F232` — so
      `finalIndex = u16[hdr + 0x14 + 2*u16[hdr + 0x14]] + rec+0x0C`, and the tag's third byte
      selects nothing. Each entry is `{u16 texX, u16 texY, u32{lo12 w, hi12 h}}` texel rect
      drawn at `{i16 rec+0x0E, lineY}` by `002D8C80`, bracketed by `002D8BB0(1)`/`(0)`.
      Evidence record: `_index/candidates/uq363-icon-record-writer/uq363_icon_record.py`
      (5 checks, 0 FAILS). The earlier wording claiming `rec+0x0C` receives the tag's `u16`
      and that the line builder was unread is **corrected**.

      **2026-09-24 update — the compiled form is now read (`002AC2F0`, the shared object
      resolver):** in the compiled stream every object reference is either `byte >= 0x20` →
      index `byte − 0x20` (one byte) or `byte 0x10–0x1F` → index `base[class] + byte2 − 0x20`
      (two bytes), where `class` is the low nibble and `base[]` is one of two 16-entry u32
      tables at `00916570`/`009165B0` (context flag `dword[rdi+0x44] & 0x800` selects between
      them — both are banks of `0xE0` entries). `002AC2F0` returns that index in `eax`, stores
      the resolved object row `obj+esi*8` to the shared emit slot, and accumulates the
      object's advance into `ctx`.
- [x] **UQ-364.** **Byte `+0x04` of the glyph table record — advance width, or bearing?**
      **ANSWERED 2026-09-24 (SWE2-CONTRACT): the advance width.** The records are shipped data —
      `00366080` fixes the `022CBE00` layer's `+0x10 + fontId*8` table pointers into a kind-7
      resource blob (`s16` font count, rel32 offsets → `{count@+0x04, records@+0x10}`), and the
      blob's own bytes settle it: in `ps2data/image/ff12/myoshiok/us/packfiles/fontpack_fs.bin`
      the field reads `i`/`l` = 4, `j` = 5, `k`/`n`/`x` = 6, `o`/`p`/`s`/`u`/`y`/`z` = 7,
      `m`/`w` = 10, `M` = 12, `W` = 13 — tracking the glyph's drawn width where any bearing must
      anti-correlate. All 57 letter records have `+0x04 < cellWidth`, matching the guard's normal
      case. What the correction computes is therefore `cellWidth − advance` — the last glyph's
      trailing slack, counted only when `+0x62` is set. Bytes `+0x05`–`+0x07` remain unread by any
      function here. Residual: advance-width vs ink-width is not separated (both are
      advance-class; bearing is eliminated).
- [x] **UQ-365.** **The projection callback at `TextState+0x20`.** Its four-corners-in, four-packed-out
      contract is established from the call site; no implementation was read. **PROPOSED-repos9e-5.**
      **ANSWERED 2026-09-18 (FABLE): there is no callback. `TextState + 0x20` is a pointer to a 4x4 matrix, and the call it seemed to be the target of is a direct call to an empty function.** The field is loaded three times in the draw pass `003649A0` and never called through: twice it is the argument of `0017FB00` (`00364A5D`, `0036513D`), which copies 64 bytes from it and hands them to the draw layer's matrix setter, and once it is loaded into `rdx` (`00364F5E`) as the **second argument** of `call 0016D6A0` at `00364F78`, whose five arguments are `(out at rbp+0x70, the matrix, in at rbp+0x30, 4, 0)`. `0016D6A0` is the three-byte `ret 0` that identical-code folding merged every empty body onto (5,056 direct call sites in the image); the disassembly shows no indirect call anywhere in `003649A0`, `00364530`, `003647E0` or `00366110`. So the *four-corners-in, four-packed-out* contract read from the call site is the signature of a points-through-a-matrix routine **whose PC body is empty**: it writes nothing, and the decompiler fused its matrix argument with the call. Its argument order matches the PS2 library's transform-to-packed-screen-coordinates routine, which is an inference from the shape and is not needed for the answer. Static.
- [x] ~~**What `002AC5F0`, `002AAE40` and `002AF960` draw.**~~ **WITHDRAWN 2026-09-03 — the question
      could not be answered because its premise was wrong, twice.**

      **~~None of the three draws.~~** ~~The glyph emitter is `002A9F00`, which is not among them.~~ *(corrected 2026-10-02, OPUS: `002AAE40` draws: it calls the painter begin `0017FA10` at `002AAE40`+0x52C and the per-glyph draw `0017F7C0` at +0x66E, as `002A9F00` does)* And the
      three are **not peers**: `002AAE40` calls `002AC5F0` (`002AB5B0`), so the question asked about
      a function and one of its own callers as if they were alternatives. Sharing the
      `"display : draw Font"` scope made them look like siblings; **a profiler scope groups a call
      tree, not a set of equals.**

      What each is, now that all three are read:

      | | |
      |---|---|
      | `002AF960` | **opens and closes a run** — zeroes the batch counter, sets the `+0x10E4` budget, brackets with two `RenderCommand_SubmitCurrentBufferAndSwap` |
      | `002AAE40` | **a drawing pass** — sets the per-glyph gradient via `0017FC90`, then walks the string through the interpreter |
      | `002AC5F0` | **the control-code interpreter** — see [`../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md`](../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md) |

      > **An open question can encode a wrong structural assumption, and then no answer to it is
      > right.** This one asked "which text is each responsible for", which presumes a partition that
      > does not exist. **Three readings all came back not-quite-fitting before the premise was
      > checked instead of the answers.**

- [x] **UQ-366.** **Replacing it: what divides `002AAE40` from `002A8C50`, `002AF340`, `002B1FB0` and
      `002B5730`** — ~~the other four callers~~ four of the six other callers *(corrected 2026-10-02, OPUS: `002AC5F0` has seven calling functions; `002A9F00` and `002B2150` are the two not named here)* of the interpreter. **That is the question the original
      was reaching for**, asked about functions that really are peers, since all five sit at the same
      level of the call tree.
      **PARTIAL 2026-09-15 (FABLE) — the five are not reached the same way, and that is the first
      division.** Two are entries in a dispatch table and three are ordinary functions:

      | function | `rel32` callers | every other reference to it in the image |
      |---|---:|---|
      | `002A8C50` | **0** | one quadword at `009164C8` and one at `009164E0` — **slot 1**, kinds 0 and 1 |
      | `002AAE40` | **0** | one quadword at `00916518` — **slot 2**, kind 3 |
      | `002AF340` | 6 | none |
      | `002B1FB0` | 7 | none |
      | `002B5730` | 1 | none |

      The table is the three-wide, four-group drawer table at `009164C0` decoded on
      [numeric formatting and character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md),
      §7; the reference counts are a whole-image 8- and 4-byte pointer search cross-checked against
      `work/graph/imagebase_refs.tsv`, which lists none of the four. **So what divides `002A8C50` from
      `002AAE40` is *slot*** — two of the three roles in one group, read by different dispatchers off the
      same kind byte (`002ABEC0` / `002ABF20` take slot 1, `002AF960` takes slot 2). **`002AAE40` is
      divided again by *kind*:** it is the only non-null entry in group 3, so it runs only once
      `002A4830` has stamped the state, which happens only in the message window's case-4 update.

      **The three ordinary callers divide too, and by role rather than by route.** Each was read at its
      interpreter call site and at its return:

      | function | size | what it does with the interpreter |
      |---|---:|---|
      | `002B1FB0` | 246 B | **measures one token.** Builds a throwaway `0xD0`-byte state on the stack (`00861EC0` zero-fill, then the defaults `0x80808080`, three `1.0f`, `0x1E`, `0x25`, `0xFF`, `8`), peeks the first byte, sends `> 0x0F` to `002AC2F0` and the rest to `002AC5F0`, and returns `[rsp+0x28] - rcx` — **bytes consumed**. Nothing survives the return. |
      | `002B5730` | 383 B | **truncates a string to a byte budget on token boundaries.** Same measure step in a loop, accumulating `r14d = consumed + written` and stopping at `jge [rsp+0x24]`, the capacity; each token is `memcpy`ed (`00861EBA`) into the destination and the result NUL-terminated, with byte `2` ending it early. Returns **bytes written**. |
      | `002AF340` | 1,563 B | **a full pass over a real state.** The state arrives from the caller and is `movups`-copied in at entry; it calls the shared glyph-run emitters `0017F940` / `0017FAE0` / `0017F8C0`, of the `0017F7C0`–`0017FD30` family documented in [the font painter's public API](the-font-painters-public-api.md), plus the image-pointer fixup `0020E600`, goes through the cluster hub `002B2150`, and runs the interpreter once at `002AF783`. |

      **So the division is: two table-dispatched drawers separated by slot and kind, one per-token
      measurer, one budget-bounded truncator, and one stateful pass.**
      **What is still not established** is the inside of `002AAE40`, `002A8C50` and `002AF340` — the
      first two are characterised here by *how they are reached*, and `002AF340` by its entry, its
      callee set and its single interpreter call, not by a full read of 1,563 bytes. *(Narrowed 2026-09-30, FABLE, on SWE2-DATA's `measure_checks.py`, [`dd-data-3-0930`](../../_index/candidates/dd-data-3-0930/README.md): `002AF340` returns the number of characters laid out up to its stop string, or -1; `002ABB20`'s stop string `00916548` is `0F 23`, the `#` page-wait escape.)*

      **ANSWERED 2026-09-24 (SWE2-CONTRACT) — all three interiors are the same walk over one
      compiled line protocol, divided by pass role.** The input is not raw text: it is a
      *compiled* byte stream in which `0x00` ends, `0x02` is an inline marker, `0x03` is a line
      commit, `0x10`–`0x1F` are two-byte object references and `>= 0x20` one-byte object
      references, all resolved to object indices by `002AC2F0` (the `{i}` raw tag becomes one of
      these object bytes — that is the compiled form `UQ-363` points at). The three passes:

      | function | pass | what the same walk does there |
      |---|---|---|
      | `002AF340` | **measure** | `002AC2F0` per object → pen += its resolved width and `r12d` counts them (`bit31` of the metric row → `ctx+0x10FC` = 1/2); `002B2150` per text run → `{w,h}` out-params; `0x03` commits line metrics into the caller's extent struct — `+0x10` pen, `+0x14` line height, `+0x20`/`+0x30`/`+0x34` running maxima. Draws nothing. |
      | `002AAE40` | **emit** (kind 3) | `002AC2F0` per object → emits a `0x20`-byte descriptor pair **plus** a `0x40`-byte parameter record `{colour, pen, 1.0f scales, shadow flag}` into the draw queue whose write cursor lives at `020A2C50`; `ctx+0x10D4` counts queued items and `002B4730` flushes at `0x14`. Text runs go to `002AC5F0`; `0x03` runs `002B2150` + `002B1F20`. |
      | `002A8C50` | **draw** (slot 1, kinds 0/1) | Object bytes are only counted and skipped (`r14d` vs `word[+0x12]`/`+0x10` caps → flush); `002B2150` ~~draws~~ measures each text run *(corrected 2026-10-02, OPUS: it sums the width in `xmm6` and the maximum height in `xmm7` and stores them to its out-parameters at `002B2150`+0x315 and +0x32F; it never calls the glyph draw)*; `0x03` commits the working state into the *live element* — `+0x8A` cursor advance, `+0x90`/`+0x92`, `+0xB0` mode bits, `+0x54` — i.e. incremental/scroll-aware drawing. Bounded by a `0x2710` iteration cap and a caller-supplied stop byte (`r15b = dl`). |

      **So the full division is route x role:** the table slot chooses which pass runs
      (slot 1 = draw for kinds 0/1, slot 2 = emit for kind 3), `002AF340` is the caller-driven
      measure pass, and `002B1FB0`/`002B5730` remain the per-token measurer and the
      budget truncator. The compiled stream format and `002AC2F0`'s resolver are the shared
      machinery all three consume. Residual (the field-level detail of `002AAE40`'s descriptor
      packing, `002A8C50`'s flush modes `4`/`6`, and `002B1F20`) belongs to `UQ-367`;
      `002AC2F0` itself is now read — see `UQ-363`.

      **2026-09-24 companion reads — the rest of the stream family and where the stream comes
      from.** `002B2150` ("the hub") is a *scoped* pass, not a compiler: it snapshots
      `ctx+0x10C8`/`+0x10FC`/`+0x10FF`/`+0x10D8`/`+0x10E8` and a 16-byte block, sets
      `+0x10FF = 1` (inside-run flag) and `+0x10C8` = the caller's stop-word pointer, walks the
      stream accumulating `xmm6` (width) / `xmm7` (max height) into the caller's out-params, then
      restores everything — the RAII wrapper every pass calls per text run. `002B2970` is the
      same measure specialised to *one line* (`ctx+0x10C8` pointed at a local `3` — it stops at
      the `0x03` line break), wrapped by `002B2880`/`002B28B0` for line-height queries;
      `002B2930`/`002B28F0` are pure accessors — skip-to-line-`n` and count-lines-up-to-cursor.
      The byte stream therefore interleaves
      single-byte object refs (`>=0x10`) with `u16` text runs that `002AC5F0` interprets — the
      `u16` tag language lives *inside* the compiled stream's text segments.

      **2026-09-25 correction — `0209C700` is a page-history stack, not authored config.**
      (The previous package called `0209C708` a "config table of authored streams"; a complete
      accessor census reverses that.) The full accessor set for the BSS block: `002A3250` is
      the **only writer** — it snapshots the live element `window+0xD0` into
      `row = 0209C700 + depth*40`: `row+0x00` <- `elem+0x28` (the stream cursor mid-walk),
      `row+0x08` <- `elem+0x60` (resource), `row+0x10` <- the `0209C980` save-slot qword,
      `row+0x18` <- `elem+0x44` bit 11 (bank selector), `row+0x20` <- `elem+0xA6` (font),
      `row+0x22` <- `002B28F0(elem)+1` (lines through cursor), `row+0x24` <- summed per-line
      heights (each line measured via `002B2930`/`002B2880`, clamped to `>= 3*tick`), then
      `window+0x3C2` (stack depth) increments. The clears are `002A2720` and the `002A2FFC`
      teardown — both `memset(0209C700, 0, 0x280)` (16 rows x 40) gated on `window+0x3E8`
      bit `0x10000`, then `+0x3C2 = 0`. `002A5020` (scroll-to-line layout) and `002A5E06`
      (summing `row+0x22` into `window+0x3C1` = total lines) read it. So `002A4830` is the
      **pop/restore pass**: per stacked row it rebuilds one kind-3 element per line —
      `element+0x28` = `002B2930(row+0x00 snapshot, lineIndex)`, stamping `+0xA3 = 3`,
      `+0x8C = 0x7D00`, `+0x54` <- `row+0x1C`, `+0xA6` <- `row+0x20`, `+0x60` <- `row+0x08`,
      `+0x44` bit 11 <- `row+0x18`, restoring `row+0x10` to `0209C980` and replaying
      `row+0x24` into the y accumulator. The message-window proc `002A6190` is a 21-case
      jump table (`002A698C`); case 4 picks `002A4830` when `+0x3E8 & 0x700` (history exists)
      else `002A4430`. The authored-stream delivery question therefore moves upstream to
      `element+0x28`'s first writer — the message payload `window+0x38` (whose `+0x58`/`+0x5A`
      and `+0x90`–`+0x93` bytes scale the run's colour/size) — still `UQ-367`. The `+0x28`
      writers themselves are the kind constructors (`002B3400`, `002B3C30`, `002B3D50` each
      take the stream pointer as an argument), so authoring is upstream of construction.

      **2026-09-25 delivery chain — the delivered stream is a `00264D60` table entry of the
      current actor-manager slot block, and the producer boundary is walked end to end.**
      (2026-09-26 scope correction per FABLE: the `+0xA0`/`+0xA8` tables are *presumably* a
      loaded message resource, but their planter is unread — `0026C8C0`'s bind clears
      `+0xA0`/`+0xA8`/`+0xB0`/`+0xB8`/`+0x108` at `0026CC49`–`0026CC65`, and no planter of a
      non-zero value is yet cited. "Authored resource data" is the plausible reading, not
      yet the proven one.) `002A3250` has zero `call` sites — it is tail-called
      (`jmp`) only from `002A35B0`, which is called only from `002E1933` inside **`002E16B0` —
      the message-window opener** (`002E16DF`: `SetBank2048(actor+0x102, 1)` — `UQ-138`'s
      opener). `002E16B0(actor, slot=edx, stream=r8, resref=r9)` stores `r9`/`r8` into locals
      and forwards them unchanged; `002A35B0(window, resref, stream)` stores the resref to
      `window+0x1A8` (lazily re-resolved through `0039C480`) then tail-calls
      `002A3250(window, stream)`. `002A3250`'s own tail does the hand-off: it stores the new
      stream into the `0209C980` save slot, `002B39A0`'s it for the first `0x02` page
      separator, advances `r14` to `found+1`, then calls **`002B3D50(newElem, r14)`** — one of
      the three constructors that write `element+0x28` — and `002A3730` installs the element.
      So the first write of `+0x28` for a fresh page is the constructor argument, and the
      argument is a cursor **inside a message resource's compiled blob**.

      The resource side of that blob is `00264D60(obj, id)`: `obj+0xA0` is a table
      `{s32 count, u16 offsets[count]}` (`count = *table >> 2` — dword entries, of which the
      `u16` low half is used), `id &= 0xFFFFFF`, bounds-checked, and the return is
      `table + u16[table + id*4]` — a pointer **into** the resource blob = one compiled
      stream. `00264D90` is the identical accessor on `obj+0xA8` (a second section). The
      sibling `obj+0xB0` supplies the resref all three `002E16B0` call sites forward as `r9`
      (`00348EF8`/`0034AE91`/`0050EB57` — uniformly `[obj+0xB0]`). The callers: `00348EFF`
      and `0034AE98` are script-verb-side (a dense `002E1xxx` window-property block — flags,
      page capacity, colours — runs first, then the opener is called only when a zero test
      passes) and `0050EB67` is the UI/system path (`ebx = id & 0xFFFFFF` at `0050EB0B`;
      `r8 = 00264D60(obj, id)` result directly). **`002E16B0`'s `edx` is a window-slot
      index, not a message type** (corrected 2026-09-26 per FABLE, re-verified against the
      image): it is clamped to `0..7` (`min(esi,7)` `cmovg` pairs at `002E16FF`/`002E1827`/
      `002E18FD`, negative → 0) into the eight-entry, `0x68`-stride window-slot registry at
      **`0215F200`** (`lea` at `002E170C` and again at `002E1830`; a whole-`.text`
      rip-relative census finds zero references into `020BF200`–`020BF300` — the earlier
      "shared built-in page" reading was wrong). The one
      delivery call, `002A35B0` at `002E1933`, is reached only via the old
      `byte[rbx+0x40] == -1` test (`002E1811`) with `r8 = r13` — the *caller's* stream,
      unchanged. On the
      occupied-slot arm `r13` is merely reused as scratch for the slot-table base. So every
      stream delivered on the opener route is the caller's `00264D60` result; the
      "non-resource stream" exception does not exist.

      **What this resolves and what stays open.** `UQ-367`'s narrowed producer question is
      answered to the delivery boundary: the delivered stream is a message-table entry of
      the current actor-manager slot block — `00264D60(block, id)` returns
      `[block+0xA0] + u16[[block+0xA0] + (id & 0xFFFFFF)*4]`, or the shared empty string
      `01CEB638` when the table is absent or the id out of range — fetched by
      `id & 0xFFFFFF`, delivered via `002E16B0` → `002A35B0` → `002A3250` → constructor
      `002B3D50` → `element+0x28`. Page-history rows (`0209C700`) only ever snapshot that
      cursor — never author it. The `id`'s script-verb provenance and the
      `002B3400`/`002B3C30` caller questions are both closed in codas 4–7
      below (`id` = the 7th typed operand popped by `00267E10`; `002B3400`
      is the shared kind-2 constructor, `002B3C30` the non-default arm of
      `002B3D50`).

      **2026-09-26 coda — `obj` identified as the ambient actor-manager slot block.**
      `00264D60`'s first argument is not threaded down from the verb — it is `[02099D70]`,
      read through `002640C0()`, which EF-3 (the calling-convention page) names the
      **current actor-manager slot block**; the `+0xA0`/`+0xA8`/`+0xB0` message-table
      fields live inside that block. `002640C0` has **140 call sites** across the
      `0034xxxx` verb family and the `0050xxxx` UI paths (every message verb reads the same
      slot). The slot is installed by `00264050(newBlock, mode)`: NULL falls back to
      the static default block `lea`'d at `02098E10` (block 0 of the
      `ActorManagerSlot` array), `mode >= 0` binds and calls
      `00358940`, `mode < 0` (the `00343340` site calls `00264050(NULL, -1)`) **restores the
      previous block** — a push/pop scope around each verb's work. Eight call sites install
      it (`0034336E`/`00343BCE`/`003440EE`/`00344765`/`00352FD8`/`00353808`/`00359DE5`/
      `00359F9F`), all inside the verb region — so the block (and with it the message
      tables) is bound per-operation, not once at load. `0039C480` (the `+0x1A8` resolver
      in `002A35B0`) is itself a `00254A10`-gated fallback returning `[02AEE840]` — the
      resource subsystem's current/fallback pointer. What remains genuinely open: which of
      the eight install sites delivers a block whose `+0xA0` tables are already planted
      (the planter/resource-kind question FABLE scoped) and the `id`'s provenance inside
      the verb arg stream.

      **2026-09-26 coda-2 — the planter is `00266AD0`, and the tables are INLINE in the
      block** (supersedes the "borrow/install" framing above and partially reverses the
      loaded-resource reading):

      - *Correction to the coda above:* `00264050` is a **borrow wrapper**, not an
        installer — it stores `arg`-or-default into `[02099D70]`, runs one call
        (`00358940` for `mode>=0`; the `003590D0`→`003588B0` cleanup pair for `mode<0`),
        then **restores the prior block** (`mov [02099D70], rbx` at `0026407E`/`0026409B`/
        `002640AA`). All eight call sites pass `(NULL, -1)` — every one borrows the
        *default* block `02098E10` for the cleanup pair and restores. No site installs a
        loaded block through it. The same save/set/use/restore shape appears at the
        direct `mov [02099D70], reg` stores (`0026C472`/`0026C48D`, `0026E077`/`0026E0B7`
        confirmed pairs — the latter borrows the default to fire message
        `0x3000000|entry` through `002E9A60`). The persistent writer is a subset of the
        ~29 direct stores, still unisolated.
      - **`00266AD0(block)` plants `+0xA0`/`+0xA8`/`+0xB8`/`+0xC0`** — an 8-way dispatch on
        `byte[block+3] & 0x1F` (jump table `00266BA4`, four distinct arms): kind 0 →
        `+0xB8`/`+0xC0` null, `+0xA0 = block+0x120`; kinds 1–2 → `+0xB8 = +0x120`,
        `+0xA0 = +0x1A0`; kinds 3–4 → `+0xB8 = +0x120`, `+0xA0 = +0x140`; kinds 5–7 →
        `+0xB8 = +0x120`, `+0xC0 = +0x350`, `+0xA0 = +0x4D8`. Common tail:
        `+0xA8 = +0xA0 + (0xC8 if byte[01E0E329 + kind*4] == 1 else 0xA0)` — the second
        table sits immediately after the first. **The message tables live inside the
        block's own storage**, in per-kind layouts — they are not pointers into a loaded
        blob, so "the stream is a resource-table entry" shrinks further to "the stream is
        content the block holds inline".
      - Callers of the planter: `002665A9`, `002694A9`, `002694F8`. The `002665A9` site
        iterates a block array (`rbx = [rdx + r10*8 + 8]`), reads `block+3` for the
        `01E0E329` config byte, calls `00266AD0` then `00266BD0` — a per-block
        layout/init pass.
      - `00266BD0` (the call after the planter) is *not* the filler — it is the per-kind
        flag setter: same `block+3 & 0x1F` dispatch (jump table `00266C30`), writing
        `block+0x1C` (`0`/`0x38`/`0x40`/`0x30004`/`0x34C85` per kind) and `+0x14` bit 7.
      - The `002665A9` caller's function is `00266530(parent, blockArray, index)` — a
        per-block init: `rbx = [blockArray+8 + index*8]`, planter + flag-setter + a
        dense field reset (`+0xEC`, `+0xF5`, `+0x118 = 0x3C0000`, flag bytes `+8`/`+9`/
        `+B`/`+C`/`+D`/`+E`/`+14`/`+15`). Construction only — the compiled-stream bytes
        are not written here.
      - **The persistent installer is `0026C8C0(slotIndex, payload, altPayload)`** —
        FABLE's `ActorManager_BindLoadedDefinitionPayload`. It computes
        `rdi = 02098E10 + slotIndex*0x288` — **`02098E10` is block 0 of a fixed
        8-slot array, stride `0x288`** — stores `[02099D70] = rdi` with *no*
        restore (the one persistent write; every other store site restores),
        plants `block+0x00 = payload` (the loaded definition blob), `block+0x28`
        = index, and clears `+0x244`–`+0x27C` + `+0x200` bit. `ecx == 0` (slot 0)
        additionally bulk-clears the array region `02099014`–`020997AC` and runs
        a ~12-call subsystem reset (`002EF350`, `0032F240`, two `00369760`/
        `0036D160`/`003697F0` triples, `00377440`/`00377480`-gated `0025A990`/
        `0025AA30`, `003ACA90(8)`, `00360110`, `002E24B0`, `003EC850`, `0036E3B0`,
        `0026FFA0`/`002700C0`/`002EC590`/`002EC5A0` each `(1)`). Its only caller
        is `0032F966` inside a three-way kind dispatch — selector `5`, `13`, `14`
        each pass a different **resolver-thunk function pointer** as `r8`
        (`00267930`/`00267BB0`/`00267C20`; each thunk does `ecx = 5`/`0xD`/`0xE`
        → `0036B200`/`0036C1D0` — the kind re-selected inside), `rdx` = the
        loaded payload, `ecx` = slot. `r8 == 0` in the bind falls back to a
        static default target (`lea` in `0026C8C0`'s tail).
      - Layout tension kept open, now sharper: the slot block's `+8` field is a
        `{u32 count, ptr[count]}` **sub-block array** — `00358940(block, idx)`
        bounds-checks `idx` against `[block+8]` and returns `ptrs[idx]`.
        `00264050(block, mode)` for `mode ≥ 0` is exactly that lookup wrapped in
        a scoped install (set arg-or-default → `00358940(block, mode)` →
        restore); for `mode < 0` it runs `003590D0()` on the ambient block then
        `003588B0(eax)` cleanup instead. All eight shipped call sites pass
        `(NULL, -1)` — the lookup arm is **dead at shipped call sites**, and
        the live arm is "borrow default → ambient cleanup → restore".
        `00266530` receives the same `{count, ptr[]}` array as its arg2 and runs
        the planter on each element. **Correction 2026-09-28:** those elements
        are `ActorStorageRecord`s (canonical name in the record field map —
        `00266530` = `ActorStorage_InitializeRecord`, `002679F0` =
        `ActorStorage_AllocateAndInitializeRecords`, `0026CE60` =
        `ActorSystem_InitializeManagerRuntime`, `00358940` =
        `ActorManager_GetRecordByOrdinal`, per-kind sizes `0x328`/`0x3A8`/
        `0x330`/`0x348`/`0x2D0`/`0x6E0`/`0x6E0`/`0x668` from the
        `ActorSequenceDescriptor` table `01E0C328`). The planter's `+0xA0`
        is the **record's** `slotsA0` — a different field from the **slot's**
        `+0xA0` that `00264D60` reads. `00264D60`'s `obj` is the
        `ActorManagerSlot` itself (`[02099D70]`), and its `+0xA0` is installed
        externally — see coda-3. The record/slot conflation in the earlier
        coda is retracted; the inline-pointer finding remains true *for the
        record's* `slotsA0`/`slotsA8`/`contextPtr` fields.
      - **coda-3 — `slot+0xA0`'s planter and the content writer, both closed.**
        `00264D60`'s `obj+0xA0` is written by setter `0026C880(slot, ptr)`
        (siblings `0026C860`→`+0xB0`, `0026C8A0`→`+0xA8`), called from
        `00330190(packedArg)` which unpacks `{ptr = arg & ~0xF, slot = arg & 0xF}`
        — a 16-aligned blob pointer tagged with its slot nibble — and also
        records it in a 16-entry global table (`[imagebase + 0x21A6CA0 + slot*8]`).
        `00330190`'s sole caller is `003304A0` — the **universal post-load
        section installer** run for every resource blob: `rdi = arg & ~0xF` is
        the blob, `dword[blob+4]` is a header-field-count gate (each section
        fires only when `count > N` **and** its offset dword is nonzero), and
        the header's section offsets (`+0x10` → `0032F850`, `+0x18` →
        `00330190`/slot+0xA0, `+0x1C` → `00330220`/slot+0xA8, `+0x28` →
        `00330060`, `+0x34` → `0032FAC0`-family, `+0x40` → presence flag bit9 in
        the `022C6E48[slot]` word) are each rebased `blob + offset`, OR'd with
        the request index (`arg & 0xF`, 0–15 — the same index space as the
        `ActorManagerSlot` array), and dispatched to a typed installer.
        `0032F850` (the `+0x10` installer) stores the section pointer into the
        per-request array `022C6C28[reqIdx]` — the pack's **script section**.
        `003304A0` runs two ways: as the async read-completion callback passed
        to `0032E620` for normal loads (`00330426`, stored at `rsp+0x40`), and
        inline for resource kind `0xD4` — the `003303B0` arm memcpy's
        (`00861EBA`, CRT import thunk) the staged blob `[022C6F10]` (size
        `dword[022C6D3C]`) into the request buffer instead of reading disk.
      - **coda-4 — kind `0xD4`'s file identity resolved, and it is NOT the
        message-table source.** `[022C6F10]` is staged once by `0032F430`
        (called at `00266DE6` inside the manager-init sequence): it sizes via
        `0032E400(8, 0x350)` and loads via `0032E620(8, buf, 0x350, size, 0)`
        the file **`PS2Data\plan_master\<lang>\event\pre_z\pre_z0000\
        pre_z0000.ebp`** — kind 8 id `0x350` in the resource-path tables,
        verified in all five embedded path arrays (`us/fr/de/it/es`) and in
        the shipped corpus: 3,840 bytes, byte-identical SHA256 across all 9
        locales. Its `EBP2` header has `dword@4 = 0x14` but only `+0x10`
        nonzero (`0x80`) — so `pre_z0000` contributes **only** the script
        section (`init` function, `"00/00 00:00"` format string, `iwabuchi`,
        `pre_z0000.src` symbols at blob+0x80) and **never plants
        `slot+0xA0`**. The `slot+0xA0` message table is the `+0x18` section of
        *other* packs — zone event `.ebp`s carry it (`alc_a0100.ebp`:
        `+0x18 = 0x2440` → `{u32, {u16 streamOffset, u16 flags}[]}`, streams
        verified compiled text). The earlier claim that kind `0xD4` supplies
        the message table is **corrected**: `0xD4` is the staged bootstrap
        pack's serve-from-memory escape; the message table arrives through
        the same installer path from whichever blob the slot loads.
      - **So the compiled-stream producer is the resource file itself:** the
        table `00264D60` reads is authored data in the `+0x18` section of the
        pack bound to the slot — bound check `id < dword[table] >> 2` with
        `id & 0xFFFFFF` (`00264D74`–`00264D85`), entry `i` at `table + i*4` =
        `{u16 streamOffset relative to table, u16 flags}`. The "inline tables
        in the block" reading is retracted — `block+0x120`+ regions are the
        *record's* interior (`movementContext`/`resourceEntryPool` per the
        field map), unrelated to the message table.
      - **`id` provenance closed** (`00348DF0` verb handler): the verb pops
        eight operands from the script's **typed value stack** via
        `00267E10(ctx)` — `dword[ctx]` = remaining count, `byte[ctx+4+i]` =
        per-arg tag (1 = s32 direct, 2 = f32 via `cvttss2si`), values at
        `ctx+0x184+i*4`, unknown tags fail closed through `008620C0`. The
        7th popped value is the `id` (script-authored, `& 0xFFFFFF` inside
        the accessor); the 8th is the window-slot index `002E16B0` clamps.
        The same `id` also feeds `002673A0(slot, id)` — a sibling accessor on
        the *same* `+0xA0` table returning `u16[table + id*4 + 2] & 1`, which
        refines the entry shape to **dword `{u16 streamOffset, u16 flags}`** —
        low half = blob offset `00264D60` follows, high half bit 0 = a
        **suppress flag**: `test ebx,ebx / jne 00348F04` at `00348EE0` skips
        the `002E16B0` opener call entirely when set.
      - **coda-5 — the EBP2 section vocabulary, censused over all 1,115 US
        `.ebp`s.** `003304A0` is a 20-slot directory walker — the canonical
        map is [the EBP2 container page](../../25-EBP-Script-Container/Container/ebp2-container.md)
        (15 offsets touched, 14 slots dispatched, `slotCount > n` bound,
        magic never validated; slots 1/5/7/13/15/18 wired to nothing, 17
        unused in the corpus). The shipped corpus names each populated slot
        by magic: `+0x10` slot 0 (1114 files) = the script blob
        (`0x8000000B`); `+0x18` slot 2 (828) = the `slot+0xA0` message table;
        `+0x1C` (359) = a **second** same-shape table → `slot+0xA8` (read by
        `00264D90`, `00264D60`'s mirror on `+0xA8`) — consumed by verb
        `0x179` **`fieldsignmesbyid`** (`0035714A`) and an object-field fetch
        (`00355A9F`, id = `word[obj+0xA]`): the pack's **field-sign /
        message-by-id strings**, distinct from the `+0xA0` dialog table;
        `+0x28` (67) = a `TIM2`
        texture → `slot+0xB0`; `+0x30` (423) = `CML1` → `0032FA10` → setter
        `0026CE00` → **`slot+0xD8`**; `+0x34`
        (423) = `CAM7` → `0032FAC0` → setter `0026CE20` → **`slot+0xE0`**
        (`022C6D58[req]` mirror + `002561C0` — which validates the `CAM7`
        magic before registering into the `02092800` table — and 4×
        `002566E0`); `+0x38` (113) = a second `CML1` → `00331610` →
        `0026D3A0` → **`slot+0xF0`**; `+0x3C` (113) = `SHK1` → `003316B0` →
        `0026D3C0` → **`slot+0xF8`**; `+0x40` (842) = a small-count
        table → `0032FB70` → `0026CE40` → **`slot+0x100`** + presence bit9.
        The slots my first census did not enumerate fill out the bundle:
        `+0x20` slot 4 (209) = **`NAVI`** navigation data → `00332100` →
        `003DFDC0`; `+0x48` slot 14 (140) = **`LGT2`** lighting → `00330110`
        → `022C6E20[req]` (skipped for manager 0 — the `.mpk` map pack
        supplies manager-0 lighting, BW-3); `+0x50` slot 16 (517) and
        `+0x5C` slot 19 (271) = **`FF12`**-magicked payloads → `003320E0` →
        `003DFE60(0)` and `003320D0` → `003EAA00` respectively; `+0x54`
        slot 17 = `00332110` → `003DFE60(1)` — same binder as 16, selector
        1, **0 files ship it**. `slotCount[+0x04]` = 20 in all 1,114 EBP2
        files; `+0x08`/`+0x0C` are always 0 and never read.
        Every install is OR'd with the
        request index and mirrored into a `022C6Cxx` per-request record.
        The setter stubs are all five-instruction `imul 0x288` writes onto
        `02098E10`, and this mapping matches FH-1's section-numbering
        narrowing exactly (sec 2→`+0xA0`, 3→`+0xA8`, 6→`+0xB0`, 8→`+0xD8`,
        9→`+0xE0`, 10→`+0xF0`, 11→`+0xF8`, 12→`+0x100`) — the producer
        (EBP2 header field → installer → setter → slot field) and consumer
        sides now agree on every section.
        Player-facing: **an event pack is a zone's whole cutscene bundle** —
        its script, up to two text tables, an optional event texture, and
        camera/shake animation data; `pre_z0000` ships only the script.
      - The `+0x18` issuer side is already censused on the actor-manager
        record page: `WorldSimulation_ProcessDeferredModeRequest`'s sites =
        slot 0 (`World_UpdateSimulationTick`), slot 1 (the `0xD4` startup
        request above), slot 3 (verb `0x0198` `summoneventread`, request id
        popped via `00267E10`), and script-supplied slots from verbs
        `0x00E7` `eventread` / `0x00E8` `eventread_e8` / debug `0x202D` —
        the `eventread` family is the path that loads a zone/event `.ebp`
        onto a slot and thereby plants its `+0x18` message table.
      - `entry.flags` vocabulary **closed by corpus census**: across every
        `+0x18`/`+0x1C` table in all US `.ebp`s the flag half is only ever
        `0` or `1` — bit 0 (suppress) is the sole authored flag; larger
        values in a naive walk are stream bytes past the entry array, not
        flags. `dword[table]` doubles as entry 0 `{off, flags}` — it carries
        `flags = 1` in most packs (a suppressed lead entry whose offset is
        the header+array span), which is why the `>>2` bound is permissive.
      - **coda-6 — the `+0x18`/`+0x1C` authoring split, closed by path
        census.** Of 1,115 US `.ebp`s, **769 are `plan_map/<zone>/<map>/
        global/<map>.ebp` map packs and 346 are `event/<zone>/<scene>`
        event packs** — 345 EBP2; `evt_t0020.ebp` is a bare `0x80000007`
        script blob with no EBP2 wrapper. `+0x1C` — the field-sign
        table `00264D90`/`fieldsignmesbyid` reads — is authored **only** in
        map globals: 359/769 carry it, **0/346 event packs ever do**. The
        split inside the globals: 328 carry both tables, 274 only `+0x18`,
        31 only `+0x1C`, 136 neither. `+0x18` — the `slot+0xA0` dialog table
        — rides both families (602 globals + 226 events = 828). `+0x28`
        TIM2 rides **mostly** globals (55 of 67; 12 event packs ship their
        own texture) — corrected 2026-09-27, an earlier line wrongly said
        all-event. The rest of the split: `+0x20` `NAVI` (209) and both
        `FF12` slots (`+0x50` = 517, `+0x5C` = 271) are **global-only** map
        fixtures; `+0x48` `LGT2` (140) is **event-only** — cutscene
        lighting. So the partition is **the pack family,
        not the content**: a map's sign text lives in its global pack and
        follows `fieldsignmesbyid`; event packs carry only their own dialog
        (`+0x18`), and a running event leaves `slot+0xA8` holding whatever
        the map global last installed (the installer only writes sections
        that exist — `003304A0` skips null offsets).
      - **coda-7 — `002B3400`'s 21 call sites, censused.** Signature is
        `(rcx = block, rdx = stream, r8 = resref-or-NULL)` —
        **the shared kind-2 byte-charset element constructor for the
        whole UI**; no caller is message-exclusive. `r8` is a resource
        reference (the same "resref" currency `002E16B0`'s `r9` carries),
        not a constant zero: `002B3400` forwards it through `rbx` to
        `0039BAD0`, which classifies it into the element's `+0xA6` kind
        byte; when that byte is 7 and `00254A10` passes, `+0x44 |= 0x800`
        and `0039C4A0` resolves a texture handle stored at `element+0x60`.
        The arg census: 16 sites `xor r8d,r8d` (NULL); five pass a real
        resource — **`002C8BC0` at `002C8D26` reads `[slot+0xB0]`, the
        EBP2 `+0x28` TIM2 section** (NULL when no slot is bound),
        `00243860` passes `0020E600(record+0x20)`'s resolved resource,
        `002D8910`/`002D89E0` forward their own stack arg-5, and
        `002C68A6` a saved local. 15 of the 19 enclosing bodies build on the shared
        text context `[01F44830]`; the other four init elements embedded in
        widget structs — `0027AD70` (`widget+0x1550`), `003EE420`/`003EE8C0`
        (`obj + idx*0x1E0 + 0x160`, indexed element arrays; `003EE8C0`'s is
        the lone `E9` tail), `0057C480` (`rsi+0xE0`, stream `rsi+0x1B0`). The
        message-window-side subset is six sites in four bodies: `002A86A0`
        (3 sites — the log-pane/message-window helper), `002BF230`,
        `002D8910`, `002D89E0` — the last two being `00364980` `ex`-split
        instances where `002B3400`+`002DD680` is the not-`ex` arm. The other
        15 sites spread across menu/widget text: battle-menu `0027AD70`,
        billboard emit `0028A090`, typed-list `00243860`, label-gate
        `002C64C0`, record-field `002C8BC0`, script-side dialog text
        `0035C160`, widget/frame paths `003EE420`/`003F7F50`, menu-selection
        `003EE8C0`, settings arm `003F9720`, map screens `004044D0` +
        destination-label `00550A00`, menu atlas `005528C0`/`005569F0`, and
        the confirm window `0057C480`. `002B3C30`'s callers are
        enumerated: it is the **non-default arm** of the `002B3D50` constructor — `test ebp,ebp` at
        `002B3350` dispatches mode≠0 → `002B3C30`, mode==0 → `002B3D50` (after
        `+0x44 |= 0x800` gating on `byte[+0xA6]==7` and a `0039C4A0` resolve
        into `+0x60`); its second caller `002A1C86` is a window re-render path
        that rebuilds an element and feeds `window+0x1A8` (the resref
        `002A35B0` stored) into `002D89E0`.

      **2026-09-25 companion reads.** `002B1F20` — the call beside `002B2150` in `002AAE40`'s
      `0x03` arm — is the **per-line horizontal-alignment resolver**: it switches on
      `element+0x9A` minus `0x25`, returning `+0x99` (left origin) for `0x25`,
      `+0x99 + (+0x94 − measuredWidth)/2` for `0x26` (centre) and `+0x99 + +0x94 − measuredWidth`
      for `0x27` (right edge), `xmm2` otherwise — `+0x94` is the line box width and `+0x99`
      the pen origin. So each committed line is aligned independently by `element+0x9A` —
      the element-level form of the `{a}` tag's centre/right argument. `002B39A0` is a plain
      `strchr` over the byte stream (the page-advance tail calls it `(r14, 2)` to hunt `0x02`
      markers) and `002B39D0` the substring find that pairs with it.
- [x] **UQ-367.** **The 147 residual functions this block did not read at all.** 138 bodies were extracted;
      27 were read; 153 of the 158 remain unresolved. **This is the category's standing
      question AC-1 and is not closed.** *(Ledger note 2026-09-14: the residual itself is now
      **30** — R109 classified ~~128~~ 109, and GN159 to GN161 128 in all *(corrected 2026-10-02, OPUS: `residual-109-classification.tsv` has 109 rows; 158 − 30 = 128)*, so the "not read at all" tail is correspondingly smaller; the
      153/158 figures record the block's own read coverage at its date.)*
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md. See the register row.* *(answered: see this pointer names this page; the residual population is carried by the-unresolved-158.md and its member TSVs; 2026-10-02, OPUS)*

---

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The stream is 16-bit text | complete body of `003647E0`: `U+0020` and `U+3000` both dispatched to the space-advance path | 1 |
| `{` opens a tag, `}` closes it | complete bodies of `003647E0` and `00366110` | 1 |
| Exactly eleven tags: `a c f h i k n p r s v` | raw 22-entry dword jump table at `00366638`, decoded from the EXE independently of the decompiler; agrees exactly | 1 |
| `{s}` is percent | `DAT_008F3134 = 100.0f` read from `.rdata` | 1 |
| Texture coordinates are 12.4 with a half-texel inset | `DAT_01CEBC84 = 16.0f`, `DAT_01CEBB70 = 0.5f` read from `.rdata`; the `0x00080008` first payload | 1 |
| The corner transform is a real matrix multiply | complete body of `00202B90`; `00203170` copies the 4×4 identity, verified as `[1,0,0,0][0,1,0,0][0,0,1,0][0,0,0,1]` from `.rdata` | 1 |
| Cell dimensions are rounded to powers of two and converted to log2 | complete bodies of `00364210` and `003666E0` | 1 |
| One quad per character, four vertices, strip | complete body of `003649A0`: four coordinate/position pairs, primitive word `0x154` | 1 |
| Filtering only when scaled | complete body of `003649A0`: `+0x56` flag drives payload `0x20` on code `0x14` | 1 |
| The renderer selector is `strncmp(record, "ex", 2)` | complete body of `00364980` | 1 |
| The operation is called "draw Font" | authored `.rdata` string `008C5B18`, sole code reference at `0017F854` inside `0017F850` | 2 |
| Four residual functions close that scope | call-graph edges into `0017F850`, 8 callers, cross-checked against the certified residual list | 8 + 11 |
| The `TextState` offsets are bytes, not indices | three decompilations with different pointer types (`float*`, `longlong`, `float*`) agree field for field | 1 |
| Body extents do not over-run | each of `003649A0`, `00366110`, `00364530`, `0053E0B0` ends in `C3` followed by `0xCC` padding to the next function; `00366110`'s 90-byte gap is its own jump table, exactly accounted | 1 |

### Superseded reading — "the residual has no authored strings" is an instrument artefact

Both this category's [README](../README.md) and
[the-unresolved-158](../the-unresolved-158.md) state, as a founding fact, that the 158 have
**zero** direct authored strings. The freshly regenerated `STRING_REFS.tsv` for this session
reproduces that zero. **The zero is wrong, and the reason is the scanner.**

`DumpUnresolvedStringReferences.java` walks each instruction and asks for
`instruction.getReferencesFrom()`, then `listing.getDataContaining(target)`, then whether that
`Data` object's value `instanceof String`. **The scan reports the contents of Ghidra's
database, not the contents of the binary** — and in this program the third condition is never
satisfied.

**Which link breaks, established rather than assumed.** References *do* exist: the certified
`DATAREF_CONTEXTS.tsv` for this session carries 378 rows derived from them, 16 of which are
real code references. What is absent is **defined string data**. Decompiling the two functions
that demonstrably reference strings shows every one of their string targets as undefined
`&DAT_00905988`, `&DAT_008FB2B4`, `&DAT_00D10F50` — never Ghidra's `s_…` form for a typed
string. Independently, the only `data_type` values in the whole certified dataref dump are
`PEx64_UnwindInfo`, `_IMAGE_RUNTIME_FUNCTION_ENTRY` and `IPToStateMapEntry[…]`: three exception
structures a prior session defined by hand, and nothing else. So the zero measures **which
bytes some earlier session happened to type**, not which functions reference strings.

> **Correction, 2026-09-02, same session.** This subsection first attributed the zero to
> `Import-GfzParent.ps1` importing with `-noanalysis`, and said Ghidra "never created references
> or typed string data." The second half holds; **the first half is false** — the packed parent
> carries prior analysis and its references are plainly present, which is why the dataref dump
> is not empty. `-noanalysis` prevents *re-*analysis on import, not all analysis ever. The
> corrected mechanism is narrower and does not depend on the import flag at all.
>
> A second slip is recorded because it nearly became evidence: a grep for `s_[A-Za-z0-9_.]+`
> appeared to find a defined string `s_ResolveRuntimePointer`, which would have proved string
> typing was merely patchy. It was a substring match inside the function name
> `ImageAddress_ResolveRuntimePointer`. **A regex without an anchor is not a search for
> symbols** — it was caught only because the "defined" string had no plausible reason to exist
> where it appeared.

Why the typing is absent is **not established** and is not guessed at here.

A byte-level scan of the executable — every RIP-relative `LEA` in `.text`, resolved against
every NUL-terminated printable run in `.rdata`/`.data`/`.rodata`, attributed to its owning
function by the certified body extents — gives a different answer:

```
population: the 158 certified-current residual functions (sha c5d4b7f7…)
instrument: 50,717 RIP-relative LEAs scanned; 8,611 string references in 3,312 functions
positive control 1: 0017F850 -> "display : draw Font"   PASS
positive control 2: 00378540 -> "MWeather"              PASS   (agrees with the Weather documents)

residual functions with a string reference of their own     :  2 / 158   (reported: 0)
residual functions with a string one call away              : 13 / 158   (never measured)
```

The two direct ones were verified byte for byte at instruction level, not merely counted:

| Residual fn | Body | Strings it references directly |
|---|---:|---|
| `0036A570` | 729 B | `"M2/l"` `"M2/U"` `"M2/L"` `"M /l"` `"M /U"` `"M /L"` `"FREE"` `"/I"` `"/C"` — a contiguous 8-byte-aligned label table at `00D10F40` |
| `0020AC30` | 572 B | `".json"` `"spc_"` `"sum_"` `"0001"` |

And one call deeper, eleven residual functions acquire a name:

| Residual fn | Body | Named by |
|---|---:|---|
| `002AC5F0` | 7489 B | `"display : draw Font"` |
| `003649A0` | 3020 B | `"display : draw Font"` |
| `002AAE40` | 2440 B | `"display : draw Font"` |
| `002AF960` | 1117 B | `"display : draw Font"` |
| `0018EEE0` | 1581 B | `ColorBuffer` `ColorBufferSampler` `apply_MainTex` `gamma` `resolution` `colorR/G/B` `percent` |
| `001E8070` | 1293 B | `fontclut_%d` |
| `001D72F0` | 937 B | `"display AutoSave Window"` |
| `001C2980` | 897 B | `"softEdges"`, `"Debug Info:"` |
| `0036A570` | 729 B | its own table, plus `"TkFreeMain:Allready Free:%p from %p"` neighbourhood |
| `0020AC30` | 572 B | `JsonData/CutScenes/`, `mDofFocusDistance`, `mDofApertureFnumber`, a `plan_master\…\event\` path regex |
| `0036A2A0` | 495 B | `"TkFreeMain:Allready Free:%p from %p"` |

**`001E8070` has since been opened** — see
[painting-a-line-of-text-into-a-render-target](painting-a-line-of-text-into-a-render-target.md).
It is the **vertex emitter**: six vertices per glyph (corners 0,1,2 then 1,2,3), `0x3C` bytes each,
UVs with V flipped, colours drawn from one of **28 `fontclut` palettes** selected by
`[glyph_record + 0x9C] % 0x1C` at `001E8297`–`001E82BB`. It also accumulates the screen-space
bounding box of the whole line, which is what lets the flush pick a render target. **The string
`fontclut_%d` named the palette correctly; what the function does with it needed the body.**

**Why this matters more than the four classifications.** `002AAE40` is the function
[the-unresolved-158 §11](../the-unresolved-158.md) called "the purest example in the database of
why a call-context classifier cannot touch these" — `002AAE40` has no caller, and all three of its data
references banned exception metadata. It is a font drawing function, and the evidence was one
call below where every scan was looking. `002AC5F0`, the largest unclassified function in the
game, is likewise. The cluster hypothesis that §11 killed and then reinstated was **right**, and
the reason it kept oscillating is that the decisive evidence sat at depth 1.

**Limits of the corrected instrument, stated so it is not over-trusted.** It finds only
`48 8D`/`4C 8D` RIP-relative `LEA` forms; it misses `mov reg, imm64`, references reached through
pointer tables, and 32-bit absolute forms. It requires a NUL-terminated printable run of at
least two characters. **2 and 13 are lower bounds, not counts.** A caller's ownership is still
not a callee's ownership, and none of these strings is being used to assign a `PrimaryOwner` —
they name the *operation*, which is what a `CodeDomain` describes.

### Method notes

- **Batch measurement, re-taken as the mission requires.** 80 functions decompiled in
  **10.7 s**, 80/80 ok, 0 fail, 0 miss, 432 KB. A second batch of 46 and a third of 12 both
  returned 100 %. Extraction is not the constraint; reading is. **138 bodies were extracted and
  27 were read.** Only the 27 are claimed.
- **The residual list was not reused.** `verify/residual_addrs.txt` from the prior session was
  diffed against this session's freshly regenerated `verify_GFZ_H9E/residual_addrs.txt`:
  identical, sha `c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff`.
- **The cluster instrument was positive-controlled** before being used to choose targets: run
  over the 158 it reproduces the independently recorded structure exactly — 14 clusters of two
  or more plus 109 singletons, largest cluster 13.
- **The switch was verified against the whole construct**, per the lesson recorded in
  the-unresolved-158 §12. The decompiled label set and the raw binary jump table were derived
  separately and compared; they agree on all eleven, and the table's 22-entry span rules out a
  twelfth hiding below a truncation.
- **A wrong intermediate is recorded rather than hidden.** The jump table was first parsed as
  MSVC's dword-plus-byte-index form, which produced index values of 243 and 216 — obvious
  nonsense that stopped the reading. The table is dwords only, 22 of them. The tell was that
  the derived numbers were impossible, not that the parse looked wrong; had the byte values
  happened to fall under 16 the mis-parse would have produced a plausible and entirely false
  case list.

---

## 10. Corrections, and a falsification pass this document still owes

**This section is not a falsification pass.** It records machine-found defects that the *author* of
this document confirmed and fixed. **A pass by the author is worth less than a pass by anyone else**,
and this document has not had one — the rule this project applied on 2026-09-03, when the author of
the Audio boundary document offered to attack it and was declined on exactly that ground. The four
functions documented here are also the four rows of batch A, so an audit of this evidence by the
person who produced it is the weakest available check on a mutation.

**~~Still owed: a first falsification pass, by a session that did not write this.~~** *(answered: see "Falsification pass 1 — 2026-09-03" below; front matter `falsification_passes: 1`; 2026-10-02, OPUS)* One
unresolved-neighbour finding below is flagged for it rather than answered here.

### Corrected 2026-09-03 — two body sizes

| Address | Was | Is |
|---|---:|---:|
| `002D8690` | 1106 B | **306 B** |
| `002D87D0` | 1106 B | **306 B** |

Found by `audit_crossrefs` as `BODY DRIFT` and confirmed against the certified function list.

**The cause, because it is the useful part.** `002D28E0` is **1,106 bytes**, and it appeared one row
away from these two functions in a working listing this document was written from — the callers of
`0017F850`. **A size was transcribed from the wrong row of a neighbouring table.** Both wrong values
being *identical* is the tell: two independent slips do not land on the same number, so a repeated
value in a size column should be read as one error with two victims rather than two errors.

That is the same shape as the seven sizes in
[the Audio boundary document](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md),
where three claimed sizes covering seven functions turned out to encode a grouping — and where one
of the groups was wrong. **Here the grouping is correct** — `002D8690` and `002D87D0` genuinely are
the same size — **and only the shared value was wrong.** The distinction matters: a repeated wrong
size can mean either, and the two documents now hold one example of each.


### Dispositioned 2026-09-03 — five `UNACCOUNTED NEIGHBOUR` findings

Enumerated by `audit_crossrefs` before they were looked at, so confirming them is maintenance rather
than audit. **Silence is not disposition**, so each is answered, and where the answer is "this is a
real gap" it is flagged for the incoming auditor rather than resolved here.

**Three are shared-utility noise, and the numbers say so.**

| finding | why it is not a relationship of this system |
|---|---|
| `ActorEntity` — 1 edge, `00203170` caller `003F1E90` | `00203170` is the 44-byte axis-vector loader with **84 callers across five owner classes** (39 unowned, 23 Presentation, 20 Movement, 1 Script/VM, 1 UI). A utility at that fan-in has a neighbour in almost every subsystem by construction |
| `Gameplay` — 1 edge, `00203170` caller `00339630` | same routine; the caller is `BattleAction_FindApproachGeometryAroundTarget`, doing its own geometry. Two systems using the same vector loader are not two systems interacting |
| `Movement` — 27 edges via `00202B90`, `00202F70` and siblings | `00202B90` has 14 callers (8 Presentation, 3 Movement, 3 unowned), `00202F70` has 12. **Movement uses the same vector maths as text rendering because it is the same maths**, not because the paths meet |

**One is an artefact of citing a control address, and it is worth knowing generally.**

`Resource` — 2 edges, `00378540` callee `0032E400` / `0032E620`. **`00378540` appears in this
document exactly once, in §8, as the positive control for the string scanner** — *"positive control
2: `00378540` → `MWeather` PASS"*. It is not part of the glyph path and this document makes no claim
about it. The checker cannot distinguish an address cited as a **system claim** from one cited as an
**instrument control**, and inherits the whole neighbourhood of the latter.

> **Publishing your controls costs audit noise.** This project has spent the session pushing sessions
> to name their controls in the document, which is right — and the consequence is that every control
> address drags its neighbours into `audit_crossrefs`. Worth a tool decision: control citations could
> be marked, or the checker could ignore addresses that appear only in an evidence section.

**One is a real gap and is NOT dispositioned away.**

`CoreRuntimeScheduling` — 8 edges. Two of them matter:

```
002AAE40  ->  0020E600   ImageAddress_ResolveRuntimePointer   (10 B)
002B0280  ->  0020E600   ImageAddress_ResolveRuntimePointer
```

`002AAE40` is one of the four functions this document identifies as font drawing by the
`"display : draw Font"` scope, and `002B0280` is the **other** text renderer §2 says exists (the byte-charset one; polarity corrected 2026-09-25, FABLE, Claude Opus 5.5; see UQ-361). **Both
resolve authored-data pointers, and this document never mentions that they do.** The remaining edges
(`002AC5F0` → `00229E40`, `0018EEE0` → `001A1470`) are 7- and 93-byte scheduling helpers and are not
argued either way here.

**Flagged for the falsification pass this document still owes, not resolved by its author.** Whether
authored-data pointer resolution belongs in §2's mechanism, and whether it changes the account of how
a glyph run reaches its font data, is exactly the kind of judgement an author should not make about
their own omission.

## Falsification pass 1 — 2026-09-03, session `repos-d2` (author recused)

Run by a session that did not write this document, at the author's request, because its four
`unresolved → proposed` rows are the four rows of a pending mutation and **a pass by the author on
the evidence backing a mutation is the weakest possible check.** Program state: parent `2ed8affb…`,
snapshot `46f02e26…`, EXE `73461d08…`, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED`.

### Batch verdict: all four rows cleared

| row | cleared on |
|---|---|
| `003649A0` `Text_EmitGlyphRunQuads` | 23 distinct callees, **6 render/scope**: `FontScope_CloseAndFlush`, `RenderCommand_BeginSubpacket` / `FinalizeSubpacket` / `SubmitCurrentBufferAndSwap`, plus both glyph-cache functions, `Log2OfPowerOfTwo` and `Vec3TransformByMatrix` |
| `00366110` `Text_InterpretBraceTag` | compares against `}`; the 90-byte trailer decodes **exactly** as a 2-byte `NOP` plus **22** image-base-relative offsets, all 22 landing in-body, **12 distinct targets**, dispatched by `jmp rcx` at `0036618B` |
| `00364530` `Text_MeasureGlyphRun` | 12 call sites, **~~zero~~ two** render-target chooser calls and no scope call *(corrected 2026-10-02, OPUS: `0017FD00` at `00364530`+0xB0 and +0x169, as the render-target page says)*, sharing six `0017Fxxx` metric helpers with the emitter and calling `00366110` |
| `0053E0B0` `Text_DrawScrolledWindowLines` | call order `003659F0 → 003649A0` **twice**, then `002D8BB0 → 002D8C80 → 002D8BB0`; `add rsi, 0x20` at `0053E337` is the 32-byte line-record stride; five comparisons precede the first pass |

**Two of those deserve their method noted rather than their result.**

**The measure row is cleared on a *controlled* negative.** "No drawing" is an absence claim, so the
identical scan was run against `003649A0`: it returns **6** render/scope calls. The instrument fires
when render calls exist, so **zero on the measure path is a measurement rather than a silence.**

**The eleven tags are corroborated from a direction this document did not use.** §8 states the
90-byte gap is *"its own jump table, exactly accounted"*. It is: `2 + 22 × 4 = 90`. And **22 cases
resolving to 12 distinct handlers is eleven tags plus a default** — arrived at from the table's
arithmetic, touching none of the reasoning that produced the tag list.

**Extents.** All four are exact against the ledger and each terminates in `C3` followed by `int3`
padding or, for `00366110`, by its own table. The reported cause of the earlier `1,106` drift was
also checked rather than adopted: `002D28E0` is 1,106 bytes and **ends `FF`, not `C3`**, consistent
with a size read from the wrong row of a caller listing.

**Explicitly not cleared, and none of it bears on the four names:** the shadow *offsets*, the `{i}`
body, and (at the time of the verdict) `003659F0`'s role, which a third session then read.

### Overturned — `008C5F80` is a pooled constant run, and so was the correction

The key-address row first called `008C5F80` *"the 4×4 identity"*, and a correction earlier the same
day replaced that with *"a pool of six ± axis vectors"*, noting that no `−X` exists and nobody had
explained it. **Both readings are over-reads, and the missing `−X` is not an anomaly.**

```
+0x00   1  0  0  0        +0x40   0  0 -1  0
+0x10   0  1  0  0        +0x50   0  0  0  1
+0x20   0 -1  0  0        +0x60   0  1  0  1     <- not an axis vector at all
+0x30   0  0  1  0        +0x70   0  0  0  0     <- referenced by nothing   <- corrected 2026-10-02, OPUS: +0x70 (008C5FF0) holds 22 05 93 19 01 00 00 00 40 45 C3 01, not zeros; the pool ends at +0x70
```

A reference census over all 38,161 bodies settles what the region is:

| row | value | referencing functions |
|---|---|---:|
| `+0x00` | `1 0 0 0` | 42 |
| `+0x10` | `0 1 0 0` | 39 |
| `+0x20` | `0 -1 0 0` | **1** |
| `+0x30` | `0 0 1 0` | 42 |
| `+0x40` | `0 0 -1 0` | 3 |
| `+0x50` | `0 0 0 1` | **73** |
| `+0x60` | `0 1 0 1` | 3 |
| `+0x70` | `0 0 0 0` | **0** |

**110 distinct functions touch the region and 72 of them touch exactly one row.** Different callers
take different subsets: `00203170` and about two dozen others take `[0, 1, 3, 5]` — which **are** the
identity — while `00189130`, the sole reader of `+0x20`, takes `[0, 2, 4]` = `+X, −Y, −Z`.

**So this is a compiler-deduplicated `.rdata` float-constant pool, not a structure.** The constants
immediately before it are `0.02`, `0.10`, `1.5708`, `6.2832` and `1000.0` — a generic pooled area.

**And that dissolves the `−X` question rather than answering it: there is no `−X` row because no
function in the image needed one.** A pool contains what was used, deduplicated, in emission order.
The "missing" element is only missing relative to a structure that was never there — and `+0x60`
(`0 1 0 1`, not an axis vector) and `+0x70` (referenced by nothing) are the same tell read from the
other end.

> **The original reading named the region after four of its rows; the correction named it after six.
> Both named a pool.** The lesson is not that either count was wrong but that **a run of constants in
> `.rdata` does not have to be anything** — and when the reference census shows most callers taking
> exactly one element, that is the answer rather than a step toward one.

**Nothing in the batch is affected.** `00203170` really does load four rows that really do assemble
to the identity; only the *name of the region* was wrong, twice.

## 9. Related

- [`../README.md`](../README.md) — the residual category. Its "Direct authored strings: 0" row
  is corrected by §8 above.
- [`../the-unresolved-158.md`](../the-unresolved-158.md) — §10/§11 identified the 13-function
  cluster containing `002AC5F0`, `002AAE40` and `002AF960` as the highest-value target and
  reinstated the text hypothesis on partial evidence. §8 above settles it.
- [`../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md)
  — the upstream half: number to characters. **Should reopen**: its §1 records the measuring
  function as unread, and §2 here reads it.
- [`../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
  — the PS2-derived drawing vocabulary this renderer's command codes belong to.
- [`../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md`](../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md)
  — the graphics local memory the glyph cache uploads into.
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the tiers cited in §8.

### Correction 2026-09-02, ITSELF CORRECTED 2026-09-03 — `008C5F80` is a deduplicated constant pool

> **The correction below replaced one over-read with another, and both named a pool.** The
> original text called this address *"the 4×4 identity"*, naming the region after the four rows
> one caller assembles. The correction called it *"six ± axis vectors"*, naming it after six. **It
> is neither: it is a compiler-deduplicated `.rdata` constant pool, and the “missing −X” is not an
> anomaly.**
>
> Re-read from the certified program, `+0x60` and beyond:
>
> ```
> 008C5FE0 (+0x60)   0  1  0  1      <- not an axis vector at all
> 008C5FF0 (+0x70)   22 05 93 19 01 00 00 00 | 40 45 c3 01 00 00 00 00
>                                    <- not float data; the pool has ended
> ```
>
> **110 distinct functions touch the region and 72 of them touch exactly one row.** Different
> callers take different subsets: `00203170` and about two dozen others take rows 0, 1, 3, 5 —
> which *are* the identity — while `00189130` is the sole reader of `+0x20` and takes rows 0, 2, 4
> = `+X`, `−Y`, `−Z`. The constants immediately before the region are `0.02`, `0.10`, `1.5708`,
> `6.2832`, `1000.0` — a generic pooled area.
>
> **So there is no −X row because no function in the image needed one.** A pool contains what was
> used, deduplicated, in emission order. **The missing element is only missing relative to a
> structure that was never there** — and `+0x60` being `0 1 0 1` is the same tell from the other
> end.
>
> **The lesson is not that either count was wrong.** It is that **a run of constants in `.rdata`
> does not have to be anything**, and when the reference census shows most callers taking exactly
> one element, **that is the answer rather than a step toward one.**
>
> Nothing downstream is affected: `00203170` really does load four rows that really do assemble to
> the identity. **Only the name of the region was wrong, twice.**

#### The superseded correction, kept for its trail

### ~~Correction 2026-09-02 — `008C5F80` is a vector pool, not a 4×4 identity~~

The key-address row called `008C5F80` a `float[4]×4` and named it *"the 4×4 identity"*. **The four
offsets it lists are right and the assembled result is right; the object is not.** The full `0x60`,
read from the certified program:

```
+0x00   1  0  0  0     <- loaded here
+0x10   0  1  0  0     <- loaded here
+0x20   0 -1  0  0
+0x30   0  0  1  0     <- loaded here
+0x40   0  0 -1  0
+0x50   0  0  0  1     <- loaded here
```

**Six ± axis vectors interleaved.** The gaps this document already declined to explain — it lists the
rows non-contiguously, so its author plainly saw that `+0x20` and `+0x40` were skipped — hold the
**negations**. The four that are loaded do assemble to the identity, so every downstream statement in
this document stands. What was wrong is the **type**: naming a 64-byte matrix object at an address
that holds a pool, when the code reads four selected rows out of six.

**The tell was already in the row.** A contiguous `float[4]×4` at `008C5F80` would have rows at
`+0x00`, `+0x10`, `+0x20`, `+0x30`; this row lists `+0x00`, `+0x10`, `+0x30`, `+0x50` and calls the
object contiguous in the same breath. **A type label and an offset list in the same cell disagreed
with each other, and neither the author nor five subsequent readers compared them.**

> **When a row states a type and an extent that cannot both be true, it is not a typo — it is two
> different readings of the address that were never reconciled.**

Found by a falsification pass on `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`, whose
own §2 reaches the *correct* reading — "four rows selected from a pool of common vectors, not a
contiguous matrix literal" — by inference from the uneven spacing. That pass dumped the whole `0x60`
rather than the cited rows and turned an inference into a positive explanation. The bytes above were
then re-read here independently before this correction was applied.

**This is the first time the cross-document check has caught the error in the neighbour rather than
in the document being attacked.** The check has now caught something five times; on the four previous
occasions the document under audit was the one that was wrong. It is not only a check on the thing
you are auditing.

## `002AF960` read — the context setup, and `+0x10E4` closed across three functions

This document asked **"what `002AC5F0`, `002AAE40` and `002AF960` draw"**. The first two are read
elsewhere; this is the third, and the answer for it is **that it does not draw — it sets up.**

> **That answer was the first of three, and all three came back the same way.** None of the trio
> draws, and `002AAE40` calls `002AC5F0`, so they were never peers. **The question has since been
> withdrawn rather than answered** — see the entry in section 7. **Getting a not-quite-fitting answer
> three times was the signal to check the question instead of the answers**, and it took three
> readings to hear it.

It was reached by a **pair census** rather than by a citation: a scan for structure displacements
touched by two to six functions put `+0x10E4` at three touchers, two of which had been compared and one
of which — this one — **nobody had opened.**

**Extent checked**: 230 instructions, and the last instruction is `jmp 0x2afafa`, **inside its own
body** — a loop back edge, not a tail call.

### It initialises the context the other text functions consume

```asm
002AFB19  mov   dword ptr [rcx + 0x10d8], eax       ; from word [src + 0x8C]
002AFB26  mov   dword ptr [rcx + 0x10dc], eax       ; from word [src + 0x90]
002AFB2C  mov   dword ptr [rcx + 0x10d4], esi       ; the batch counter, zeroed
002AFB32  mov   byte  ptr [rcx + 0x1102], 1
002AFB39  movsx    eax, byte ptr [rbx + 0x9d]
002AFB44  cvtdq2ps xmm0, xmm0
002AFB47  mulss    xmm0, dword ptr [rbx + 0x50]
002AFB4C  movss    dword ptr [rcx + 0x10e4], xmm0   ; the budget
```

**`+0x10D4` is the same batch counter the emitters compare against `0x14`**, and it is zeroed here — so
this function is where a run of text begins.

### `+0x10E4` now has three roles in three functions, and the lifecycle is closed

| function | what it does with `+0x10E4` |
|---|---|
| **`002AF960`** *(this one)* | **initialises it: `(float)byte[src+0x9D] × float[src+0x50]`** |
| `002A9F00` | **decrements it**, once per character |
| `002AC5F0` | **multiplies by it** and compares the product |

> **A count byte times a per-unit scale, spent one character at a time, and read as a multiplier while
> it lasts.** The initialisation is what settles the reading: **it is a budget**, and the multiply is a
> use of *how much is left*, not an independent scale factor.

That question was previously answered as *"one field, two roles, two functions"* after two readers
compared notes. **The third site was found by census rather than by collision, and it supplies the
origin neither of the other two could.**

### What it is

Two calls to `RenderCommand_SubmitCurrentBufferAndSwap` and a run of small `0017Fxxx` render-state
calls, around two loops — **the open and close of a text run**, not the per-glyph work. The
`"display : draw Font"` string this document already associates with it names the scope it opens.

### What is not established

- [x] ~~**UQ-368.** What `byte [src + 0x9D]` counts and what `float [src + 0x50]` scales — **the budget's two
      factors are read; their units are not.**~~
      **ANSWERED 2026-09-14 (FABLE): `+0x9D` is a fade length in glyphs, and `+0x50` is the per-glyph alpha step.**
      `002AF960` passes `src` as the context to the measure pass (`002AFA92`) and to the renderer it dispatches
      (`002AFC82`–`002AFCB1`), so the emitter's context is the same object. The emitter copies it to `rsp + 0x60`
      and addresses the copy through `rbp = rsp + 0x100` (`002A9F0A`–`002A9F11`). Its per-glyph block
      (`002AA05C`–`002AA0BA`) therefore reads context `+0x33` (`[rbp − 0x6D]`, the glyph alpha) and context `+0x50`
      (`[rbp − 0x50]`):
      - while painter `+0x10DC` is positive, the glyph keeps its alpha;
      - otherwise the alpha is `alpha × [+0x10E4]`, clamped to `[0, 0x80]` (`002AA079`–`002AA097`), and the budget
        then drops by context `+0x50` (`002AA07D`–`002AA086`).

      The budget starts at `+0x9D × +0x50`, so the multiplier steps down by `+0x50` a glyph and reaches zero after
      `+0x9D` glyphs past the full-alpha ones. The `0x80` clamp is set again before every loop iteration
      (`002AA73C`). The interpreter's inline-glyph arms fade the same way
      ([the control-code language](../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md) §2.6).
- [x] ~~**UQ-369.** What `+0x10D8` and `+0x10DC` hold, beyond being copied from two `word` fields.~~
      **ANSWERED 2026-09-14 (FABLE): two per-glyph countdowns.**
      - **Sources.** `002AF960` loads `+0x10D8` from context word `+0x8C` and `+0x10DC` from context word `+0x90`
        (`002AFB05`–`002AFB26`).
      - **Spending.** The emitter decrements both once per glyph (`002AA0B1`–`002AA0BA`), and once per unit a
        control code reports through its character count (`002AA6C3`–`002AA6FF`).
      - **`+0x10DC` is the number of glyphs still drawn at full alpha.** While it is positive, the fade budget is
        neither applied nor spent (UQ-368, above). The interpreter's inline-glyph arms test it the same way.
        `002B0280` sets it to `0x7D00` (32,000) before three of its emitter calls (`002B16FD`, `002B1759`,
        `002B1919`), which switches the fade off for those runs.
      - **`+0x10D8`** counts down in step with it. None of the eight text-cluster bodies scanned tests it for
        zero. The `*` code reads it in a proportion (`002AD670`–`002AD6CD`).
      - **Compensation.** The number formatter `002AE610` adds one back to both under a flag test (`002AE9D2`–
        `002AE9E8`), so some digits do not count.

      The markup parser's `"` tag writes a word at state `+0x90` ([numeric formatting](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md)
      §13). That structure is not shown here to be this context, so the authored source of the full-alpha count
      is suggested, not established.
- [x] ~~**UQ-370.** What `byte +0x1102` gates, set to `1` here and cleared elsewhere in the cluster.~~
      **ANSWERED 2026-09-14 (FABLE): it is the line-start flag.**
      - **Set** when a run opens (`002AFB32`), by the line-break token `0x02` (`002AC6DD`), and on `002AAE40`'s token
        path (`002AB691`).
      - **Cleared** by the drawers on the first ordinary glyph (`002AA0ED` in the emitter, `002AAFE7` in
        `002AAE40`) and in `002AF340` (`002AF49C`, set again at `002AF667`).
      - **Gates** the two interpreter arms that place the pen at the start of a line. Justification `%&'` measures
        the rest of the line and writes the justified x (`002AD2B8`), and indent `5` writes its offset as x
        (`002ADD31`). After the first glyph neither can move the line.
      - **Saved and restored** around the selection list's nested call (`002ACA9E`, `002ACACF`).

      See [the control-code language](../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md) §2.6.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named these bodies only at their entries. Each interior address was read in the shipping
image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `002AF340` | `002AF4D0` | `call ImageAddress_ResolveRuntimePointer` mid-body, after it stores `0209CC40`/`0209CC48` — the text-state globals this page documents |
| `003F1E90` | `003F1F9F` | `movss xmm0 → 01DFE0BC` — first of five writes to the same float global between `00271380` calls |
| `002D28E0` | `002D2BB7` | `call 00249EE0` after `0017F650`/`0017FA10`/`0017FB00` — a glyph-run helper chain ending in `00243E90` |

*(Pass 22 adjacency, 2026-09-14: the quad walk touches three outside layers — **rewards**
`00317ED0` calls `00229E40`, `00339630` calls **party** `0031B7E0`, and `0032E620` is called by
**input** `00291C80` (3 edges). Text rendering reuses shared state accessors owned elsewhere; the
edges name the reuse, not a glyph-pipeline owner.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT (22 edges, one fan-in).** All 22 edges are CombatAction bodies calling `0031B7E0` on this page: the focus-handle resolver behind `byte[02089340] & 0x10` that this page documents. `BattleUnit_HandleActorTimelineEvent` is the worked example - it resolves the unit that way before dispatching on the event's `dword[+0]`. The crossing is **one shared primitive with 22 callers**, not 22 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (184 edges).** The UI layer's bodies call the glyph helpers this page cites — `002D28E0`, `002AC5F0` and `002AF960` reach `0017F650`/`0017F850`, and `00247AE0`, `0055B3F0` and `0056A3D0` call `002497B0` (the element-buffer allocator `002A2AD0` uses for its window-slot arrays). UI drives glyph rendering; the glyph pipeline owns nothing in UI. Edge count from `edges.tsv`. (SWE2-EC7 batch 152, shipping bytes.)

**ActorEntity — CLIENT (SWE2-EC7, batch 159, 155 edges).** Actor-layer bodies call the record helpers this page's glyph passes cite — `003F1E90` reaches `00202C70` and `00203170`, `0026C8C0` reaches `0025A990`/`0025AA30`. The glyph pipeline shares the helpers; the actor layer owns nothing in text rendering. Edge count from `edges.tsv`.

**Movement — CLIENT (SWE2-EC7, batch 162, 62 edges).** Movement bodies call the shared helpers this page's glyph passes cite — `0022F250`, `0022F9B0` and `00230C10` all reach `00202B90`, and `00230790` reaches `00202C70`. The crossing is shared-callee fan-in on the transform/record helpers, not a glyph responsibility in navigation.

**Script VM — CLIENT (SWE2-EC7, batch 162, 114 edges).** Script-VM bodies call the same helper family this page cites — `00356160` reaches `00203170`, `0033FED0` and `0034BA00` reach `00229E40`, and the `00264050` edge set is the same shared-callee shape. The glyph pipeline shares the helpers; the script-VM layer owns nothing in text rendering. Edge count from `edges.tsv`.

## The `003649A0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`003649A0` (3,020 B) is the per-line emitter this page already names. Its
prologue calls the four exclusive members in order — `003647E0` (`00364B58`),
`00365FD0` (`00364B90`), `00364210` (`00364BA6`), `00474650` (`00364BFF`) —
before the `00202B90` quad loop and the `0017Fxxx`/`003A1xxx` submit battery.
The layer gate is `bt [022CBE00+0x240], movsx([rcx+0x60])` at `003649E0`–
`003649EA`, and the batch entry is `[02EBEFF0] × 24 + 02EBEFC0` (`003649F0`–
`00364A16`).

| member | role | interior |
| --- | --- | --- |
| `003647E0` (366 B) | the inline-markup interpreter — walks the encoded stream at `[rsi]` (+2 per step), dispatching on the byte after `0x20`: ~~opcode 1 copies~~ opcode 3 copies `[rdi+0x37]`→`[rdi+0x33]` (`00364843`), opcode 2 writes `[+0x37]/5` via the `0xCCCCCCCD` multiply (`0036485E`–`00364868`), ~~opcode 3 scans~~ opcode 1 scans the `[022CBE00]` layer's `0xC`-stride table for `word == 0x30` (`00364893`) — ~~all gated on `byte[rdi+0x63] & 1`~~ only opcodes 2 and 3 gated on `byte[rdi+0x63] & 1` *(corrected 2026-10-02, OPUS: code 1 branches to `003647E0`+0x91 and scans for `0x30` at +0xB3 with no gate; code 3 tests `[rdi+0x63]` at +0x5A and copies at +0x63; code 2 tests it at +0x70 — §2's table is right)* | [`0036485E`](../../_index/ADDRESS-INDEX.md) |
| `00365FD0` (171 B) | the u16-key cache scan — walks `[022CBE00]` records matching `word[rax+0x10] == cx` with ~~`r8d`/`edx` range checks~~ an exact match of the font byte `+0x12` against `edx`, a move of the hit node to the list head `+0x230`, and a `byte[rax+0x13]` flag (`00365FE7`–`00366073`) *(corrected 2026-10-02, OPUS: the relink is `00365FD0`+0x2C..+0x9B; §3's `GlyphCache_PromoteOnHit` row is right)* | [`00365FE7`](../../_index/ADDRESS-INDEX.md) |
| `00364210` (367 B) | ~~the span clipper~~ the glyph-cache fill on a miss — it unlinks the list tail `[022CBE00+0x228]` and relinks it at the head `+0x230` (`00364210`+0x1B..+0x49), then a u16 tag scan over `[022CBE00]` records, then `byte[rcx+2]`/`byte[rcx+3]` ~~clamped against the `edx`/`ebx`/`ebp`/`r14d` bounds, returning the clipped span in `eax`/`edx`~~ rounded up to 8, 16, 32, 64 or 128 and stored at node `+0x14`/`+0x15`, returning the node in `rax` (`003642D0`–`00364338`) *(corrected 2026-10-02, OPUS: `00364210`+0x14D `mov rax, r8` returns the node, 0 on a miss; §3's `GlyphCache_FillOnMiss` row is right)* | [`003642D0`](../../_index/ADDRESS-INDEX.md) |
| `00474650` (35 B) | the arg-shuffle adapter — repacks `rsp+0x28`/`rsp+0x30` into registers and tail-jumps to `003A22A0` (`0047466E`) | [`00474650`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0017FA10`/`0017FD00`/`0017FB00`/
`0017F8C0`/`0017F9C0`/`0017F8E0`/`0017F850`/`0017FAE0`/`0017F7C0` (the
draw-state API), `002DDC50`, `00254A00`, `003666E0`, `003A1FE0`/`003A2090`/
`003A2020`/`003A1DB0`/`003A22A0`, `00202B90`, `0016D6A0`, `00808C40`.

## Interior citation — frontier hub `0017FB00` (2026-09-18, SWE2-EC7)

`0017FB00` — 103 B, 8 A-measured callers; the record repack the quad path runs per batch.
Interior verified: four `xmm` rows are copied out of `rcx` and re-stored interleaved into a
`0x50`-byte stack record at `rbp+0x17` (`0017FB0E`–`0017FB49` — rows 0/3 land contiguous,
1/2 swap slots), `001B5FA0()` supplies the draw context, and `001E9C80(ctx, &record)` submits
it at [`0017FB59`](../../_index/ADDRESS-INDEX.md). A layout adapter between the caller's 4x4 matrix shape and the
context's expected record order.


## Interior citation — frontier hub `002AC2F0` (2026-09-18, SWE2-EC7)

`002AC2F0` — 767 B, 6 A-measured callers; the text-render object init whose product this page's
glyph walk consumes. Interior verified: clears globals `0209CC70`/`0209CC78` (`002AC30C`–
`002AC316`), requires `byte [[rdx]] >= 0x20` (`002AC32A`), resolves the shared table row via
`0039C4A0` into `[rdi+0x60]` ([`002AC330`/`002AC345`](../../_index/ADDRESS-INDEX.md)), and the
`[rdi+0x44] & 0x800` persistent flag selects the `0017FD30(7,…)` notify arm (`002AC34E`,
`[0209DD80]` dword becomes 7) over the plain one. The rest of the body seeds the draw-state
fields the glyph pass then reads.


### Interior citation — frontier hub `003FFC60` (2026-09-18, SWE2-EC7)

`003FFC60` — 115 B, 6 callers (`002A8C50`, `002AC5F0`, `002AE610`, `002B0280`,
`002B4810`, `002B49F0` — the text-element drawers this page walks). Sibling of
the `003FFAB0` compact-record decoder: `rdx` receives `byte[rec+1] & 0x7F`, `r8`
receives `min(byte[rec+2] & 0xF, 8)` (the clamp at
[`003FFC81`](../../_index/ADDRESS-INDEX.md)), and `r9`/two stack outputs each
receive one bit of `byte[rec+2]` (`>>6`, `>>5`, `>>4`). Returns 3 — the record's
byte length.

### Interior citation — frontier hub `00364980` (2026-09-18, SWE2-EC7)

`00364980` — 28 B, 11 callers, `Text_IsExPrefixed`: the renderer selector,
verified against the image — null `rcx` returns 0, `byte[rcx] == 0x65` and
`byte[rcx+1] == 0x78` (`'e','x'` at
[`00364988`](../../_index/ADDRESS-INDEX.md)) return 1, anything else 0. The
two-byte prefix probe the quad pipeline consults.
## SWE2-EC7-18 update (2026-05-15) — `002D8C80` 0x30-byte record copy to the `022D80xx` globals

`002D8C80` (48 B) is the record-staging forward this page's draw path reaches: it builds a three-field stack record — `[rsp+0x20] = 00917250`, `[rsp+0x28] = 0`, `[rsp+0x30] = 1.0f` (`01CEBBA8`) — and calls `002DB080` (`002D8C84`..`002D8CA6`), the staged `{record, 0, 1.0f}` submission the icon-record path runs before the glyph-quad emitters.
## SWE2-EC7-32 update (2026-09-18) — `00202F70` rotation-matrix build

`00202F70` (100 B) is the `{r}` builder the name-format sequence
names: the caller's 0x40-byte record copies in four `movups`, the
`xmm2` angle goes through `00861F08` (cos) and `00861F0E` (sin),
and a tail `jmp 00217970` assembles the matrix at `rcx` with both
results — copy-layout, compute angle pair, assemble. Interior
anchor `00202FCF` (the `jmp 00217970` tail).

## SWE2-EC7-40 update (2026-09-19) - `002B4810`

`002B4810` (381 B) is a glyph-run body - `002B1FB0` plus the `003FFxxx` family (`003FFF10`/`003FFB90`/`003FFC60`/`003FFCE0`/`003FFAB0`). Interior anchor `002B4857` (a `002B1FB0` call).

## SWE2-EC7-42 update (2026-09-19) - `00407450`

`00407450` (305 B) is a glyph-quad body - `00407D10`/`00394690` pair/`00393220`/`002F9860`/`00364980`/`00365B30`/`002B4090`/`0020E620`. Interior anchor `00407460` (a `00407D10` call).

## SWE2-EC7-42 update (2026-09-19) - `002DD680`

`002DD680` (297 B) is the kind-2 drawer stamp the page names - `01F44830`, `00203170`/`00397910`/`002B0280`/`00808C40`. Interior anchor `002DD73C` (a `00203170` call).

## SWE2-EC7-42 update (2026-09-19) - `003659F0`

`003659F0` (297 B) is the `'ex'`-prefix case builder the page names - `01F44830`/`022CBE00`, `00861EC0`/`00202C70`/`00203170`/`00202D70`/`0017FAE0`/`00808C40`. Interior anchor `00365A33` (an `00861EC0` call).

## SWE2-EC7-43 update (2026-09-19) - `002D89E0`

`002D89E0` (276 B) is a glyph-quad body - `01F44830`, `002B3400`/`002DD5D0`/`002DD680`/`00364980`/`003659F0`/`00808C40`. Interior anchor `002D8A20` (a `002B3400` call).

## SWE2-EC7-50 update (2026-09-19) - `00202B90`

`00202B90` (181 B) is `Vec3TransformByMatrix` - call-free `out = in.x*row0 + in.y*row1 + in.z*row2` `mulss`/`addss` per component over `r8` vector, `rdx` 3x4 matrix. Interior anchor `00202B94` (the `y` load).

## SWE2-EC7-52 update (2026-09-19) - `00407D10`

`00407D10` (639 B) is a glyph-quad body - `00404F50`/`002487A0` plus `02B62D88`. Interior anchor `00407D8E` (a `00404F50` call).

## SWE2-EC7-53 update (2026-09-19) - `002487A0`

`002487A0` (745 B) is a glyph-quad publish body - xmm0/xmm1/xmm3 + rax into `022D9310`-`022D931C`, the `022D8F90`/`022D8FA0`/`022D8FB0`/`022D8FC0` heads mirrored into `022D92E0`-`022D92EC` and `022D9450`-`022D9458`, `0036DD80` tail. Interior anchor `0024896B` (a `0036DD80` call).


## SWE2-EC7-78 update (2026-09-20) - `0017FD00` two-call forwarder measured

`0017FD00` (35 B) is the `001B5FA0` + `001E9D20` forwarder the
glyph/text callers share: `rax = 001B5FA0()`, then it tails
`001E9D20(rax, ebx, 2, 0)` - a fixed-mode delegate with `r8d = 2`,
`r9d = 0`.
Interior anchor `0017FD08` (the `001B5FA0` call).

## SWE2-EC7-93 update (2026-09-20) - `003656A0` float-parameter call measured

`003656A0` (312 B) is the parameterized glyph query `002D8B00` calls:
a 0x68 stack record is zeroed, three `1.0f` fields are staged, the
`[rbx]` float and `[rbx+0x60]` kind byte override them when a record
is given, the `002DDC50` gate admits kinds 6-0xB to the `00254A00`
scale, `[02CDBF9B+0x238]` is cleared, `0017FAE0` + `00364530(record)`
produce a ratio that scales the two outputs, and `cvttss2si` writes
words into `rsi`/`rdi`.
Interior anchor `003656D5` (the `00861EC0` record clear).

## SWE2-EC7-100 update (2026-09-20) - `002B41F0` + `002B3E90` measured

`002B41F0` (460 B) is the staged-record text submit
`002AC5F0`, `002B20B0`, `002B4540` and `002B49F0` call: a
`0xD0` parameter block builds on the stack (`00861EC0`
clear, `0x80808080` colour, `0x1E`/`0x25`/`0xFF`/`8`
stamps, `0x3F800000` scales, `0039C4A0` resolve into
`+0xA0`, `0x30000` flags), `0209CC40`'s `+0x10C8` scratch
slot is redirected at the record for the duration,
`strlen(rbx)` lands at `+0xCC`, the block is copied into
the second stage and `002AF340` submits it with the
string - then `+0x10C8` restores - the swap-call-restore
text write the glyph path runs.
Interior anchor `002B4385` (the `002AF340` call).

`002B3E90` (506 B) is the sibling measure-and-advance
`002A3250`, `002A6C40` and `002A8C50` call: the `0xD0`
record is copied in, `+0x10C8` redirects to `0031A544`
this time, `002AF340` measures, `002B43C0(rbx, rdi, 3)`
bounds the answer, and a nonzero clamped width advances
the pen - `+0x8E` takes old `+0x8C`, `+0x8C` gains the
width and copies to `+0x90`, `+0x92` keeps the old
`+0x90`, `+0x9B`/`+0x9D` clear - then `+0x10C8`
restores - the render-width advance the line walk
applies.
Interior anchor `002B4036` (the pen-advance arm).

## SWE2-EC7-101 update (2026-09-20) - `002B2930` + `002B28F0` + `002B2880` + `002ABF20` measured

`002B2930` (57 B) is the Nth-occurrence scan `002A3250`,
`002A4830`, `002A5020` and `002A6190` call on the `+0x28`
buffer: walk bytes until the `edx`-th `3` is seen, then
return one past it (`rax+1` recorded per hit) - the
byte-3 delimiter seek the line walk uses to step fields.
Interior anchor `002B2947` (the `cmp cl, 3`).

`002B28F0` (62 B) is the sibling count-and-last scan
`002A3250`, `002A4830`, `002A5020`, `002A5CC0` and
`002A6190` call: the `+0x28` buffer walks `word[+0x8A]`
bytes counting `3`s into `[rdx]` while `r9` tracks one
past the last hit - the count-and-position pair the
line walk derives delimiters from.
Interior anchor `002B2917` (the scan loop head).

`002B2880` (44 B) is the float out getter `002A3250`,
`002A4830`, `002A5020`, `002A5F40` and `002A6C40` call:
`002B2970` resolves the `+0x28` buffer into a stack
out-pair and `cvttss2si` of the float lands at
`word[rdx]` - the measured-extent fetch the glyph arms
share.
Interior anchor `002B2897` (the `002B2970` call).

`002ABF20` (65 B) is the pen-store dispatch `002A3250`
and `002A6C40` call: `0209CC40`'s `+0x10D8` takes
`movsx word[rcx+0x8C]`, `0209CC48` clears, and
`byte[+0xA3]` tripled indexes the `009164C8` vtable -
`jmp` into the selected arm - the mode-keyed
continuation the text walk runs per record.
Interior anchor `002ABF54` (the vtable index load).

## SWE2-EC7-109 update (2026-09-20) - `001E9F40` measured

`001E9F40` (261 B) is the
parameter-block constructor
`00181E70`, `00181F20`,
`001C1D20`, `001C2980` and
`001CCB20` run: `+0x10`..`+0xE0`
zero, `1.0f` lands at `+0x58`,
`+0x6C`, `+0x80`, `+0x94`, then
the tuning constants - `+0xF0`
= 3.0, `+0xF4` = -10.0, `+0xF8`
= 0.45, `+0xFC` = 1, `+0x100` =
0.005, `+0x104` = -0.005,
`+0x110`/`+0x114` = -0.0273,
`+0x118` = 0.1, `+0x11C` = 0.6,
`+0x120` = 0x500, `+0x124` =
0x2D0 - the default glyph-run
envelope every instance starts
from.
Interior anchor `001E9F67` (the
first `1.0f` qword write).

Mechanical neighbours introduced by
this section's citations: `001CCB20`
(one of the constructor's callers)
reaches Platform `005CC930` (1
edge), and `005CC930` itself
carries an Application caller
(`00799980`, 1 edge). Those are
edges of the caller and its callee,
not of the parameter block - noted
so the audit accounts for them.

`002A4EE0` (313 B) is the per-glyph walker `002A6190` calls: for `word[rcx+0x3F0]` entries, `sbyte[[rcx+0x400] + i]` indexes the `[rcx+0x3F8]` table at 0x60 stride; flag `byte[+8]&1` scales `sword[+0x1C]` x `float[+0x24]` and `sword[+0x1E]` x `float[+0x28]` into `rbp+0x5C`/`rbp+0x90` and the stack quad, flag `byte[+8]&2` halves the width against `word[+0x10]`, then `002D8C80` finishes - the glyph-quad measure the line builder runs.

Interior anchor `002A4F57` (function `002A4EE0`).

`00217970` (234 B) is the in-place 2D rotation `00202F70` applies to a four-row float record: for each vec4 row at `+0x00`/`+0x10`/`+0x20`/`+0x30` it rewrites the leading `(x, y)` pair as `(x*cos - y*sin, x*sin + y*cos)` with `cos` = `xmm1`, `sin` = `xmm2` - the caller's angle applied to all four rows

Interior anchor `002179F7` (function `00217970`).

`002A2AD0` (219 B) is the element-array (re)build `002E16B0` runs for a `r15d`-count window: `002497B0(count*0x60)` lands at `+0x3F8` and `002497B0(count)` at `+0x400`, each `0x60` element is `00861EC0`-zeroed then stamped `+0 |= 0x20`, `+5 = -1`, `+0x18 = 0x80808080` (the grey RGBA default), `+0x1C`/`+0x20 = 1.0f`, and the `+0x400` byte array zero-fills; `+0x3F0` takes the count, `+0x3F3` clears, `+0x44` trades bit `0x80000` for `0x100000`, and `+0x54` snapshots `+0x98`

Interior anchor `002A2B3B` (function `002A2AD0`).

`003F3D80` (185 B) is the per-element transform pass `003F1E90` runs when stamping a glyph run: `00203170` builds the `0x60`-byte local record, the incoming `xmm7`/`xmm6` float pair is stamped at `+0`/`+0x14`/`+0x28`, and `edi` elements of the `0xA0`-stride array starting at `rcx+0x60` each take two `00202B70` applications - the `+0` and `+0x10` members against the same record - before the stack cookie is checked

Interior anchor `003F3DE0` (function `003F3D80`).

`0053DD20` (908 B) is the glyph-run header builder `0053F0D0` calls per staged run: the `rdx + r9*8` attribute triple (`+0xCC`/`+0xCD`/`+0xD0`) fills `rcx+0x18`/`+0x19`/`+0x1A`/`+0x1B` and the `+0x8` dword, `r9w` lands at `+0xC`, bit 15 of `r9` picks text id `0x6590` or `0x61A8` for the `002F9860` label stored at `[rdi]`, a `0x68`-byte local record is `00861EC0`-cleared, and `byte[rsi+0x102]` dispatches the align class - `003656A0` measures and the `r15`-offset extents commit to `+0x14`/`+0x16`

Interior anchor `0053DDAC` (function `0053DD20`).

`0026BC70` (166 B) is the signed-angle write `00355A00` runs: `xmm6` gets `+/-pi` added by its own sign (`40490FDB`/`C0490FDB`), wraps by truncating against `6.2832f` (`40EA0EA1`), then subtracts the bias back into `(-pi, pi]`; `byte[+3] >> 5` selects - lane 1 stores to `[+0xB8]+0x48`, lane 3 first pushes it through `003DA850` onto `+0x70`/`+0x60` then stores, other lanes write nothing

Interior anchor `0026BCE9` (function `0026BC70`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Application — MECHANICAL, 1 edge.** `005CC930` is called by `00799980`.

**Audio — MECHANICAL, 10 edges.** `0036DD80` is called by `00361DE0`, `003623C0`, `00363FD0`; `005CC930` is called by `00223190`, `00224570`; `001E8070` calls `00225690`; `00202C70` is called by `00362850`; `002DB080` calls `00182E80`; `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `00362850`; `00407450` calls `00225580`.

**CombatAI — MECHANICAL, 1 edge.** `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) is called by `AiOrder_EvaluateTargetSelector` (`00301AD0`).

**CoreRuntimeScheduling — MECHANICAL, 12 edges.** `0018EEE0` calls `001A1470`; `00254A10` calls `00229E40`; `002A6190` calls `001EDEC0`; `002A8C50` calls `001EDDA0`; `002AC5F0` calls `00229E40`; `002B0280` calls `00229E40`; `002EF350` calls `00229EC0`; `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls `00229E40`; `0053E380` calls `001EDEC0`; `005528C0` calls `001EDEC0`; `0057C480` calls `001EDEC0`; `005CC930` is called by `001E03F0`.

**Gameplay — MECHANICAL, 6 edges.** `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) is called by `BattleUnit_HasCurrentFocusEngagementEvidence` (`0030BB30`), `00312B40`, `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` (`00339630`); `00203170` is called by `BattleAction_FindApproachGeometryAroundTarget` (`00339630`); `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `0031ADB0`.

**Platform — MECHANICAL, 2 edges.** `001CCB20` calls `005CC930`; `00799980` calls `005CC930`.

**Resource — MECHANICAL, 30 edges.** `0032E620` is called by `00249210`, `0024AC30`, `00259DF0`, `00324510` and 5 more; `0032E400` is called by `00249210`, `0024AC30`, `00259DF0`, `00379E90` and 4 more; `0032F430` calls `0032E400`, `0032E520`, `0032E620`; `00378540` calls `0032E400`, `0032E620`; `0053EB90` calls `002493D0`, `00249580`; `005CC930` is called by `001D9F90`, `001DADC0`; `00291C80` calls `0032E620`; `0032E620` calls `0032E870`; `003EE420` calls `0024A5A0`; `008620C0` is called by `0032E3B0`.

**Save_Load_Settings — MECHANICAL, 3 edges.** `00254A10` is called by `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`); `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`); `0032E620` is called by `002EF300`.

**World — MECHANICAL, 7 edges.** `ActorManager_GetRecordByOrdinal` (`00358940`) is called by `0025E400`, `002623A0`; `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is called by `0025E400`, `002623A0`; `0032E400` is called by `00378540`; `0032E620` is called by `00378540`; `0032F430` is called by `00266D10`.

**WorldAreaField — MECHANICAL, 20 edges.** `0032E400` is called by `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10` and 1 more; `0032E620` is called by `MapRef_BeginLoadResources` (`00268750`), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (`003EA820`); `00267930` is called by `MapRef_BeginLoadResources` (`00268750`); `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`); `ActorSystem_InitializeManagerRuntime` (`0026CE60`) calls `BattleSystem_InitializeAreaState` (`002342F0`); `0032F430` calls `003EA6B0`; `003320D0` calls `003EAA00`; `003320E0` calls `003DFE60`; `00332100` calls `003DFDC0`; `00332110` calls `003DFE60`; `00378540` is called by `00377CC0`; `003EAA00` calls `003DCF10`; `003EAA00` is called by `003319D0`; `003F9720` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-how-a-line-of-text-becomes-glyph-quads-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00267BB0` | 102 B | calls `0036B200(0xD)`, then `0036C1D0(0xD, 5)` when that returned non-zero and `0036C1D0(5, 5)` otherwise; takes `0036C750(009156E8)` (the string "..\..\katano\ateldecode.c"), returns `0036C660(0036A100(ecx), that result, 0x16C1)` after calling `0036C140()` | `00267BC1`, `00267BD2`, `00267BE0`, `00267BFB`, `00267C03` |
| `00267C20` | 102 B | calls `0036B200(0xE)`, then `0036C1D0(0xE, 5)` when that returned non-zero and `0036C1D0(5, 5)` otherwise; takes `0036C750(009156E8)` (the string "..\..\katano\ateldecode.c"), returns `0036C660(0036A100(ecx), that result, 0x16E6)` after calling `0036C140()` | `00267C31`, `00267C42`, `00267C50`, `00267C6B`, `00267C73` |
| `00271380` | 39 B | calls `003588B0(rcx)`; returns the float -1.0 (`01CEBC9C`) when that is null, otherwise tail-jumps `00263940(object)` | `00271384`, `0027138E`, `002713A2` |
| `002A35B0` | 66 B | stores `rdx` at qword `+0x1A8` of `rcx`, overwrites it with the result of a second `0039C480()` call when the first `0039C480()` returns non-null, then tail-jumps `002A3250(rcx, r8)` | `002A35BD`, `002A35C7`, `002A35D1`, `002A35D6`, `002A35ED` |
| `002B2D90` | 82 B | walks runs from `rcx`, each a byte whose low 7 bits (AND `0x7F`) give the count of bytes that follow it, stopping at a zero byte or after run index `r9d`; runs whose index bit (`bt`) is set in `edx` are not counted, and at the unskipped run number `r8d` (from 0) it stores the run's low 7 bits at the dword the fifth (stack) argument points to and returns the pointer past that byte; when the walk stops first it stores 0 there and returns 0 | `002B2D96`, `002B2D9B`, `002B2DA1`, `002B2DBA`, `002B2DCD` |
| `003666E0` | 88 B | forms `r8` = sign-extended `ecx+ecx` minus 1, finds its highest set bit by scanning down from bit 63 (`sar`, `test al, 1`), then keeps scanning down while bits stay set and returns that highest bit index minus the index where the second scan stopped (the first clear bit, or 0); for a power-of-two `ecx` this is its log2 | `003666E7`, `003666EC`, `00366709`, `00366729`, `00366731` |
| `003EA6B0` | 43 B | stores -1 at dword `02B5E0B8`, zeroes the 16 bytes at `02B5E0C0`, calls `003DCF00(0)` and tail-jumps `003DCF10(0)` | `003EA6B7`, `003EA6C3`, `003EA6CB`, `003EA6D6` |
| `003F7F50` | 187 B | unless dword `[rdx]` is 4, calls `005C5230(rcx, rdx)` and returns its value; for 4 fills a stack record with `002B3400(&rec, qword +0xC0, 0)`, sets its float `+0x34` to 1.0 (`01CEBBA8`) and its byte `+0x9F` to byte `+0x5C` of the qword `+0x38` object, stores word `0x40` at that object's `+0x5A` when bit 0 of byte `+0xD4` is set and `0x80` otherwise (`cmovne`), calls `002D8650(object, word +0xC8, word +0xCA, &rec)` with the words sign-extended and returns 0 | `003F7F6B`, `003F7F95`, `003F7FC9`, `003F7FD0`, `003F7FE3` |
| `0053ED10` | 73 B | calls `00244F50(0xC8, 0053EB90, 0)` when qword `02CA8A78` is zero, then tail-jumps `00244F50(0x1498, 0053E380, 0)` when qword `02CA8A80` is zero and returns otherwise | `0053ED14`, `0053ED2D`, `0053ED32`, `0053ED4F` |
| `00799980` | 92 B | calls `0071F970(rdx, 008F6D40, &f)` and stores the float `f` at `+0x6C` of `rcx`; when `f` is not greater than 0.0 (`comiss`, `jb` skips otherwise, also skipping on NaN) stores at qword `+0x50` the double `005CC930()` minus qword `02CB60E8` minus qword `+0x50` minus qword `+0x40` plus qword `+0x50`; returns 0 | `0079999B`, `007999A9`, `007999AC`, `007999B3`, `007999CF` |
