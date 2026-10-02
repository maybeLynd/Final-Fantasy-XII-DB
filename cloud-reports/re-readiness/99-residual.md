# Reconstruction readiness — `FFXII TZA/99-Unresolved-Residual/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-99-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `f26c5667` only; no executable, Ghidra, extracted data or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** COUNTS-PLACEHOLDER

Citation form: `NAME:line` or `NAME:a-b`. `NAME` is a short name for one page, listed in the table below with its path inside
`FFXII TZA/99-Unresolved-Residual/`, so `NAME:line` reads as `page-path:line`. Line numbers are the snapshot's 1-based line
numbers. "Not stated" means none of the 23 pages says it. Where only a page outside this folder makes a point, the pointer is
given as the 99 page cites it. That outside page was not audited for this report.

## Pages read

All 23 `.md` pages were read in full: 18,141 lines. The `.tsv` members were opened only to confirm layouts and row counts.

| NAME | path (under `99-Unresolved-Residual/`) | lines | status as the page states it |
|---|---|---:|---|
| README | `README.md` | 538 | category index; "**30 functions** … currently carry no classification at all" (`README:3`); lists only four systems (`README:135-156`) |
| GQ | `Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md` | 2040 | `status: AUDITED` (`GQ:4`), tier 1, `last_reviewed: 2026-09-02` (`GQ:21`), `reopened_count: 0` (`GQ:31`) |
| CBC | `Glyph-Run-Rendering/drawing-a-line-character-by-character.md` | 695 | `status: AUDITED` (`CBC:4`), `last_reviewed: 2026-09-03` (`CBC:19`) |
| RT | `Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md` | 498 | `status: AUDITED — the selection, its tree, …` (`RT:5`), two `parent_tag` values GN162 / GN159 (`RT:12`, `RT:19`) |
| PAINT | `Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md` | 855 | `status: AUDITED` (`PAINT:4`), `last_reviewed: 2026-09-03` (`PAINT:19`) |
| API | `Glyph-Run-Rendering/the-font-painters-public-api.md` | 372 | `status: AUDITED` (`API:4`) |
| CTX | `Glyph-Run-Rendering/the-shared-drawing-context.md` | 786 | `status: AUDITED — every register row is closed …` (`CTX:4`); body banner "**PARTIAL.**" (`CTX:35`) |
| DISP | `Glyph-Run-Rendering/the-text-element-dispatch-table.md` | 810 | `status: AUDITED — …` (`DISP:4`); body banner "**PARTIAL.**" (`DISP:37`) |
| CS | `Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md` | 1842 | `status: AUDITED` (`CS:4`), `last_reviewed: 2026-09-03` (`CS:20`) |
| DB | `Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md` | 726 | `status: AUDITED` (`DB:4`); body banner "⚠ REFUTED 2026-09-16 (FABLE)" (`DB:31`) |
| REF | `Unlisted-Code/referenced-code-the-list-never-had.md` | 363 | `status: DOCUMENTED — every register row is closed …` (`REF:4`) |
| CUT | `Unlisted-Code/the-bodies-the-list-cuts-short.md` | 267 | `status: AUDITED - 164 listed bodies are truncated …` (`CUT:4`) |
| UNL | `Unlisted-Code/the-code-the-function-list-does-not-contain.md` | 965 | `status: DOCUMENTED — every register row is closed …` (`UNL:4`) |
| BIG | `Largest-Unclassified-Code/the-largest-unclassified-functions.md` | 1640 | `status: DOCUMENTED — every register row the page names is answered …` (`BIG:4`); body banner "**`PARTIAL` deliberately.**" (`BIG:49`) |
| CENSUS | `Unowned-Code-Census/why-the-unowned-code-has-no-owner.md` | 1533 | `status: AUDITED` (`CENSUS:4`), `last_reviewed: 2026-09-02` (`CENSUS:21`) |
| U158 | `the-unresolved-158.md` | 1597 | `status: DOCUMENTED` (`U158:4`), `evidence_tier: 3` (`U158:6`), `readiness: CLASSIFIED` (`U158:8`), `confidence: HIGH` (`U158:9`) |
| RECT | `drawing-one-coloured-rectangle.md` | 340 | `status: AUDITED` (`RECT:4`) |
| MEASURE | `measuring-text-by-drawing-it-with-the-output-off.md` | 328 | `status: AUDITED — every register row is closed …` (`MEASURE:4`) |
| BLINK | `the-blinking-icon-and-its-atlas.md` | 598 | `status: AUDITED — both reservations closed 2026-09-18 …` (`BLINK:4`) |
| NINEP | `the-nine-patch-window-frame.md` | 453 | `status: AUDITED` (`NINEP:4`) |
| ICON2 | `the-second-icon-drawer-and-what-it-adds.md` | 305 | `status: AUDITED` (`ICON2:4`) |
| WBG | `the-widget-background-and-its-atlas-sets.md` | 283 | `status: AUDITED` (`WBG:4`) |
| WTREE | `the-widget-tree-draw-pass.md` | 307 | `status: AUDITED — every register row is closed …` (`WTREE:4`) |

(Line counts are `wc -l`. Several files have no final newline, so an editor shows one line more.)

Member files were checked for layout and counts only. No item below rests on a member file alone.

| file | what was checked |
|---|---|
| `residual-30-GN161.tsv` | 16 comment lines, header `address size old_tier band role disclaimed bare list evidence_page evidence`, **30 data rows**, all `band` = `DESCRIBED`, `0036A2A0` included (see C-V40) |
| `residual-109-classification.tsv` | 31 comment lines, header `address size band citing evidence role domain disp`, **109 rows** (65 `ENTRY-MENTION`, 44 `UNTOUCHED`). It includes `002A4830`, `002A4430`, `002AF960` and `00256CA0`, which U158 places in clusters, not among singletons (see C-V41) |
| `residual-crossref.tsv` | no comments, header `address size interior_cited pages`, **30 rows**, all `interior_cited=yes`, none with an empty `pages` (see C-S35) |
| `residual-order.tsv` | 3 comment lines, **139 rows**, tiers 1:12 / 2:12 / 3:32 / 4:83, addresses `00180A70`..`005DF890` (see C-V39) |
| `residual-30-GN161-stage1.tsv`, `vu-region-classification.tsv` | 30 and 210 rows. `vu-region-classification.tsv` agrees with README's 210-body run (`README:240`) |
| `Glyph-Run-Rendering/glyph-run-widget-1498-accesses.tsv` | header `function name site disp kind instruction route note`, 192 rows. **No page in the folder links it** |
| `Unlisted-Code/referenced-unlisted-blocks.tsv` | 143 rows, 6,038 B. Agrees with `REF:35`, `REF:43-45` |
| `Unlisted-Code/unlisted-code-blocks.tsv` | 1,471 rows, 244,619 B. 66 blocks / 177,977 B below `00160000`. Agrees with `UNL:33-36`, `UNL:240` |
| `Unlisted-Code/unlisted-body-admissions.tsv` | 1,471 rows: table 431 / body 874 / continuation **162** (3,418 B) / ambiguous **3** / covered 1. Agrees with `UNL:69-75`, not with `UNL:37`, `UNL:595-597` (see C-V47) |
| `Unlisted-Code/unlisted-entry-points.tsv` | 1,524 rows in 1,392 distinct blocks. Agrees with `UNL:670` |
| `Unlisted-Code/listed-bodies-with-code-past-body-bytes{,-rewalk-0929}.tsv`, `underrun-errata-rows-0929.tsv` | 177 / 164 / 159 rows. They agree with `CUT:4`, `CUT:86-100`, `CUT:175`. `0037C3F0`'s `code_ends` / `corrected_end` is `0037C6F8` (see C-V45). Neither file lists `0025E4C0` or `00301AD0` (see C-V44) |
| `Unlisted-Code/uc1-applied-population-*.tsv`, `uc1_apply_band_*.out` | 706 / 120 / 50 rows. `FAILS 0`. They agree with `UNL:862-868`, `UNL:891-894`, `UNL:924-927` |
| `Largest-Unclassified-Code/members/chain-b-resolve-fields.txt` | resolve counts for `004355D0` 76, `00437130` 77, `00438860` 239. They agree with `BIG:1460-1465` |
| `*.py` members | header comments only; not run |

---

## 1. Interface

**What this folder is.** The folder is not one engine system. It is a residual ledger (README, U158, CENSUS, UNL, REF, CUT,
BIG): four sets of code the classification left unexplained, measured and progressively read. Two kinds of page sit inside
it, and a port could take engine behaviour from both:

1. **Text and UI drawing.** A complete-looking text pipeline (GQ, CBC, RT, PAINT, API, CTX, DISP, MEASURE) and a widget,
   primitive and icon drawing layer (WTREE, WBG, RECT, NINEP, DB, BLINK, ICON2). The two layers share one drawing-context
   record (`[widget+0x38]`) and one immediate-mode batcher.
2. **Read-out systems found while reading the residue.** Cutscene name slots and the depth-of-field sidecar (CS). The
   render-model subresource binding machine and the effect mesh draw path (BIG). The libvpx VP8 SIMD and the unlisted script-verb
   tails (UNL, REF). The deferred-work queue and the message-window text engine (U158).

The ledger pages themselves (counts, denominators, dispositions) define no runtime behaviour. They are mapped in 1.6 only
for the per-function readings they carry.

### 1.1 Text pipeline — entry points (functions, with their callers)

| function | role as stated | callers as stated | cite |
|---|---|---|---|
| `0053E0B0` `Text_DrawScrolledWindowLines` (718 B) | cull, shadow pass, text pass, icon path per 32-byte window line record | "`0053E0B0` is called with the widget by its procedure `0053E380` (message 4, `0053E44B`; installed by `0053ED10`)" | `GQ:316`, `GQ:291-302`, `GQ:711` |
| `002D8690` / `002D87D0` (306 B each) | select renderer by `ex` prefix; modulate colour by window intensity `(channel * intensity) >> 7` | `0053E0B0` (as the call chain draws it; see C-V9) | `GQ:325-326`, `GQ:517`, `GQ:547-550` |
| `00364980` `Text_IsExPrefixed` (28 B) | returns 1 iff the record's first two bytes are `'e'`,`'x'`; null `rcx` returns 0 | 11 callers / 12 sites listed | `GQ:321`, `GQ:660-663`, `GQ:1831` |
| `003649A0` `Text_EmitGlyphRunQuads` (3,020 B) | the `ex` (UTF-16) arm: pen walk, glyph cache, 16-byte GS command records | `0053E0B0`; also "a single caller (`002DD5D0`)" per PAINT | `GQ:313`, `GQ:567`, `GQ:690-693`, `PAINT:238-239` |
| `002B0280` (6,441 B) | the byte-charset renderer (records **not** `ex`-prefixed, corrected 2026-09-25); arms `01E0CDF4` | `002D8690`/`002D87D0` | `GQ:327`, `GQ:674-675`, `CBC:137` |
| `003647E0` `Text_HandleControlCodes` (366 B) | control codes 1, 2, 3, the two spaces, the `{` entry (code meanings disagree; C-V1) | `003649A0` (`00364B58`) | `GQ:317`, `GQ:270-277`, `GQ:1777-1787` |
| `00366110` `Text_InterpretBraceTag` (1,318 B) | eleven `{x}` tags; 22-dword jump table `00366638` | `003647E0` | `GQ:244-256`, `GQ:314`, `GQ:337` |
| `00364530` `Text_MeasureGlyphRun` (684 B) | non-drawing advance/extent measurement | 12 call sites (see C-V12 on whether it draws) | `GQ:315`, `GQ:1481` |
| `00365FD0` / `00364210` | glyph cache promote-on-hit / fill-on-miss (roles disagree; C-V2) | `003649A0` | `GQ:318-319`, `GQ:1788-1789` |
| `002AF960` (1,117 B) | opens and closes a run; seeds `+0x10D8`/`+0x10DC`/`+0x10E4`; slot-2 dispatcher `call qword ptr [rdi + r9*8 + 0x7F64D0]` | `002A4430`, `002A4830`; sites `002A4541`, `002A4B3E`, `002A4E2E`, `002D8620` | `GQ:783`, `CTX:375-385`, `DISP:316-323`, `DISP:603`, `U158:524` |
| `002AAE40` (2,440 B) | the per-character walk: control codes to the interpreter, everything else to the font painter; flushes `002B4730(1)` every 20 queued items | no `rel32` caller; one quadword at `00916518`, slot 2 of kind 3 in table `009164C0` | `CBC:31-33`, `CBC:185-192`, `CBC:312` |
| `002A9F00` | the kind-0 glyph emitter; tests `+0x10DC`, decrements the counters | `002AC5F0` (four sites), dispatch table | `GQ:773`, `CTX:393-413`, `DISP:381-386` |
| `002AC5F0` (7,489 B) | control-code interpreter, GN162 `UI.Text.ControlCodeInterpreter` (status disagrees; C-S20) | seven callers (counts disagree; C-V20) | `DISP:43`, `U158:216`, `DISP:285` |
| `002B2150` (861 B) | line measurer, GN162 `UI.Text.MeasurePass`; nulls `0209CC48` around the walk (whether it draws disagrees; C-V13) | `002AC5F0`, `002AF340`, `002AF960`, `002AAE40`, `002B2DF0`, `002B5390` | `MEASURE:228`, `MEASURE:298-299`, `MEASURE:326` |
| `002AF340` (1,563 B) | block measurer; returns the character count to the stop string, or −1 | `002ABB20` | `MEASURE:146`, `MEASURE:229` |
| `002ABB20` / `002ABF70` | scroll step (installs stop string `00916548`) / reveal stepper, eight modes via table `002AC1B4` | `002ABF70` → `002ABB20` | `MEASURE:230-231`, `MEASURE:288` |
| `002B3930`, `002ABF20`, `002ABEC0` | column 0 / 1 / guarded-1 dispatchers into table `009164C0` (4 rows × 3 qwords) | 2 / 3 / 5 callers (see C-V21) | `DISP:79-86`, `DISP:100-138` |
| `002B4730` (218 B) | render-buffer swap: appends a 16-byte record, header `0x6c008150 \| count<<16`, submits via `003A1DB0` | 7 callers | `CBC:303-312`, `CTX:224-242` |
| `002B3550` (69 B) | the only writer of `0209CC40`: `memset(0209D490, 0, 0x1108)` | **not stated** ("at startup", `CTX:32`) | `CTX:53-61` |
| Font painter API `0017F650`–`0017FD30` | 18 entry points → `001E8070`, `001E8580`, `001E93C0`, … `001E9D20` (count disagrees; C-V22) | callers per entry, tier 2 | `API:55-74`, `API:370` |
| `001E8580` (3,572 B) | flush: ladder chooser, offscreen passes, composite | only `0017F850` | `PAINT:34-39` |
| `001E8070` (1,293 B) | glyph emitter: six `0x3C`-byte vertices per glyph, 28 fontclut palettes | `0017F7C0` | `PAINT:32-34`, `API:58`, `PAINT:453-468` |
| `001E9D20` (472 B) | render-target selection by `key = (b << 32) \| a` | wrappers `0017FD00` (b = 2) and `0017FD30` (b = 0/1) | `RT:35-60`, `RT:91`, `RT:287-288` |
| `0017FA10` → `001E9920` | per-frame begin; resets both 44-byte records and the alpha pair to `1.0f` | "Eleven sites in seven functions" (six named; C-V25) | `PAINT:172-192` |

### 1.2 Text pipeline — inputs, outputs and record layouts

- **Text record.** "first four bytes are a header the renderers skip; the characters begin at `+0x04` and are **16-bit,
  NUL-terminated**" (`GQ:121-122`). An `ex` record is "`ex00` followed by UTF-16LE text" (`GQ:674`). The byte path: "a byte
  at or above `0x20` is glyph byte − `0x20`; a lower byte selects a page through a 16-entry table and combines with the next
  byte" (`GQ:694-695`).
- **Tags.** "`{` is a `u16` `0x007B`, bodies are `{letter:1B, args:nB}` closed by a `u16` `0x007D`" (`GQ:728-729`). Eleven tags are
  tabled at `GQ:244-256`. Control codes are tabled at `GQ:270-275`, but that table conflicts with the subtree table (C-V1).
- **`TextState`** (`GQ:357-387`): `+0x00` masterScale f32, `+0x04` scaleX, `+0x08` scaleY, `+0x0C` rotation, `+0x20` matrix
  pointer, `+0x28` text record, `+0x30..+0x33` colour RGBA, `+0x34` saved colour, `+0x38`/`+0x3C` pen x/y, `+0x40`/`+0x44`
  glyph w/h, `+0x48`/`+0x4C` overrides, `+0x50` yOffset, `+0x54` depth, `+0x56` needsFiltering, `+0x58`/`+0x5A`/`+0x5C` box
  origin/width, `+0x60` fontId, `+0x61` palette (biased `0x20`), `+0x62` trailing-trim flag, `+0x63` flags bit 0. Total size
  **not stated**.
- **`GlyphTableRecord`** (12 B): `+0x00` u16 code, `+0x02` cellWidth, `+0x03` cellHeight, `+0x04` advanceWidth, `+0x08` u32
  pixelOffset. The table is at `[022CBE00 + 0x10 + fontId*8]`: count at `+0x04`, records from `+0x10` (`GQ:389-401`). "Bytes
  `+0x05`–`+0x07` remain unread by any function here" (`GQ:764-765`).
- **`GlyphCacheNode`** (`GQ:424-434`): `+0x00` next (head `[022CBE00+0x230]`), `+0x08` prev (tail `[022CBE00+0x228]`), `+0x10` char,
  `+0x12` fontId, `+0x13` resident, `+0x14`/`+0x15` texture w/h (power of two, ladder `<9→8 … else 128`, `GQ:440-444`),
  `+0x18` pixels, `+0x20` glyph record. Node count and pool: **not stated**.
- **GS command records** (16 B), codes `0x3F`, `0x42`, `0x47`, `0x08`, `0x06`, `0x14`, `0x00`, `0x01`, `0x03`, `0x05` (`GQ:162-173`).
  Corner order is TL, BL, TR, BR (`GQ:176-178`). UV: `U_min = V_min = 8`, `U_max = (int)((cellWidth + 0.0f + 0.5f) * 16.0f)`
  (`GQ:454-456`). Pen: `penX += advanceWidth(glyph) * scaleX`; `scaleX = sx / 100.0f; scaleY = (sy != 0) ? sy / 100.0f : 1.0f`
  (`GQ:499-506`). Submit-and-swap past `0x180` records (`GQ:539`).
- **160-byte glyph record** (font painter side; `API:93-102`, `CBC:98-111`): `+0x00` source U ×2, `+0x08` source V ×2, `+0x10`–`+0x1B`
  "three dwords — **not established**", `+0x1C` / `+0x2C` screen X / Y per corner, `+0x3C` / `+0x4C` "four floats each — **contents
  not established**", `+0x5C` / `+0x6C` / `+0x7C` per-corner colour weights, `+0x8C` per-corner alpha (`0x80` = 1.0), `+0x9C`
  palette index mod 28 (but see C-V28).
- **Font painter object** `[01F811F8]` (`PAINT:46-55`): batches `+0x70`, matrix `+0xE30`, palettes `+0x1358`, corner multipliers
  `+0x137C..+0x1388` (`API:110-122`), `+0x1390` (always `0x44`), `+0x1398` handle, `+0x13A0` "shared render parameters", ladder
  slots `+0x13C0`, 64-slot target cache `+0x1500`, two 44-byte records at `+0x2320` (stride `0x2C`, fields `PAINT:137-151`),
  `+0x2378` outer gate, `+0x2379` mode selector. Object size `0x2380` (`RT:300`). Render-target state map: `RT:209-220`, `RT:290`.
- **Ladder table** `009018F0`: "10 pairs of `int32`", 50×60 … 1920×1080, chooser `while (table[i].w <= box_w || table[i].h <= box_h)`,
  overflow returns 9 (`PAINT:88-119`).
- **Vertex output** of `001E8070`: `0x3C` bytes, `u = x / texture_width`, `v = (texture_height − y) / texture_height`, colour
  `fontclut_channel × per_corner_value × (1/128) / 255.0`, palette `[param_2 + 0x9C] % 0x1C` (`PAINT:453-468`). The third float
  "was **not** resolved" (`PAINT:549-550`).
- **Shared drawing context** `0209D490` (`0x1108` B, pointer `0209CC40`; `CTX:53-88`). The 24-offset field map is at `CTX:76-88`.
  `+0x10C8` stop-set pointer, `+0x10D4` batch counter (flush at `0x14`), `+0x10D8` progress counter, `+0x10DC` full-alpha count,
  `+0x10E4` fade fraction, `+0x10E8` line height, `+0x10FC` three-state byte, `+0x10FF` measuring byte, `+0x1102` line-start
  flag (`GQ:1663-1743`, `CTX:281-308`, `MEASURE:53-99`). `+0x000` and `+0x400` are row tables (`CTX:107-129`, `CTX:149-184`).
- **Render buffer.** `0209CC48` is the current 24-byte record in table `02EBEFC0`, indexed by `02EBEFF0`. `0209CC50` is the write cursor,
  descending in 16-byte steps. `0209E5A0` is the buffer base (`CTX:227-249`).
- **Text-element block** (the element a dispatcher indexes): `+0x44` flags, `+0x8C` word (default `0x7D00`), `+0x90` word, `+0x9D`
  s8 fade length, `+0xA3` kind byte (selects the dispatch row), `+0xAC` guard byte (`DISP:101-128`, `CTX:378-387`). Full size:
  **not stated**.
- **Message-window records.** `TextLayoutRecord` array `0209C700`, stride `0x28` (`U158:553-561`). Window fields `+0x3BE`
  scroll, `+0x3C0` cursor, `+0x3C1` row total, `+0x3C2` count, `+0x3C5` input wait (`U158:243`). The page-history stack is
  16 × 40 B (`GQ:865-877`).
- **Compiled line stream** (`002AAE40` family). GQ says "`0x00` ends, `0x02` is an inline marker, `0x03` is a line commit, `0x10`–`0x1F` are
  two-byte object references and `>= 0x20` one-byte object references" (`GQ:833-835`). CBC disagrees (C-V14). The message table
  entry is `{u16 streamOffset relative to table, u16 flags}`, flag bit 0 = suppress (`GQ:1090-1107`).

### 1.3 Widget, primitive and icon drawing — entry points

| function | role as stated | callers as stated | cite |
|---|---|---|---|
| `00245E60` (1,416 B) | recursive widget-tree draw; gate `(node.flags & 0x405) != 5` → return | brackets `002450B0` (pass 0, "MainLoop_Draw and twelve sites") / `00245110` (pass 1, from `00252990`); root `0208EC90` | `WTREE:32-75`, `WTREE:199-214` |
| `00245170` (927 B) / `002455A0` (2,232 B) | background drawers, chosen by flag bit 8 (bit 7 set, bit 24 = pass) | `00245E60` | `WBG:31-32`, `WBG:160-167`, `WTREE:183-192` |
| `002DA7C0` (1,193 B) / `002DA2D0` (1,262 B) | textured quads; exclusive vs inclusive far edges; mode `d & 3` vs literal `2` | the background drawers | `WBG:183-202`, `WTREE:158-175` |
| `002DBDD0` | tinted rectangle, GN161 `Presentation.Primitive.TintedRectangleQuadEmit` | "Seven callers: `00241D40`, `002B8EE0`, `002BCA70`, `002BCB00`, `002C9120`, `002C9570`, `003C32B0`." | `RECT:31`, `RECT:192` |
| `00392A00` (12 B guard) → `00392A10` (707 B) | nine-patch dispatcher; `cmp word ptr [rcx + 0x58], 0` / `jne 00392A10` / `ret` | guard callers `002A62EE` (in `002A6190`), `002C0967`, `002C0E5E`, `00574056`; `rcx` = `[widget+0x38]` | `DB:38-57`, `DB:431`, `NINEP:109-117` |
| `00392CE0` (589 B) | fallback when `002DD4B0() == 0` (one quad vs nine slices disagrees; C-V5) | `00392A10` only | `DB:241-252`, `NINEP:103`, `NINEP:139-145`, `CS:1553` |
| `002DC7F0` (2,194 B) | one nine-patch cell: one quad, or two quads split at the centre (`flags & 8`) | `00392A10` ×9 | `NINEP:183-213`, `DB:455-462` |
| `002DC290` (1,363 B) | gradient quad, GS words `0x1000000000000002`, `0x2026400000008004`, `0x41` | 11 callers (not listed) | `NINEP:159-172`, `NINEP:247` |
| `002DD1E0` / `002DD090` | open / close the nine-slice batch (`002DD090` role disagrees; C-V7) | `00392A10` | `DB:243-245`, `DB:468-470`, `CS:1551` |
| `002DD4B0` (7 B) | returns `[0215E6D0]`, the draw-bracket-open flag (set by `002DD4C0`, cleared by `002DD4A0`/`002DD420`) | ten raw sites listed at `DB:449-451` | `DB:447-451`, `WTREE:258`, `CS:1459-1469` |
| `002B8EE0` (2,865 B) | pulsing icon from atlas or resource | `002B9A20` once per marker node, from track-map page procedure `002B7B80` | `BLINK:31`, `BLINK:298-299`, `BLINK:435` |
| `002BCB00` (2,703 B) | twin icon drawer (location map) | "reached through their own caller" | `ICON2:31`, `ICON2:158`, `BLINK:300-301` |
| `002DD7E0` | palette / fontcolor face colour getter (role disagrees; C-V18) | 88 callers | `BLINK:107-117`, `BLINK:288` |
| `00181560` … `00181460` … `00181330` | immediate-mode batcher (begin, colour, strip-to-list, flush to a `DynGeoTextureInstance`) | `002DBDD0`, `002DC290`, others | `RECT:125-127`, `RECT:140` |

### 1.4 Widget and primitive drawing — inputs, outputs and record layouts

- **Drawing context `[widget+0x38]`** (a 0xA0-byte stack record built by `002D8C00`; `DB:431-433`):
  - `+0x48` box, with `+0x4C`/`+0x4E` the extent (`ICON2:104`, `ICON2:193`);
  - `+0x50`/`+0x52` origin (`RECT:247`);
  - `+0x58` alpha scale and `+0x5A` brightness, both words with `>> 7` (`RECT:63-91`, `NINEP:130-132`);
  - `+0x5C` palette (`BLINK:78`);
  - `+0x70` vertex third component (`RECT:123`);
  - `+0x78` and `+0x80` the ALPHA_1 and TEST_1 values (`RECT:138`);
  - `+0x90..+0x93` RGBA and `+0x94` packed tinted colour (`RECT:64-67`).
- **Composition rule.** "root `+0x58` = node byte `+0xA0` (`00245EF0`); child `(parent +0x58 * +0xA0) >> 7`" (paraphrase of `DB:435-437`).
  The constructor `002465F0` sets `+0xA0 = 0x80` (`DB:438`). Brightness is `(node[+0xA1] × parent[+0x5A]) >> 7` (`WTREE:153`).
- **Widget node**: `+0x00` handler, `+0x10` definition, `+0x18` first child, `+0x20` next sibling, `+0x38` context, `+0x40`
  flags, `+0x50` typed list, `+0x8C` scale, `+0x9C`/`+0x9E` own size, `+0xA0` alpha, `+0xA1` brightness, `+0xA3` style,
  `+0xA6`/`+0xA7` (`WTREE:59-214`, `NINEP:131-132`, `WBG:76-77`, `WBG:232`). The node position fields and total size are **not stated**.
- **Flag bits** (node `+0x40`). The gate needs bits 0 and 2 set and bit 10 clear. Bit 7 is the background gate, bit 8 picks the drawer,
  bit 12 gates message 5, bit 21 scale, bit 24 = pass, bit 28 clear for messages 3/4, bits 22 and 26 select atlas and colour table
  (`WTREE:52`, `WTREE:113-114`, `WTREE:136`, `WTREE:192`, `WBG:127-167`).
- **Nine-patch inputs**: BoxRect `short[8]` = origin x/y, total w/h, left/right column widths, top/bottom row heights. CornerColours
  are four u32, TL/TR/BL/BR (`DB:302-316`, `NINEP:57-62`). The split rule and the corner blend disagree between pages (C-V3, C-V4).
- **`ImmediateVertex`** (0x30 B): `+0x00` x,y,z,w floats, `+0x10` four int32 channels (`0x80` = 1.0), `+0x20` u,v, `+0x28` flags word
  (`DB:455-460`). The batcher holds 64 batch slots of `0x58` at `+0x2328`, index at `+0x3928` (`RECT:140`, `NINEP:299-302`).
- **GS packet** of `002DBDD0`. It is `0x90` bytes. The GIF tag `0x1022400000008004` reads "NLOOP 4, end-of-packet and a PRIM of triangle strip, flat
  shaded, alpha blending on, texturing off; **the `4` beside it is the register list - XYZF2 - not a vertex count**" (`RECT:109-123`,
  `RECT:138`; see C-S29). "**So the rectangle is described twice and drawn once.**" (`RECT:142`)
- **Icon atlas** (`BLINK:68-100`): `atlas = *(*(param_5 + 8) + 0x20)`; header `+0x40` entry array, `+0x42` palette remap, `+0x44` index table;
  8-byte entries with `u = entry[+4] & 0xFFF`, `v = entry[+4] >> 12 & 0xFFF`, `pal = entry[+7]`; sentinel `record + 0x20 == 0xFF`.
  Pulse: `sinf((DAT_0208F570 * 3.1415927f) / 30.0f)` (`BLINK:47`); `0208F570` counts 60 Hz ticks (`BLINK:287`).
- **Background descriptor**: `((((v1 << 10 | v0) << 10 | u1) << 10 | u0) << 4) | 10` (`WBG:88-97`). Colour tables `00915208` (3×4) and
  `00915218` (9×4). Colour = `002DD7E0(style * 4 + 0x2C + selector)` (`WBG:130-155`).

### 1.5 Cutscene name slots and the depth-of-field sidecar (CS)

- **Entry**: `0020AC30` `CutsceneSlot_SetNameAndClassify` (572 B), GN162 `Resource.CutsceneAssetSlot.NameClassifyingSetter` (`CS:184`).
  Callers: "`ActorResource_BeginManagerResourceSetLoad   0032FCA0` -> `thunk_FUN_0020ac30  001EC660   5 bytes, one JMP` -> `0020AC30`"
  (`CS:72-74`). That loader is reached from `World_UpdateSimulationTick` → `WorldSimulation_ProcessDeferredModeRequest(0, id)`
  (`CS:1729-1731`). Other slot entry points `001EC520`, `001EC540`, `001EC620`, `001EC680`, `0020A760`, `0020AF10` (`CS:535-541`)
  are called by ScriptVM handlers (`CS:1786`).
- **State**: 5 × 32-byte `SlotRecord` at `0x01F832F0` (`+0x00` begin, `+0x08` end, `+0x10` capacity, `+0x18` allocator; `CS:225-229`).
  `PerSlotFlag` at `0x01F832B0` (`CS:231-232`). Flag A `01F832E8` is set when a `sum_` name contains `0001`; flag B `01F832E9` when a
  non-`sum_` name contains `spc_` (`CS:206-207`). Current-slot latch `01DFE40C`, whose ".data value is `0xFFFFFFFF` (none)" (`CS:531-532`).
  Initial values of the records and flags: **not stated**.
- **Order inside `0020AC30`**: bounds check → latch → build name → change guard (length, then `memcmp`) → release old entry → assign →
  `length > 3` then `sum_` / `0001` / `spc_` tests → `.json` load (`CS:82-138`, `CS:235-264`). The latch order disagrees (C-V31).
- **Sidecar**: `JsonData/CutScenes/<name>.json`, keys `mDofFocusDistance`, `mDofApertureFnumber` (`CS:151-154`), loaded by `001C5750`
  `CutsceneDof_LoadSidecar` (`CS:187`). Sections are `Common` plus `Cut 1` … `Cut 61`, 116 distinct keys (`CS:448-455`). PresetDof
  composition is at `CS:471-477`. Where `001C5750` stores the two values: **not stated**.
- **Consumers**: `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState` gates the script stop marker `entry[0x16]` (`CS:198`,
  `CS:708-757`). The stand-down gate is written out in full at `CS:895-905`. `001ED130`:
  `return !( fieldVar == 0x19 || (fieldVar == 0x10C7 && slotFlag == 5) );` (`CS:847`). Its operand is story progress, not a field id
  (corrected `CS:1715-1723`; C-S16). Skip bitmask byte `+0x201` of the 0x288-byte manager record (`CS:1086-1096`).

### 1.6 Systems read out of the residue

- **Render-model subresource binding machine** (BIG). Dispatchers `003CCF20` (887 B, bind) and `003CD2C0` (688 B, release) walk work list
  `[0x02B47778]`. They dispatch on byte opcode `[rec+0]` through 8-entry tables `003CD298` / `003CD570`. Opcodes 1–8 map to `0050AC20`,
  `00506B40`, `005080A0`, `0050A100` (via `003CD840`), `00509BB0`, `00507490`, `00508C90`, `00507120` (via `003CD840`) (`BIG:697-713`,
  `BIG:1303-1312`, `BIG:1366`). The eight operations are palette (CLUT) animation effects on an 8.8 fixed-point colour table
  (`BIG:928`). Which opcode is which effect: **not stated**. `003CD840` (21,276 B) and `003D2B60` (20,710 B) are translated PS2 MMI kernels over the
  EE/VU0 register bank `022D8F10`–`022D94A0` (`BIG:286-312`). Init `003CD6E0` allocates a 32 × 64 B handle table and a
  128 × 0x50 B pool (`BIG:795-811`). Handle `= (gen<<8)|index` (`BIG:890`). Entry and pool layouts: `BIG:905-923`. Chain A
  callers: `00258E40` from `MainLoop_UpdateAndRenderFrame` (`0022B8C0`), `00258D70` from `0022A770` (`BIG:1563`).
- **Event-effect load table** `022D94B0` (32 × 24 B; `BIG:1162-1183`) and the typed-handle layer `0024Cxxx`. Class nibble `>>28`:
  1 = magic-effect files, 5/6/9 = presentation records, 7 = event-effect loads, 8 = screen-effect descriptors (`BIG:1187-1231`).
- **Effect element type `0x05` mesh draw** (chain B): `002F4020` → `00449AB0` → `004355D0` → prep `00434CD0`/`00435050` → `00438860`
  (VU0 path, `+0x1F1` bit 7) / `00437130` / inline (`BIG:1395-1401`). The kind-`0x54` mesh record is at `BIG:1413-1426` and the `+0x1F1`
  builder at `BIG:1492-1496`.
- **libvpx VP8 v1.6.0** (UNL). 63 of the 66 head-of-`.text` blocks are byte-matched hand-written SIMD, 159 routines (`UNL:446-449`).
  The rtcd setups `0016F080` and `00172580` fill eight pointers at `02F974F0`–`02F97528` (`UNL:443`). UC-2 answers that the 63 heads are
  dead (`UNL:443`). The routine names live in `uc3-blocks.tsv` outside this folder.
- **Script-verb tail bodies** (REF). Fourteen unlisted bodies are reached by a tail `jmp` from listed thunks (`REF:61-76`), with their verb
  mappings (`REF:225`). They include system-stop release `0025B500`, which recomputes `[02099DB8]` from three stop flags (`REF:255-269`), and
  the party-focus request byte `022C7FF8` (`REF:245-251`).
- **Deferred-work queue drain** `0024B580` (U158): queue head `[02092170]`, link `+0x348`, kind byte 1..9, jump table `0024B6C4`
  (`U158:1300-1372`). "What the nine kinds *are* … are **not read here and are not claimed**" (`U158:1360-1365`).
- **CENSUS readings.** The census page identifies shared unowned helpers:
  - `00584730`, a null-guarded aligned free (`CENSUS:226`);
  - `00811130` `lua_settop` and `008119F0` `lua_type` (`CENSUS:227-261`);
  - `00244F50`, the 112-record UI widget allocator (`CENSUS:287-310`);
  - the Skin registry callbacks (`CENSUS:1237-1272`);
  - the authored-command table `01EFFAF0` (`CENSUS:1389-1406`).

### 1.7 State (globals and objects, with lifetime)

| state | what the pages say | lifetime / initial value | cite |
|---|---|---|---|
| `0209CC40` → `0209D490` | shared drawing context, `0x1108` B | "one value for process lifetime"; zeroed once, "every field's initial value is 0 and nothing re-initialises it" | `CTX:65-67` |
| `0209CC48` / `0209CC50` / `0209E5A0` | current render-buffer record / cursor / base | writers and readers counted (`CTX:246-249`); what a dispatch does to `0209CC48` disagrees (C-V16) | `CTX:227-249` |
| `[01F811F8]` font painter | object of `0x2380` B, created by `001B5F10` | "drawn once per frame"; `+0x2378`/`+0x2379` are 0 at construction | `PAINT:55`, `PAINT:167`, `RT:300-301` |
| `022CBE00` font layer | glyph tables, cache list, shared matrix `+0x1E0`, font slot mask `+0x240` | table pointers fixed up by `00366080`; mask writer and initial value **not stated** | `GQ:391-426`, `GQ:522-526`, `GQ:757-758` |
| `01E0CDF4` | screen-width counter | "starts at exactly `1.0`", armed at `002B034D` | `CBC:134-141` |
| `0208F570` | 60 Hz tick counter | advanced per presented frame by `00184950()` (1–3); re-based on message 18 | `BLINK:287` |
| `0208F564` | widget pass index (0/1) | set by the brackets; value outside them **not stated** | `WTREE:199` |
| `0215E6D0` | draw-bracket-open flag | set to 1 only when bracket-open `0x10000000` was submitted; initial value **not stated** | `DB:447`, `CS:1459-1469` |
| `0215E6B8` / `0215E6C8` | fontcolor count / pointer | null except in the `ch` and `in` locales | `BLINK:108`, `BLINK:288` |
| `01F832F0`, `01F832B0`, `01F832E8/E9`, `01DFE40C` | cutscene slots, flags, latch | latch ships `0xFFFFFFFF`; others **not stated** | `CS:204-208`, `CS:531-532` |
| `02B47770`…`02B477A0` | binding-machine state block (56 B) | allocated lazily by `003CD6E0`; generation counter's initial value **not stated** | `BIG:798`, `BIG:888-889`, `BIG:960-968` |
| `022D94B0` | event-effect load table | constructor `0036E320` | `BIG:1073` |
| `02092170` | deferred-work queue head | **not stated** | `U158:1308` |
| `022C7FF8`, `02099DA0`, `02099DB8` | party-focus request kind / one-shot byte / system-stop total | `02099DA0` reset to 0 by `00266D10` at `00266DF7` | `REF:241-266` |

### 1.8 Order (what runs when in a frame, and what triggers it)

- **Widget draw.** `002450B0` (pass 0) and `00245110` (pass 1) bracket a recursive walk of root `0208EC90`. Per node: gate → transform/clip →
  background → message 3 → content → message 4 → `002435C0` → children → message 5 (`WTREE:52-56`, `WTREE:81-86`, `WTREE:114`,
  `WTREE:192`, `WTREE:209-214`). The order of the two brackets within a frame: **not stated**.
- **Font painter.** At each call site `0017F850` (draw last frame's accumulation) precedes `0017FA10` (begin) (`PAINT:204-208`). The flush tests
  `+0x2379` then `+0x2378`, then takes one of three paths (`PAINT:357-421`). Whether anything sets `+0x2378`: "**Whether anything sets `+0x2378`
  at all**" (`PAINT:546-547`) is open.
- **Message window.** `002A6190` case 1 registers the window in `0209C4D0`. Case 4 is the per-frame update, choosing `002A4830` when `+0x3E8 & 0x700`,
  else `002A4430` (`U158:823-852`, `GQ:882-884`).
- **Reveal and scroll.** `002ABF70` → `002ABB20` → `002AF340` → interpreter / measurer (`MEASURE:238-244`). "how often the stepper is called per
  frame is not traced" (`MEASURE:215`).
- **Per glyph.** `002A9F00` tests `+0x10DC`, then decrements both counters (`CTX:393-413`). `002B4730(1)` runs every 20 queued items
  (`CBC:312`, `GQ:841`).
- **Cutscene slots** run on resource-set load / map transition (`CS:275`, `CS:1725-1733`). The stop marker is consumed on the next pass of
  `0025DF00` (`CS:712-757`).
- **Binding machine.** Per pending entry, the dispatcher runs the operations, then the tail `003D2B60` (`BIG:167-168`, `BIG:1367`). `0036E1E0` runs per
  tick from `World_UpdateSimulationTick` (`BIG:1176`).

### 1.9 Dependencies (on other systems)

- **00-Engine-Core**: shared transform workbench `022D8F30`–`022D8F6F` and the EE/VU0 register bank (`BIG:158`, `RECT:267-273`). Per-frame gate
  and scheduling (`WBG:254`, `DISP:151`).
- **16-UI**:
  - widget object model, constructor `002465F0` and the message protocol (`WTREE:99-105`);
  - request router (`DISP:229-230`, `MEASURE:183`);
  - numeric formatting and character mapping (`GQ:281`, `DISP:689`, `U158:39`);
  - map screens (`BLINK:297`).
- **17-Presentation**:
  - render command submit `003A1DB0` (`CTX:234`);
  - VIF1/VU1 layer (`U158:249`);
  - effect element type dispatch (`BIG:327`);
  - graphics-thread handshake (UQ-211, `RECT:138`).
- **02-Resource**: authored-data registry `02EBF000` (`CTX:259-263`) and `ImageAddress_ResolveRuntimePointer` (`BIG:264`; role disputed, C-V8).
  Kind-7 loader `0029CED0` for `fontcolor.bin` (`BLINK:288`).
- **01-Script-VM**: verb handlers that tail into REF's bodies (`REF:225`). Dispatch table `01EED720` (`CS:806`).
- **04-Actor / 06-Movement / 11-Party**: actor storage record, movement context, party focus (`REF:225-251`).
- **23-Third-Party**: libvpx (`UNL:445-453`); Lua (`CENSUS:269`).
