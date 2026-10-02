# Reconstruction readiness — `FFXII TZA/99-Unresolved-Residual/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-99-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `f26c5667` only; no executable, Ghidra, extracted data or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** **23 pages read in full** (`README.md` + 22 system pages; 18,141 lines). 18 `.tsv` members and 2 `.out` files were checked for layout and counts only; `.py` headers only.

- **Interface:** 38 entry-point rows mapped (24 text pipeline, 14 widget, primitive and icon), plus cutscene, binding-machine, effect, libvpx, verb-tail and queue summaries.
- **Gaps:** 21 self-stated open items (G-1–G-21) and 21 structural gaps (S-1–S-21).
- **Contradictions:** 125 in all.
  - **67 value-changing** (C-V1–C-V67): 53 [engine], 14 [ledger]. All are "page-text only - needs local check". 3 have a favoured side settled by a dated correction (C-V31, C-V51, C-V66); 64 have none.
  - **58 stale or banner** (C-S1–C-S58). 3 of these have a favoured side (C-S16, C-S29, C-S40).
- **Checks:** 9 cross-checks found consistent. Every quotation was checked string-for-string against the snapshot (about 470 checks, 0 misses).
- **Rating: NOT YET** overall. Widget tree, rectangle, icons, cutscene slots and the verb tails are MOSTLY. libvpx is READY as a dependency. The text pipeline, nine-patch frame, binding machine, effect mesh draw and deferred queue are NOT YET. The ledger pages are not a port target.

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
| `0053E0B0` `Text_DrawScrolledWindowLines` (718 B) | cull, shadow pass, text pass, icon path per 32-byte window line record | "`0053E0B0` is called with the widget by its procedure `0053E380` (message 4, `0053E44B`; installed by `0053ED10`)" | `GQ:316`, `GQ:291-302`, `GQ:710-711` |
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
  Corner order is TL, BL, TR, BR (`GQ:176-178`). UV: `U_min = V_min = 8`, `U_max = (int)((cellWidth  + 0.0f + 0.5f) * 16.0f)`
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
  128 × 0x50 B pool (`BIG:795-811`). "handle = (gen << 8) | index" (`BIG:890`). Entry and pool layouts: `BIG:905-923`. Chain A
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

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open on the snapshot)

Only items no later dated section on any page answers. Items that one page states as open and another page answers are
listed under 3.2 as stale.

| # | open item (quoted) | cite |
|---|---|---|
| G-1 | `ex` coverage: "*Not established:* the other eight languages' files (only `us` was read); which runtime-composed strings carry the prefix" | `GQ:703-705` |
| G-2 | Shadow pairs: "**Not established:** whether an owner rewrites the pairs through the widget pointer after init." / "What the `1.0f` beside each pair scales is also not read." | `GQ:720-724` |
| G-3 | Glyph metrics: "Residual: advance-width vs ink-width is not separated" | `GQ:765-766`, `GQ:418-419` |
| G-4 | "the field-level detail of `002AAE40`'s descriptor packing, `002A8C50`'s flush modes `4`/`6`" belong to UQ-367, which was superseded rather than answered (`GQ:1239`) | `GQ:848-850` |
| G-5 | Full-alpha count: "the authored source of the full-alpha count is suggested, not established." | `GQ:1732-1733` |
| G-6 | Render target: "nothing here says what block 0 is drawn to"; the tree's left/parent-link tension: "**The bytes do not settle it**" | `RT:193`, `RT:319-324` |
| G-7 | Font painter: `+0x1398` "**What the field holds is not established.**"; "**Whether anything sets `+0x2378` at all**"; "What the third float of each vertex holds"; "**What the consequence is on screen is not established**"; record bytes `+0x2A`–`+0x2B` "untouched by anything found" | `PAINT:257`, `PAINT:546-550`, `PAINT:540`, `PAINT:151` |
| G-8 | API: `0017FD00`'s fourth register "**not established**"; glyph record `+0x10`–`+0x1B` "three dwords — **not established**", `+0x3C`/`+0x4C` "**contents not established**"; `001B1620` "**What that predicate tests is not established.**" | `API:84-86`, `API:97-99`, `API:197-198` |
| G-9 | Shared context: §3's 24 offsets "**not re-derived**"; a receiver touching only offsets below `+0x10C8` is not covered | `CTX:731`, `CTX:599-602` |
| G-10 | Dispatch: "**A label this correction touches, and does not settle.**" (`001EDEC0`'s reading on the shared-dialogs page) | `DISP:265` |
| G-11 | Cutscene: "*Not established:* the player-facing name" (and which `sum_` letter is which Esper); "Which story beats those values mark is not established."; `entry[0x16]` "Whether anything outside this function reads it was not established."; world state `param_1[5]` "its meaning is not established here"; "**What the `01F82E38` / `01DFE0C0` mode is.**"; `001EC560`, `00265760`, `002E0540`, `0022A030`, `0022A080` "remain opaque"; "The rest of the 648-byte record."; "**Not claimed:** why the matrix is mirrored into the emulated register cells" | `CS:355-356`, `CS:406`, `CS:772-776`, `CS:919-921`, `CS:1175-1176`, `CS:1505-1506` |
| G-12 | Nine-patch: "**Not read here:** which widgets animate `+0xA0` to 0 at run time."; "**which asset, and whether the mirroring is of texture or of gradient, is not established here.**"; "**NOT CLAIMED: who installs `+0x38` and `+0x48`, or where that buffer is allocated.**"; the 0x30 record "**The record's interior is unread**" (but see `DB:455-460` for the vertex format) | `DB:445`, `NINEP:150-151`, `NINEP:314-315`, `NINEP:338-339` |
| G-13 | Rectangle: "What `00202B70` computes beyond dividing by the `w` it returns."; "`context + 0x70` holds — it becomes the third component of every vertex."; "what the mode of `00181870` and the four integers of `00181930` select is still not claimed" | `RECT:183-188` |
| G-14 | Measure / reveal: "how often the stepper is called per frame is not traced"; "What `002B20B0` maps beyond line index to byte offset." | `MEASURE:215`, `MEASURE:281-282` |
| G-15 | Icons: whether the overwrite from `01E0CE60` is dead or conditional "**not established.**"; what the four "bytes at `01E0CE60` are"; `01E0CE80` "**Not established.**"; which drawer is original "**Not established, and probably not a meaningful question**" | `BLINK:122-125`, `BLINK:310-311`, `ICON2:155`, `ICON2:158` |
| G-16 | Background: "The consumer of the `v` pair is still not visible in the decompilation"; "What the style index at `node + 0xA3`" enumerates | `WBG:101-102`, `WBG:232` |
| G-17 | Widget messages: "**This document does not claim what 3, 4 and 5 mean**" (named by place only at `WTREE:255`) | `WTREE:110-111` |
| G-18 | Unlisted: the 129 blocks called only from unlisted code: "They form chains inside the residue and none has been read." (superseded, not answered, `REF:129`); continuation ownership "**not established**"; the readers "Whether they should read the grown extents is not assessed here."; "the 11,339 records beginning inside a listed body are not investigated here"; "Until then, the readers still count 35,064." | `REF:127-129`, `CUT:204`, `CUT:236-237`, `UNL:797-799`, `UNL:932-933` |
| G-19 | Binding machine / effects: `022D94B0` `+0x0A .. +0x17` "still unread"; "**Not claimed:** what separates classes 5 and 9 in `0024B9B0`"; "which mesh each register holds was not traced"; parameter entries from slot 11 up "is not read here."; what each draw path does differently "is unread." | `BIG:519`, `BIG:1232`, `BIG:1463`, `BIG:1485`, `BIG:1510` |
| G-20 | Census: "**Who writes these slots at runtime.**" (PROPOSED-repos9e-12); the `01CCAxxx` tables "None of them is characterised; their consumers were not traced."; `01F00398` "What object kind the table serves is **not established**"; "*Not done:* naming the 145 pooled classes one by one. **AR-2.**" | `CENSUS:1014-1016`, `CENSUS:1196`, `CENSUS:1450-1451`, `CENSUS:358-359` |
| G-21 | Residual: "the XGKICK equivalence is still open."; "Whether the other 29 are player-reachable is not claimed."; `0024B580` kinds and callees "**not read here and are not claimed**"; `0036A2A0`'s header producer "**not traced**" | `U158:1258`, `U158:288`, `U158:1360-1365`, `U158:1501-1502` |

### 2.2 Structural gaps (a port needs these and no page in the folder states them)

| # | gap | where the page shows it |
|---|---|---|
| S-1 | **No frame-level order for text.** No page says when, inside a frame, the widget pass, the message-window case 4, the reveal stepper, the font painter's `0017F850`/`0017FA10` pair and the render-buffer swap run relative to each other. Each page gives only its local order | `PAINT:204-208`, `MEASURE:215`, `U158:823-852`, `WTREE:209-210` |
| S-2 | **`TextState` total size and unnamed offsets** `+0x10`–`+0x1F`, `+0x24`, `+0x2C`, `+0x5E`–`+0x5F`. The **`~0xD0` state** of `002AAE40` names only `+0x20`, `+0xB8`, `text`, `limit`. Neither page says whether the two are one type | `GQ:357-387`, `CBC:56-78`, `CBC:161` |
| S-3 | **The 32-byte window line record** read by `0053E0B0`: only a shadow byte, a kind and x at `[rsi − 0xA]` are named | `GQ:291-302`, `GQ:717` |
| S-4 | **Glyph cache sizing**: node count, pool allocation and initial list state are not stated. The data structure itself is ambiguous (C-V2) | `GQ:421-434`, `GQ:1788` |
| S-5 | **The 16-byte GS command record's byte layout** is not given (codes only). The upload callee `003A22A0` and `003A1FE0` are named, not described | `GQ:158-173`, `GQ:1790-1795` |
| S-6 | **Font slot mask** `[022CBE00 + 0x240]`: writer and initial value not stated. The `{k}`/`{p}` tags are "bounds-checked" with no bound. `{r}` angle units not stated | `GQ:251-264`, `GQ:522-526` |
| S-7 | **`DAT_0209CC50` render commands** written by `002AAE40`: "their bit layout is transcribed in the body and **not** decoded here". `0020E600`'s return is open on CBC and its role is disputed (C-V8) | `CBC:238-242` |
| S-8 | **Font painter object fields** `+0x13A0` ("shared render parameters"), `+0x1390` (always `0x44`, meaning not stated), the `0x38` batch layout beyond cursor/capacity, the `0x98` flush-and-forget draw object (no constructor named), and the render-target push callee (three addresses; C-V27) | `PAINT:183`, `PAINT:214`, `PAINT:257-258`, `PAINT:379-382`, `PAINT:593` |
| S-9 | **Shared-context field meanings**: `+0x10D0`, `+0x10E0`…`+0x10F8`, `+0x10FD`…`+0x1104` carry counts only. The three states of `+0x10FC` are not named. The `+0x000` row's third qword and the 10-bit id are answered only in an external record (SD-104) | `CTX:82-88`, `CTX:183-184`, `CTX:273-274`, `CTX:656` |
| S-10 | **Initialiser timing**: `002B3550` runs "at startup", caller not stated. The font painter initialiser `001E71B0`'s caller is not stated. `001E9C30`'s callers (who sets the mode byte) are not listed | `CTX:32`, `PAINT:155`, `RT:220`, `RT:278` |
| S-11 | **Dispatcher signatures**: what columns 0/1/2 receive besides `rcx`. The six context fields `002AC5F0` touches are not listed. Behaviour for an out-of-range `+0xA3` selector is "a hazard" with no bound | `DISP:143-145`, `DISP:384`, `DISP:721-732` |
| S-12 | **Widget node layout**: position fields (`this.x`/`this.y`), total size and `definition + 0x40` rect format are not given. `+0xA6`/`+0xA7` are used both as size addend and offset base | `WTREE:121-127`, `WBG:76-77`, `WBG:219` |
| S-13 | **`002DC290` GS words** `0x1000000000000002`, `0x2026400000008004`, `0x41`, and the batch open/close `002DD1E0`/`002DD090`, are not decoded on NINEP. RECT decodes the analogous words for `002DBDD0` only | `NINEP:234-236`, `RECT:138` |
| S-14 | **Icon record layout**: `+0x02` kind, `+0x20` index, `+0x24`/`+0x26` w/h, `+0x28` flags (bits 15, 6 only), `+0x50` amount and `+0x60` next are named piecemeal. Its size and other flags are not stated | `BLINK:63-100`, `BLINK:299`, `BLINK:312` |
| S-15 | **Cutscene source object** read by `0020A800` / `0020AA50` is not laid out. Where `001C5750` stores the two DoF values is not stated. The writer and meaning of per-slot flag value `5` (tested by `001ED130`) are not stated. `001C5570` (tail target of `001EC520`/`001EC540`) is not described | `CS:188-189`, `CS:147-154`, `CS:535`, `CS:847` |
| S-16 | **The 158-byte DoF recorder** of UQ-340 has no address on the page | `CS:515-518` |
| S-17 | **Binding machine semantics**: which opcode is which of the eight palette effects. What `003CD840`/`003D2B60` compute over the 32 cells. `[0x02B487A0]` is named once and never explained. The generation counter's initial value | `BIG:776`, `BIG:888`, `BIG:928` |
| S-18 | **The 1,405 scattered unlisted blocks** (66,642 B) of "ordinary compiled engine code" have no per-block description (UC-4 superseded, not read). The 159 libvpx routine names live only in `uc3-blocks.tsv` outside the folder | `UNL:418-419`, `UNL:447`, `UNL:456-459` |
| S-19 | **The residual set itself**: the 158 addresses are not enumerated on U158 (external `GM160_CURRENT160_ADDRS.txt`). The live 30 are listed only in `residual-30-GN161.tsv` | `U158:132-134`, `README:11` |
| S-20 | **`0024B580` queue**: when it runs in a frame, what the nine kinds are, and the meaning of `002FC010`'s return | `U158:1360-1365` |
| S-21 | **Ownership**: README lists only 4 of the 22 system pages (`README:133-156`). A port reading the index would not find the text, widget, cutscene or census pages | `README:133-156` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Each item quotes both sides exactly, with `NAME:line`. Every quotation was checked string-for-string against the snapshot
`f26c5667`. Where a quote spans a wrapped line, the line break is shown as a space and the leading `> ` of a blockquote line is
dropped.

- **3.1 Value-changing items** would change what a port computes, stores or calls. Each one is
  **page-text only - needs local check**, because this session cannot see the executable. Each is tagged **[engine]** (behaviour,
  layout, address, formula) or **[ledger]** (a count or extent that affects only the residual bookkeeping).
- **Favoured side.** A side is named only where a dated correction on the pages settles the question. Even then the byte check is
  still owed.
- **3.2 Stale or banner items** change no value. Each is an "open / not read" claim that another page or a later dated section
  answers, a corrected claim repeated unstruck, or a status banner that disagrees with front matter.

### 3.1 Value-changing — page-text only - needs local check

**C-V1 [engine] — `003647E0` control codes 1 and 3 are swapped, and the gating differs.** *No favoured side.*
- §2: "| `0x0001` | advance the pen by the advance width of the character `'0'` — **a figure space** |" (`GQ:272`) and
  "| `0x0003` | restore the alpha byte from the saved copy — **undim** |" (`GQ:274`). Also "Codes `2` and `3` are gated on bit 0
  of the state byte at `+0x63`" (`GQ:277`).
- Subtree table: "opcode 1 copies `[rdi+0x37]`→`[rdi+0x33]` (`00364843`), opcode 2 writes `[+0x37]/5` …, opcode 3 scans the
  `[022CBE00]` layer's `0xC`-stride table for `word == 0x30` (`00364893`) — all gated on `byte[rdi+0x63] & 1`" (`GQ:1787`).
- Code 2 (dim to `/5`) agrees on both sides. **Local check:** the arms at `00364843` and `00364893`, and which arms the `+0x63`
  test guards.

**C-V2 [engine] — what `00364210` and `00365FD0` are.** *No favoured side.*
- §3: `00364210` "Evicts the LRU tail, fills it from the font glyph table, rounds cell dims to powers of two" (`GQ:318`).
  `00365FD0` "Finds the node and moves it to the list head" (`GQ:319`).
- Subtree table: `00364210` is "the span clipper — u16 tag scan over `[022CBE00]` records …, returning the clipped span"
  (`GQ:1789`). `00365FD0` is "the u16-key cache scan" with no promote step (`GQ:1788`).
- This decides whether a port needs an LRU glyph cache at all (S-4).

**C-V3 [engine] — the nine-patch per-cell split rule: the no-split arm is inverted.** *No favoured side.*
- DB: "`if (col != 1 && (cellWidth - 8) <= 0x27 && (rowHeight - 8) <= 0x27)` … `flag = (colIndex == 1) ? 0 : 8;` else
  `flag = (colIndex == 2) ? 4 : 0;`" (`DB:271-274`). DB's prose agrees: "// bottom row:  4 when the cell index is 2, else 0"
  (`DB:260-262`).
- NINEP: "`if (col == 1 || (uint)(size - 8) > 0x27 || (uint)(axis - 8) > 0x27)` `flags = (index == 2) ? 0 : 4;     // no split`
  `else flags = (index == 1) ? 0 : 8;     // split through the centre`" (`NINEP:207-209`).
- The split condition and the split arm agree. In the no-split arm, DB gives cell index 2 flag 4 and the others 0; NINEP
  gives cell index 2 flag 0 and the others 4. Flag 4 selects "**one quad**, drawn with `flags & ~4`" (`NINEP:183-187`).
  **Local check:** the two `cmov`/`setcc` sequences in `00392A10` around the `0x27` compares.

**C-V4 [engine] — the corner-blend colour.** *No favoured side.* No correction strikes either version. The dated 2026-09-26 replay
(`DB:453-462`) agrees with NINEP.
- DB (twice, unstruck): "`blended = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   // per channel`" (`DB:234`) and
  "`blended_channel = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);`" (`DB:359`).
- DB's UQ-353 replay: "whose colour is `(((c0+c1)/2 + c2)/2 + c3)/2`: weighted toward corner 3, not an average." (`DB:462`).
  NINEP: "`mid = ((((c0 + c1) >> 1) + c2) >> 1) + c3) >> 1;`" (`NINEP:195`).
- The first form nests the other way and carries a `d >> 24` term (alpha byte into a colour channel). The second weights the
  corners 1/8, 1/8, 1/4, 1/2 (`NINEP:198-199`). **Local check:** the `& 8` arm of `002DC7F0`.

**C-V5 [engine] — what the fallback `00392CE0` draws.** *No favoured side.*
- DB: "`FUN_00392ce0(ctx, rect, colours);      // ONE gradient quad, no slicing`" (`DB:241`). "The fallback `00392CE0` builds a
  single quad — four corner positions and the same four colours, arranged 2×2" (`DB:250-252`). The key table says "The
  un-sliced path: one gradient quad" (`DB:288`).
- NINEP: "`00392CE0` has a special case for **two of the nine cells** — the top-left (`row 0, col 0`) and the bottom-right
  (`row 2, col 2`)" (`NINEP:139-140`). CS: "derives nine region widths …, iterates the nine slices and calls the shared emitter
  `002DC290` per slice" (`CS:1553`).

**C-V6 [engine] — who calls `002DC290`.** *No favoured side.*
- CS: "**eleven callers across seven address neighbourhoods**, including both renderers above" (`CS:1390-1391`).
- CS (same page): `00392CE0` "emits through one callee, `002DC290`. The sliced path uses `002DD1E0`, `002DC7F0` (×3) and
  `002DD090`" (`CS:1342`). DB: "The **live** cell drawer, 11 other callers — not dead" (`DB:291`).

**C-V7 [engine] — what `002DD090` does.** *No favoured side.*
- DB: "Closes the draw batch. Sole caller `00392A10`" (`DB:290`).
- CS: `002DD090` is "the packet submitter", which "writes the `0x10000000` bracket-open command" and the `0x6C008000` header
  (`CS:1551`). The bracket-open command is what sets the flag `002DD4B0` returns (`DB:447`). So which function opens the
  bracket changes the order a port must emit.

**C-V8 [engine] — what `0020E600` is.** *No favoured side.*
- A scheduler yield: "call the `CoreRuntimeScheduling` yield `0020E600`" (`CBC:256-258`, `MEASURE:304`). "`CoreRuntimeScheduling`
  `0020E600`" (`REF:288`). CBC also lists "What `0020E600` returns." as open (`CBC:239-240`).
- An address resolver: "`ImageAddress_ResolveRuntimePointer   (10 B)`" (`GQ:1453`). "`0020E600` is `mov eax, ecx; add rax, [01F83530];
  ret`" (`BIG:1386`). "calling `0020E600`, `ImageAddress_ResolveRuntimePointer` — the shared image-address resolver the core
  runtime layer owns" (`CENSUS:1469`).
- A port of the text walk (`002AAE40` → `0020E600` per glyph cell, `CBC:72`) needs to know whether this returns a pointer.

**C-V9 [engine] — the `0053E0B0` call chain.** *No favoured side.*
- Call chain: "`0053E0B0` … `-> 002D8690 / 002D87D0  renderer selection` `-> 00364980   "ex" prefix?`" (`GQ:546-548`).
- Same page: "this page's `0053E0B0` calls `003649A0` without the test" (`GQ:704`), with call order "`003659F0 → 003649A0`
  **twice**" (`GQ:1482`).

**C-V10 [engine] — what `00229E40` is.** *No favoured side.*
- "`00254A14  call 00229E40          ; returns [01E02814], which SHIPS AS 0x0A`" (`CTX:322`).
- "`00254A10` calls the `CoreRuntimeScheduling` yield `00229E40`" (`CTX:735-738`).

**C-V11 [engine] — what the 8-slot registry `0209C4D0` holds.** *No favoured side.* Neither page strikes the other.
- "`0209C4D0` is an 8-slot actor registry" (`U158:839`, also `U158:239-240`, `U158:867`). CS repeats it (`CS:977-981`).
- "the **live** message-window registry" (`U158:551`). "the window objects as **`MessageWindowRecord`**" (`U158:560`).

**C-V12 [engine] — whether `00364530` reaches the render-target chooser.** *No favoured side.*
- GQ: `00364530` has "12 call sites, **zero** render or scope calls" (`GQ:1481`) and is `Text_MeasureGlyphRun` (`GQ:315`).
- RT: the mode-2 chooser `0017FD00`, which forwards to `001E9D20`, is "called only by the message-window family
  (`00364530`, …)" (`RT:288`).

**C-V13 [engine] — whether `002B2150` draws.** *No favoured side.*
- "`002B2150` draws each text run" (`GQ:842`).
- "a score-summing pass over the line's elements, not a draw" (`CBC:288-289`). GN162 `UI.Text.MeasurePass` (`MEASURE:228`). GQ itself:
  "a *scoped* pass, not a compiler … accumulating `xmm6` (width) / `xmm7` (max height)" (`GQ:853-856`).

**C-V14 [engine] — byte meanings in the compiled line stream.** *No favoured side.*
- CBC: "bytes `0x01`–`0x0F` are tokens, `0x10` and up are text. **`0x03` is handled here rather than there**, and it ends the
  run" (`CBC:93-95`).
- GQ: "`0x02` is an inline marker, `0x03` is a line commit, `0x10`–`0x1F` are two-byte object references and `>= 0x20` one-byte
  object references" (`GQ:833-835`). And "by the line-break token `0x02`" (`GQ:1736`).
- MEASURE's walk agrees with neither as a whole: `3` hard break, `2` calls `002B2150` on the remainder (`MEASURE:165-170`).

**C-V15 [engine] — whether `002AAE40` draws.** *No favoured side.*
- "**None of the three draws.** The glyph emitter is `002A9F00`, which is not among them." (`GQ:773`)
- "| `002AAE40` | **a drawing pass** …" (`GQ:784`). CBC's walk calls "`FontPainter_DrawGlyph(&record);                    // 0017F7C0`"
  (`CBC:76`).

**C-V16 [engine] — what a column-1 dispatch does to `0209CC48`.** *Not settled.* CTX's dated correction reinterprets the store, but
it does not account for the immediate `0` in DISP's listing.
- DISP listing: "`mov   qword ptr [0209CC48], 0`" (`DISP:114`). "and clear `[0209CC48]`" (`DISP:275`).
- CTX: "the dispatch re-points `0209CC48` at the record the swap selected and rewinds `0209CC50` to its start" (`CTX:253-254`).
  Key table: "~~cleared by both column-1 dispatchers alongside the publish~~ … re-pointed … (§3d; corrected 2026-09-30,
  SWE2-DATA)" (`CTX:611`).

**C-V17 [engine] — `0209E5D8` / `0209E5DC`: read or written by `002BCB00`.** *No favoured side.*
- ICON2: the position offset globals are "**`0209E5D8` / `0209E5DC`**" (read, as the twin reads `0209E5A8`/`0209E5AC`)
  (`ICON2:57`).
- RECT: `002BCB00`'s "body stores `0209E5D8`/`0209E5DC`" (`RECT:204`).

**C-V18 [engine] — what `002DD7E0` returns.** *No favoured side.*
- BLINK: a palette getter returning `*(DAT_0215E6C8 + id*8)` or `0x80808080` (`BLINK:107-111`), whose dwords are
  `fontcolor.bin`'s face colours (`BLINK:288`, `BLINK:4`).
- NINEP: "`002DD7E0` fetches the `0x67`/`0x69` string then `0x68`/`0x6A`" (`NINEP:385`).

**C-V19 [engine] — what `00181460` does, and its caller count.** *No favoured side.*
- RECT: "`00181460(points, n)` turns a strip into a list - for each of the `n - 2` triangles it appends three 0x30-byte vertices"
  (`RECT:140`).
- NINEP: a nine-patch grid fill, "the nine-patch's 2-D `(n-2)x3` loop" (`NINEP:283-284`). It has "105 B, 9 A-measured callers"
  (`NINEP:256`), against "`00181460` is called by `002AFDC0`, `002D9DB0`, `002DA2D0`, `002DA7C0` and 10 more" (`WTREE:301`).

**C-V20 [engine] — how many callers `002AC5F0` has.** *No favoured side.*
- "`002A8C50` is one of the seven callers of `002AC5F0`" (`DISP:285`).
- "the one six other functions call" (`DISP:295-296`). GQ counts "the other four callers of the interpreter" (`GQ:792-793`).

**C-V21 [engine] — how many callers `002ABEC0` has.** *No favoured side.*
- 5: the caller column "| 5 |" (`DISP:138`), and "caller counts **2 / 3 / 5**" (`DISP:704`).
- 9: "Its nine callers pass the widget's embedded text-draw block" (`DISP:228`), and "every embedded base the nine callers use"
  (`DISP:657`).

**C-V22 [engine] — how many font painter entry points there are.** *No favoured side.*
- "**Every function in FFXII that draws text goes through eighteen entry points**" (`API:31`). The table lists 18 rows, all in
  `0017F650`–`0017FD30` (`API:57-74`).
- "Sixteen sit in one contiguous band, `0017F650`–`0017FD30`", and two more are "consumers rather than API entries" (`API:35-37`).
  A nineteenth band member, "The sibling `0017F9A0` forwards to `001B5FB0`/`001B5210` the same way" (`API:304-306`), is not in the
  table.

**C-V23 [engine] — how many callers `0017FD30` has.** *No favoured side.*
- "`0017FD30` — 63 B, 6 A-measured callers" (`CBC:294`).
- "has eight callers" (`RT:288`), with seven named.

**C-V24 [engine] — what `001FDD60` returns on a miss.** *No favoured side.*
- "**`001FDD60` is the same algorithm byte for byte**" as a find that "returns the terminator on a miss" (`RT:305-308`).
- "miss returns 0" (`RT:461-462`).

**C-V25 [engine] — who calls the painter begin `0017FA10`.** *No favoured side.*
- "Eleven sites in seven functions, and **three of them were on the 158 list**" (`PAINT:189-190`).
- The page names six: `002AC5F0`, `003649A0`, `002AF960`, `002A9F00`, `002B0280`, `002D28E0` (`PAINT:190-192`).

**C-V26 [engine] — which tree child pointer is left and which is right.** *No favoured side.*
- "`001E9D79  mov   rcx, qword ptr [rcx + 8]          ; left`", "`001E9D7F  mov   rcx, qword ptr [rcx]              ; right`"
  (`RT:95`, `RT:97`). Also "right `+0x00`, left `+0x08`" (`RT:320`).
- "left `+0x00`/right `+0x08`" (`RT:482`).

**C-V27 [engine] — the render-target push callee.** *No favoured side.*
- "`001E865F  call  0x001FBE50                 ; NON-ZERO -> push a render target and paint`" (`PAINT:343`).
- "pushed with `FUN_0018AFF0`" (`PAINT:532`).
- "the mode arguments `1` and `3` to `FUN_001FBD80`" (`PAINT:544`).

**C-V28 [engine] — what glyph record `+0x9C` holds.** *No favoured side.*
- "`FUN_001E94E0(param_1, [param_2 + 0x9C] % 0x1C)`" — a palette index (`PAINT:467`; also `CBC:111`, `API:102`).
- "`dword[rdx+0x9C]` element count read (`001E808A`), magic-divide `0x92492493` (÷7, `001E809B`)" (`PAINT:661-662`).

**C-V29 [engine] — the font painter batch array: base and stride.** *No favoured side.*
- "walked from `param_1 + 0x70`" (`PAINT:379`) against the open-batch formula "`state + 0x30 + (slot*32 + n)*0x38`" with
  `1 ≤ n ≤ 31` (`PAINT:433-436`). The formula gives `+0x68` for slot 0, n = 1.
- The fallback: vertices are "`0x3C` bytes … falling back to `001E7A20` when the batch is full" (`PAINT:454-456`), against
  "`001E7A20` (610 B) | `0x38`-stride vector insert" (`PAINT:668`).

**C-V30 [engine] — the address of `FieldData_GetActiveFieldRecordBit15`.** *No favoured side.*
- `00313F60` (`CENSUS:1531`).
- `00377C20` (`U158:1595`). REF: "calls `WorldAreaField` `00377C20`" (`REF:290`).

**C-V31 [engine] — the cutscene-slot latch order.** **Favoured: `CS:537-538`.** UQ-341, answered 2026-09-14, states that §2 "is right
about the value and too simple about the protocol" (`CS:547-548`).
- §2: "It is set before any work and cleared on every exit path, including the early ones." (`CS:89-90`). The listing has the bounds
  test first (`CS:85`, `CS:238-239`).
- UQ-341: "`0020AC30`, the slot fill, stores the index unchecked (`0020AC64`), then tests `≤ 4`. It resets the latch to `−1` when the
  name does not parse (`0020AE48`)." (`CS:537-538`). The normal-exit reset site is not given.

**C-V32 [engine] — the `002DC290` command's vertex offsets collide with its transform.** *No favoured side.*
- Vertex 0's colour is at "`+0x50 +0x54 +0x58 +0x5C`" (`CS:1408`).
- "It writes them again into the command at `+0x20`–`+0x5F`" (the 4×4 transform; `CS:1502-1503`).

**C-V33 [engine] — whether `00180120` consumes flag B.** *No favoured side.*
- UQ-336 (2026-09-15): `00180120` "does not name flag B, so the consumer count stands." (`CS:363`).
- `001EC5C0` "Zero-extends flag B for its 4 consumers" (`CS:197`). The four consumer sites "fall in **four** functions: `00180120`, …"
  (`CS:387-390`).

**C-V34 [engine] — the operand of `001ED180`.** *No favoured side.*
- "`id = WorldTransition_GetTransitionFieldId();`" (`CS:862`).
- "`ebx = 00314910()` is the current kind" (`CS:1599-1600`).

**C-V35 [engine] — the batcher's `0x58` slot and the ring base.** *No favoured side.*
- (a) `+0x2C` initial value. `001B06D0`'s template: "`qword[+0x14] = 1`, `+0x2C..` zeroed" (`NINEP:272-273`). `001B0100`'s reset:
  "`+0x10`/`+0x14`/`+0x2C`/`+0x30` latch 1" (`RECT:307-308`).
- (b) Ring base: "`&DAT_02EBEFC8 + DAT_02EBEFF0 * 0x18`" (`NINEP:175`) against "`02EBEFF0`'s index ×3 strides the `02EBEFC0` table
  (0x18 records)" (`RECT:228`). An 8-byte difference, consistent only if NINEP means the `+8` field, which it does not say.

**C-V36 [engine] — where `002DAF30`'s 64 bytes come from.** *No favoured side.*
- WBG: "four `movups` lanes copy `rdx`'s 64 B into the `022D8F30..60` globals" (`WBG:265-266`).
- WTREE: it "loads four `xmm` rows from `02EBEFC0` / `02EBEFF0` into the shared workbench" (`WTREE:258`).

**C-V37 [engine] — whether the reveal stepper's state is the drawing context.** *No favoured side.*
- MEASURE identifies the stepper state's `+0x5A` with the drawing context's brightness: "**It is the brightness**, as §5 says below and
  as [the rectangle primitive] … read it" (`MEASURE:196-197`).
- The same page gives `+0x90`/`+0x92` as "a **following pair**" (`MEASURE:209`) and `+0xA0` as "the step size" (`MEASURE:212`).
  RECT reads `context[0x90..0x93]` as "RGBA" (`RECT:64`). NINEP reads the node's `+0xA0` as alpha (`NINEP:132`).
- If the objects are the same, the fields collide. If they differ, the brightness identification fails.

**C-V38 [engine] — whether `002D6990` is dead or live.** *No favoured side.* UQ-355 is answered NO, which keeps the live reading.
- "`002D6990` (783 B) is the dead nine-patch draw body" (`DB:704`).
- "A **different, live** 3×3 system" (`DB:293`). "— both are live and their callers are disjoint**" (`DB:479`).

**C-V39 [ledger] — where the 158 lie in the address space.** *No favoured side.*
- "The 158 are scattered over **37 distinct 64 KB pages** from `0x0018xxxx` to `0x004Fxxxx`." (`U158:103`).
- The same page names 158-members above `0x0050xxxx`: `00573BE0` (`U158:525`), and `00565E00`, `0056F810`, `005771F0` (`U158:268`).
  `residual-order.tsv` (139 ⊂ 158) runs to `005DF890`.

**C-V40 [ledger] — how the 30 split.** *No favoured side.*
- "The split is **30 DESCRIBED, 0 CONTESTED, 0 UNREAD**" (`U158:1149-1150`). This agrees with `residual-30-GN161.tsv` (30 `DESCRIBED`).
- "`check_residual_depth.py` reports 29 described and **`0036A2A0` alone as contested**" (`U158:1489-1490`). "the 29 DESCRIBED bodies
  in" `residual-30-GN161.tsv` (`U158:1567-1568`).

**C-V41 [ledger] — what batch R109 classified.** *No favoured side.*
- "The 109 singletons named here are **no longer unresolved**" (`U158:50`).
- `residual-109-classification.tsv` includes cluster members `002A4830`, `002A4430`, `002AF960` (the 13-cluster, `U158:657-669`) and
  `00256CA0` (`U158:585`). `U158:1130-1134` describes R109 as 109 of the 139, not as the singletons.

**C-V42 [ledger] — the twin diff byte count.** *No favoured side.*
- "~1,186" rel32 displacement bytes (`U158:361`).
- "| 395 | 1,184 |" (`U158:426`).

**C-V43 [ledger] — census counts.** *No favoured side* on any of the three.
- (a) `00244F50`: "`00244F50`, 203 callers, read in full:" (`CENSUS:289`) against "**231 call sites** image-wide" (`CENSUS:349-350`). These
  may be different units; the page does not say.
- (b) The battle action handler table's slots in span: "| 339 | Battle action handler table — `01EEC460`, 359 slots |"
  (`CENSUS:942`) against "359 slots | 340 |" (`CENSUS:1050`). §17 claims to reproduce §16 exactly (`CENSUS:1037-1045`).
- (c) RTTI vtables: "2,286 vtables recovered and named via RTTI" (`CENSUS:361`) against "**2,335 RTTI type descriptors → 2,271
  complete-object locators → 2,271 vtables**" (`CENSUS:1151-1152`).

**C-V44 [ledger] — whether the interpreter `0025E4C0` and `00301AD0` are truncated bodies.** *No favoured side.* The member TSVs side
with `CUT:111-114`.
- "The interpreter, one of the truncated bodies, …" (`CUT:246`). "`AiOrder_EvaluateTargetSelector` (`00301AD0`). Another truncated
  body" (`CUT:252-253`).
- "**The bodies this database leans on are not among them.**", with both listed as contained in their recorded extents
  (`CUT:111-114`, also `CUT:199`). Neither address is in either truncated-body TSV.

**C-V45 [engine] — the end of `0037C3F0`.** *No favoured side* on the page. The member TSVs give `0037C6F8`.
- "out to 0037C6C3." (`CUT:15`), and again at `CUT:47`, `CUT:85`, `CUT:196`.
- "code reaching `0037C6F8`" (`CUT:68-69`). The table is also at `0x0037C6F8` (`CUT:67`).

**C-V46 [engine] — `00148F41` and `001492FF`: data or libvpx code.** *No favoured side.*
- CUT: `001492FF` is "switch data after `repz ret`" (`CUT:142`). `00148F41` is "unreferenced … outside the population" (`CUT:146`).
- UNL (UC-3, narrowed 2026-09-27): "the vpx_dsp intra predictors dc 32x32 (00148F41) and h 32x32 (001492FF)" (`UNL:453`).

**C-V47 [ledger] — the continuation count.** *No favoured side.* `unlisted-body-admissions.tsv` agrees with `UNL:73`.
- The 2026-09-25 table: "| continuation | 162 | 3,418 |" (`UNL:73`), body 874 (`UNL:72`). And "**877 blocks**: 874 bodies plus 3
  ambiguous, with the 162 continuations counted as extents" (`UNL:82`).
- Unstruck: "adjudicated **163 of those blocks as continuations of the body before them" (`UNL:37`). "163 blocks - 3,797 bytes - are not
  separate functions" (`UNL:224`). "| `continuation` | 163 | 3,797 |" (`UNL:596`), body 1,301 (`UNL:595`).

**C-V48 [ledger] — the unlisted body count.** *No favoured side.*
- "at least 1,471 bodies" (`UNL:425`), "code in about 1,308 blocks" (`UNL:33`), "**877 blocks**" (`UNL:82`), and "**~1,425 .. ~1,428**"
  (`UNL:747`): four figures for one population.

**C-V49 [engine] — the extent of the 4×4 matrix in the register bank.** *No favoured side.*
- "`022D91B0`–`022D91EF` is **64 bytes of global transform.**" (`BIG:411`).
- "| `022D91A0`–`022D91E0` | **the 4×4 matrix**" (`BIG:445`).

**C-V50 [engine] — the size of the chain-A register file.** *No favoured side.*
- "1,424 bytes" (`BIG:372`).
- "1,432 bytes" (`BIG:731`), and "1,432-byte register file" (`BIG:1001`).

**C-V51 [engine] — the binding-pool payload size.** **Favoured: 48 bytes.** `BIG:923` says it "corrects the '32-byte payload' comments in
the two code blocks above".
- "32-byte payload" (`BIG:892`, `BIG:906`). Unstruck and outside the correction's reach: "The 32-byte record payload remains opaque apart
  from its index byte." (`BIG:1014`).
- "the payload is **48 bytes**" (`BIG:923`).

**C-V52 [engine] — the event-effect tag values.** *No favoured side.*
- The BI-8 record: "0 free / 1 requested / 4 cancelled / 5 loaded" (`BIG:1181`).
- `0036E540` sets word `+4` to 2 (`BIG:1085`, `BIG:1613`), and `0036E5E0` tests `== 3` (`BIG:1615`).

**C-V53 [engine] — call counts and clamps in the binding machine.** *No favoured side.*
- `003CD840`: "(x2)" (`BIG:336`) and "The dispatcher calls `003CD840` twice among ten" (`BIG:380`), both unstruck, against "`003CD840`
  THREE times, §20**" (`BIG:333`).
- `0036B130`: "(x3)" (`BIG:336`) against "is called **four** times" (`BIG:1297-1298`).
- The clamp: "Six accessors clamp the index to `0x1F`" (`BIG:522`), while the table shows seven rows with `0x1F` (`BIG:500-506`).

**C-V54 [ledger] — the GN158 census cells and the headline size.** *No favoured side.*
- `28,009→28,137` with residual 158 → 30 (`BIG:38-39`), against "CodeDomain only 28,028 … neither 139 (the residual)" for the same GN158
  checkpoint (`BIG:206-208`).
- Headline size: front matter "2.67 MB" (`BIG:2`), body "2,524,402 bytes" (`BIG:34`), README "2.41 MB" (`README:150-151`).

**C-V55 [engine] — `0041E000` and `01EFFAF0`.** *No favoured side.*
- §19 decodes "`call qword ptr [r9 + r13]`" inside `0041E000` (`CENSUS:1398`), against "`0041E000` (461 B) is a call-free unowned body"
  (`CENSUS:1490`).
- "**A 128-record authored-command table at `01EFFAF0`**" (`CENSUS:1401-1402`), against "`01EFFAF0` vtable" (`CENSUS:1494`).

**C-V56 [ledger] — the unlisted-only count.** *No favoured side.*
- "The other 130 referenced blocks are called only from other unlisted code." (`REF:17-18`).
- "**129 of the 135 are called only from other unlisted code.**" (`REF:47`). 143 − 14 = 129.

**C-V57 [engine] — what `00261F90` is.** *No favoured side.*
- "**Audio**" (`REF:319`).
- "the field-runtime record step `00261F90`" (`REF:251`).

**C-V58 [engine] — `002AAE40`'s callees and pen addresses.** *No favoured side.*
- "The decompilation contains **fifteen" distinct calls (`CBC:165`), but the list names 16 (`CBC:166-168`), and edges.tsv has "**16
  outgoing edges and 0 incoming**" (`CBC:180-181`).
- AC-9: "`[0209CC6C]` added before each glyph (`002AA0D2`) and `[0209CC68]` after (`002AA734`)" (`CBC:230-232`). Both addresses lie below
  `002AAE40`, inside `002A9F00`'s range. The pseudo-code shows only "`pen.x += DAT_0209CC68;`" (`CBC:79`).

**C-V59 [engine] — the constant pool at `008C5F80+0x70`.** *No favoured side.*
- "+0x70   0  0  0  0        <- referenced by nothing" (`GQ:1513`).
- "008C5FF0 (+0x70)   22 05 93 19 … not float data; the pool has ended" (`GQ:1578-1579`).

**C-V60 [engine] — dispatch-table occupancy.** *No favoured side.* The table the text describes contradicts the text.
- "Of twelve slots, five are filled by four distinct bodies." (`DISP:370-371`).
- The table above it (`DISP:365-368`) fills seven slots with five bodies: `002A9980` ×2, `002A8C50` ×2, `002A9F00`, `002AA800`,
  `002AAE40`.

**C-V61 [engine] — `002DA7C0`'s output word count.** *No favoured side.*
- "twelve 16-byte words into a cursor at `param_1 + 0x10` — descriptor, then per corner a colour, a source (u, v) and a destination
  (x, y, z)" (`WTREE:159-160`). One descriptor plus 4 × 3 is 13.

**C-V62 [ledger] — `002DD4B0`'s "other" callers.** *No favoured side.*
- "10 other callers" (`DB:183`, `DB:292`).
- The ten raw sites DB lists include `00392A10`'s own `00392AE4` (`DB:449-451`).

**C-V63 [engine] — whether `0017F8E0` fetches the singleton once or twice.** *No favoured side.*
- "fetches the singleton **twice**" (`API:223`).
- One fetch, then "`001E9780(ctx, ecx)`" and `001E9BD0` (`API:319-321`).

**C-V64 [engine] — the reveal stepper's mode set.** *No favoured side.* The jump table at `002AC1B4` is the arbiter.
- "labels **0, 1, 2, 3, 4, 5, 7** (seven, no `default`)" (`U158:779`). MEASURE: "**states 0 through 5 and 7**" (`MEASURE:202`).
- "**eight-mode jump table**" (`U158:1400`). MEASURE: "**There are eight modes and six distinct bodies**" (`MEASURE:193-194`), mode 6 a
  no-op (`MEASURE:288`).

**C-V65 [ledger] — residual arithmetic on GQ.** *No favoured side.*
- "The other 153 are not" after four of 158 were found (`GQ:85`).
- "**The 147 residual functions this block did not read at all.**" (`GQ:1234-1236`).
- "**139 → 30**" (`GQ:228-229`), against "R109 classified 128" (`GQ:1236-1237`).

**C-V66 [ledger] — the `01DFE40C` reference count.** **Favoured: 23 functions** (corrected 2026-09-03, `CS:92-93`).
- Unstruck: "read by 24 functions" (`CS:296-297`).
- "This said *"**24** other functions read"* it. **23 functions reference" (`CS:92-93`). The split itself also disagrees:
  "**16 read it, 7 write it, 2 do both**" (`CS:604`) against "read only  : 16" (`CS:1211-1213`).

**C-V67 [ledger] — the size of the sidecar corpus.** *No favoured side.*
- "hold **674** files. **620 parse**, **52 are zero bytes**" (`CS:451-452`).
- "**337 files**" (`CS:556`), with "**26 zero-byte sidecars in all 337**" (`CS:566-567`). 674 = 2 × 337; neither section says the two
  directory spellings are duplicates.

### 3.2 Stale "open / not read" claims, corrected claims repeated unstruck, and banner disagreements

| # | stale side (quoted) | answering / correcting side (quoted) |
|---|---|---|
| C-S1 | README lists REF, UNL and BIG as "**PARTIAL, tier 1.**" (`README:136`, `README:142`, `README:150`). It lists 4 of 22 system pages (`README:133-156`) | front matter `status: DOCUMENTED` (`REF:4`, `UNL:4`, `BIG:4`); the other 18 pages carry their own AUDITED status |
| C-S2 | "**at least one admissible reference** \| ~~156~~ **157** \|" and "**no admissible reference of any kind** \| ~~2~~ **1** \|" (`README:52-53`) | "**The count is now 158 of 158, and the entry has no exceptions left.**" (`U158:915`); "REFUTED 2026-09-16 (FABLE)" (`DB:31`) |
| C-S3 | "\| Direct authored strings \| **0** \|" (`README:20`) | GQ says that row "is corrected by §8 above" (`GQ:1552-1553`) |
| C-S4 | body banners "**PARTIAL.**" (`CTX:35`, `DISP:37`) | front matter `status: AUDITED — every register row is closed` (`CTX:4`), "DOCUMENTED -> AUDITED" (`CTX:26`); `DISP:4`, `DISP:27` |
| C-S5 | "**`PARTIAL` deliberately.** … **None of the three is identified.**" (`BIG:49-50`) | `status: DOCUMENTED` (`BIG:4`); identifications at `BIG:57`, `BIG:928`, `BIG:973`, `BIG:1383` |
| C-S6 | DB's front matter: system "The nine-patch box renderer that is never called" (`DB:2`), `status: AUDITED`, `reopened_count: 0` (`DB:4`, `DB:26`). Body, unstruck: "**It is never invoked.**" (`DB:143`), "<- NOTHING reaches this" (`DB:176`), "**Upstream: none.**" (`DB:382`), "**Do not patch this expecting a visual change.**" (`DB:400`) | "REFUTED 2026-09-16 (FABLE)" (`DB:31`); "**`00392A10` is reachable by a static route.**" (`DB:33`); "**So the island is not dead.**" (`DB:59`) |
| C-S7 | CS (dated 2026-09-18, after the refutation): "the renderer itself still has no caller" (`CS:1335`); "genuinely dead" (`CS:679-680`). U158: "**`00392A10` is one of the fifteen no-caller residuals**" (`U158:602`) | `DB:31-33`; "**REFUTED 2026-09-16 (FABLE) — a caller exists, and it is a conditional jump.**" (`U158:945`) |
| C-S8 | "**The corrected figure is 144 of 158 with a direct caller, and 1 of 158 with" no admissible reference (`CS:639`); "The corrected figure is **1 of 158, not 2**" (`DB:163`) | `U158:915` (158 of 158); `DB:31-33` |
| C-S9 | "the full re-census has not been run" (`CENSUS:1017-1019`) | "**The re-census has now been run" (`README:45`); `U158:915` |
| C-S10 | "96 % of their incoming references are banned exception metadata" (`U158:1066-1067`, unstruck) | "**QUALIFIED 2026-09-02.**" (`README:35`) |
| C-S11 | "Fifteen have no caller at all" (`U158:618`, also `U158:47-48`, `U158:990`) | "the number re-measures as thirteen" (`U158:266`); the first statement struck at `U158:255-256` |
| C-S12 | "**Eight of 158 have been read**" (`U158:152`); "The first five read" (`U158:471`) | `U158:228` counts nine described; "Every member now has a reading" (`U158:243`) |
| C-S13 | "**24,116 functions - 70.4 % of the executable - are classified but unexplained.**" (`CENSUS:38`) | §15: against all 38,161 functions it is "**63.2 %**" (`CENSUS:783-786`) |
| C-S14 | "8 in _RDATA" (`CENSUS:124`; also `CENSUS:820`) | "**The `_RDATA` 8 were never real.**" (`CENSUS:915`) |
| C-S15 | "Which strings those are is not established here." (`GQ:73-74`); "strings tagged "ex" go elsewhere" (`GQ:100`) | "question's premise was inverted: `002B0280` draws the strings that are NOT `ex`.**" (`GQ:675`) |
| C-S16 | "`edx = movsx(00265270())` is the field id" (`CS:1605-1606`); `fieldVar = FieldData_GetVariable0();` (`CS:845`); "field variable `0x19`" (`CS:854-855`) | "**The two values in `001ED130` are story progress, not places.** … corrected in place" (`CS:1715-1723`). **Favoured: story progress.** It names the operand, not the compared constants |
| C-S17 | "\| `{i}` \| — \| 3 bytes \| an inline icon \|" (`GQ:250`, also `GQ:61-62`) | "the three bytes have no reader in this build" (`GQ:727`) |
| C-S18 | "`projectCallback(&packed[4], &TL);`" (`GQ:482`) | "**ANSWERED 2026-09-18 (FABLE): there is no callback." (`GQ:769`) |
| C-S19 | key-address row: "**a pool of six ± axis vectors, not a matrix object.**" (`GQ:342`) | "~~Correction 2026-09-02 — `008C5F80` is a vector pool, not a 4×4 identity~~" (`GQ:1602`); the pool reading is itself overturned (`GQ:1503`, `GQ:1571`) |
| C-S20 | `002AC5F0` "still residual" (`PAINT:190`, `PAINT:196`); "The largest unclassified function in the game is not called by name from anywhere." (`DISP:32`) | "classified at GN162 as `UI.Text.ControlCodeInterpreter`" (`DISP:43`, `U158:216`) |
| C-S21 | "the suspend flag is off" (`PAINT:273-274`); "the values are seeded once at construction" (`PAINT:269-271`) | "**CORRECTED — `+0x2379` is not a suspend flag.**" (`PAINT:359`); "**An earlier version of this row concluded it was written once ever and never again**" (`PAINT:536`); the begin re-seeds them (`PAINT:180-182`) |
| C-S22 | "The score therefore still reads 154 unresolved" (`PAINT:570-571`) | "**158 → 139**" (`PAINT:194-195`); now 30 (`U158:1129`) |
| C-S23 | §3 rows "**not read**" (`RT:202-203`); §4.1 "**null means the whole call failed**" (`RT:211`); "the five callees … were **not read at all**" (`RT:392-393`) | UQ-359: all five read (`RT:294-296`); "**This falsifies §4.1's “null means the whole call failed”.**" (`RT:314`) |
| C-S24 | "**The surface is now closed — all eighteen implementations have been opened.**" (`API:76`) | "**the three unread callees still carry none, and are marked unread rather than anchored.**" (`API:230`) |
| C-S25 | the "2x scale mode" label, unstruck (`DISP:198`, `DISP:221-222`, `DISP:262`) | "**Name corrected 2026-09-21 (FABLE), same day.**" (`DISP:149-154`) |
| C-S26 | the falsification note says §4's listing has "no null test" (`DISP:713-716`; front matter `DISP:24`) | the listing now has "`; omitted from this listing -- §10`" `test rax, rax` / `je ret` (`DISP:120-121`) |
| C-S27 | §7 open: "What `002AC2F0` decodes." (`CBC:239`); `+0x10FC`/`+0x1102` "mode bytes"; "What `0020E600` returns." (`CBC:239-240`); why every twenty characters (`CBC:241-242`) | `+0x1102`: "**ANSWERED 2026-09-14 (FABLE): it is the line-start flag.**" (`GQ:1735`); `002AC2F0` read (`GQ:747-754`); the twenty-item flush (`CBC:312`, `GQ:841`). `0020E600` remains disputed (C-V8) |
| C-S28 | "**Still owed: a first falsification pass, by a session that did not write this.**" (`GQ:1395`) | "Falsification pass 1 — 2026-09-03" (`GQ:1468`); front matter `falsification_passes: 1` (`GQ:26`) |
| C-S29 | "`4` — the vertex count" (`RECT:122`; also `RECT:177`) | "**the `4` beside it is the register list - XYZF2 - not a vertex count**" (`RECT:138`, FABLE 2026-09-18). **Favoured: the register list.** A port emitting the packet bytes is unaffected |
| C-S30 | the indirect call reading (`RECT:157-160`, `RECT:165-167`); §7 "The target of the indirect call in §5." (`RECT:183`) | "**CORRECTED 2026-09-18 (FABLE): there is no dropped indirect call.**" (`RECT:162`) |
| C-S31 | "**exactly 60 frames**" (`BLINK:36-37`); "**`DAT_0208F570` is a frame counter" (`BLINK:50`) | "**one second at 60 Hz whatever the present interval**" (`BLINK:287`; front matter `BLINK:4`) |
| C-S32 | "**An out-of-range colour id does not fail — it draws at flat mid-grey.**" (`BLINK:120`) | outside `ch`/`in`, "the default is the shipped behaviour there, not a fallback" (`BLINK:288`) |
| C-S33 | falsification row: "the three references it has are all `DATA`" (`BLINK:292`) | "`002B6427  lea r8, [rip + 0x1752]      ->  002B7B80        (inside 002B6350)`" (`BLINK:176`) |
| C-S34 | "What `002D8530`, `002DBDD0`, `00403970`, `00403BC0`, `00404120` and `00404730` do." (`BLINK:310`); what `003BC160` … enumerate (`BLINK:311`) | `002DBDD0` is RECT's subject; `00403970` at `RECT:255-262`; `002D8530`, `00403BC0`, `00404120` at `ICON2:200-224`; `003BC160` at `BLINK:382-390` |
| C-S35 | `residual-crossref.tsv` described as 139 rows with "the ~~89~~ 84 residual functions no page cites … with an empty `pages` column" (`U158:1246-1266`) | the member file has 30 rows, all `interior_cited=yes`, none with an empty `pages` |
| C-S36 | "What `002DD4B0` tests, and therefore which of the two paths actually runs." (`NINEP:234`; also `NINEP:98-99`) | "**`002DD4B0`** (7 B) returns the word `0215E6D0`" (`WTREE:258`); `DB:447` (UQ-352). On NINEP itself, `NINEP:126-127` is answered by UQ-351 at `NINEP:130` |
| C-S37 | `001AED50` "**NOT CLAIMED: what it does**" (`NINEP:321-323`); `001B06D0` "bump-allocator" (`NINEP:274-275`) | "`001AED50` (534 B) is a `0x30`-stride vector erase/move helper" (`NINEP:351`); "`001B06D0` never allocates — it only rewinds" (`NINEP:307`) |
| C-S38 | "**What it draws is not established**" (`ICON2:145`, `ICON2:162`); subsystem: "**the twin's document does not claim this either" (`ICON2:165`) | `002DD2F0` "translates a child rect by the parent object's origin" and clips; it does not draw (`ICON2:191-193`, `RECT:246-250`); "**Answered 2026-09-26 (FABLE, Claude Opus 5.5): the track map's markers.**" (`BLINK:296`) |
| C-S39 | `002DD7B0` "some per-style boolean, and that is as far as this goes" (`WBG:230-232`); `002DAC70`/`002DAF30`/`002DD4B0` listed as unknown (`WBG:230`) | `002DD7B0` "is the `fontcolor` shadow-byte getter" (`WTREE:258`; `BLINK:288`); `002DAF30` is read on the same page (`WBG:263`) |
| C-S40 | "\| `+0x88` \| a **countdown**; states 3 and 7 decrement it and act at zero \|" (`MEASURE:206`); "**Both constants are 30 or one less.**" (the 30-frame period, `MEASURE:261`); the 60-frame cycle (`MEASURE:219-221`) | "3 steps the target by `+0xA0` on every tick while `+0x88` is non-zero" (corrected 2026-09-30, `MEASURE:288`); "30 is the denominator of a rate, not a frame count." (`MEASURE:215`, `MEASURE:222`). **Favoured: the 2026-09-30 corrections** |
| C-S41 | "What states `0`, `1`, `4`, `5` and `7` of §5 distinguish" (`MEASURE:283`); cluster row "unread" (`MEASURE:295`) | SD-100 answered (`MEASURE:288`); "all 13 have a reading since 2026-09-18, UQ-383" (`MEASURE:294`) |
| C-S42 | "**The third call is gated on flag bit 12** and the first two on bit 24" (`WTREE:113-114`) | same line, 2026-09-30: all three need bit 24 = `0208F564`; messages 3/4 also need bit 28 clear (`WTREE:114`) |
| C-S43 | CS "not read" lines: commands "none of their bodies was read." (`CS:917-918`); `FUN_00267310` unknown (`CS:1060-1062`); bit assignments "none of which was read." (`CS:1171-1173`); consumers (`CS:307-308`, `CS:766`); predicates (`CS:774-775`) | answered at `CS:408-411` and §12 (`CS:925-926`), §13 (`CS:1071-1082`), `CS:419-436`, `CS:386-392`, `CS:396-400` |
| C-S44 | "about fifteen functions" (`CS:159`) | "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): twelve functions, not about fifteen, and each has a role.**" (`CS:506`) |
| C-S45 | "**What the prefixes denote is not established here**" (`CS:174-175`) | `sum_` = summons (`CS:327`); "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): `spc_` is the special-attack (`spattack`) event.**" (`CS:346`) |
| C-S46 | "**Still open, and it is what the row now asks:** what the 64-bit value selects." (`CS:1454`) | "**ANSWERED 2026-09-18 (FABLE): it is a VIF1 UNPACK header" (`CS:1436`) |
| C-S47 | "`0024AF50` (368 B) is a cutscene-slot body" (`CS:1635`) | its caller `0024A710` "is not cutscene code" — "**Corrected 2026-09-30 (SWE2-EC7, SWE2-CONTRACT's DD batch 6):**" (`CS:1631`) |
| C-S48 | DB: "`0020AC30` on this page calls `FUN_0020a800`" (`DB:682`); front matter "cites record(s) 0020AC30" (`DB:13`) | `0020AC30` is CS's subject; the same paragraph is at `CS:1522` |
| C-S49 | status line: "The population readers still read only merge verdicts" (`CUT:4`); "The 159 extensions not yet applied are prepared" (`CUT:175`) | "**Resolved 2026-09-30 (OPUS, `d20226c17`, the chained-tails apply).**" (`CUT:233`); "The 159 extensions applied (OPUS, 2026-09-29)" (`CUT:221`) |
| C-S50 | "larger bands stay NOT YET" (`UNL:469-470`, also `UNL:872`); "no block matched to a named routine" (`UNL:488`); 2026-09-16 sections using `.pdata` as "**positive evidence for the leading reading**" (`UNL:760`, `UNL:785-786`) | "Every UC-1 size band is now adjudicated" (`UNL:935`); UC-3 byte match (`UNL:445-453`); the pass-6 ban on `.pdata` (`UNL:148-154`, re-applied `UNL:442`) |
| C-S51 | "The denominator is NOT changed by this document." (`UNL:431`; also `UNL:749`) | applied populations 34,965 / 35,064 / 35,065 (`UNL:871`, `UNL:903`, `UNL:930`) |
| C-S52 | "**No operation body was read.**" (`BIG:1364`, also `BIG:775`); kind 0x52: "Its meaning is not read here (`SD-123`)" (`BIG:1515-1516`) | the eight palette effects (`BIG:928`); "SD-123 answered 2026-09-30" (`BIG:226`) |
| C-S53 | "first-writer-wins" (`REF:319`, 2026-09-16, unstruck); "`[rcx+0xB8]` is that movement body" (`REF:228`) | "**writes `cl` only if the byte is non-zero** (`cmovne`, corrected 2026-09-18)" (`REF:189`, also `REF:68`); "not “the movement body”" (`REF:229`) |
| C-S54 | section headed "SWE2-EC7-18 update (2026-05-15)" (`GQ:1835`, `ICON2:198`) | every other dated section on both pages is 2026-09-xx; the date is out of sequence |
| C-S55 | UQ-367 superseded with its population "is carried by 99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md" (`GQ:1239`) | that is GQ itself: the pointer is circular |
| C-S56 | "**Corrected 2026-09-14 (OPUS): two of the four are no longer residual.**" (`GQ:226`) | "Three of the four are now classified" (`GQ:223`); `002AF960` "followed" at GN161 (`GQ:228-229`) |
| C-S57 | two `parent_tag` values: "parent_tag: GN162" / "parent_tag: GN159" (`RT:12`, `RT:19`; likewise `CTX:11`/`CTX:18`, `DISP:12`/`DISP:19`) | one checkpoint per page is expected by the front-matter shape of every other page |
| C-S58 | front-matter review fields older than the body: `last_reviewed` 2026-09-02/03 with `reopened_count: 0` on GQ (`GQ:21`, `GQ:31`), CBC (`CBC:19`), PAINT (`PAINT:19`), CS (`CS:20`, `CS:26`), DB (`DB:20`, `DB:26`), BIG (`BIG:18`), CENSUS (`CENSUS:21`), RECT, BLINK, NINEP, ICON2, WBG (each `:19`) | body corrections dated up to 2026-10-01 on the same pages (for example `CS:1790`, `BLINK:391`, `BIG:4`) |

### 3.3 Checked and found consistent (not contradictions)

- **SD-103 row arithmetic.** CTX says the three pointer slots sit at "**no** row boundary of the `+0x000` table (`174.67`, `175.67`,
  `176.67`)" (`CTX:188-190`), and that "they are rows 174–176 of the `+0x000` table" (`CTX:349`). Both hold:
  `174 × 24 + 0x10 = 0x1060`, `175 × 24 + 0x10 = 0x1078`, `176 × 24 + 0x10 = 0x1090`. The slots are the third qword (`+0x10`) of rows
  174–176, the field `CTX:175` marks "not read in this pass".
- **Dispatch base.** `00120000 + 0x7F64D0 = 009164D0`, column 2 of table `009164C0` (`DISP:323`, `U158:524`).
- **Batcher slots.** 64 slots × `0x58` = `0x1600`, and `0x2328 + 0x1600 = 0x3928`, the slot index (`NINEP:299-302`, `RECT:140`).
- **README's body sizes.** "289 B to 7,489 B, mean ~1,132 B, 181,146 bytes total" (`README:99`) is the 160 set:
  180,134 (U158's 158, `U158:89-90`) + 289 + 723 (the two closed rows, `README:107-108`).
- **`00729920`.** 189 B recorded + 131 beyond = 320 (`CUT:90`). `UNL:849-850` agrees that 189 B "stops short".
- **Fixed-point colour.** `0x80` = 1.0 with `>> 7` agrees across RECT (`RECT:91-92`), BLINK (`BLINK:119`), ICON2 (`ICON2:110-111`),
  WTREE (`WTREE:153`), DB (`DB:438`, `DB:459`) and CBC (`CBC:224`).
- **GS state pairs.** `00400E80`'s pairs `{0x1001,0x47}`, `{0x44,0x42}` (`ICON2:255`) match RECT's words 2–5 (`RECT:115-118`, `RECT:138`).
- **Atlas entry decode.** 8-byte entries, `u = entry[+4] & 0xFFF`, `v = entry[+4] >> 12 & 0xFFF` agree in BLINK (`BLINK:73-77`), WBG
  (`WBG:65-66`) and ICON2 (`ICON2:71-80`).
- **The 30.** README "**30**" (`README:9`), U158 `unresolved=30` (`U158:53-54`), and `residual-30-GN161.tsv` (30 rows) agree.

---

## 4. Rating

**NOT YET** overall. The folder is a residual ledger, and the systems it reads out have structural gaps. On the text and nine-patch
paths, the pages disagree with each other about core behaviour.

| part | rating | why |
|---|---|---|
| Ledger pages (README, U158, CENSUS, UNL, REF counts, CUT) | **not a port target** | They measure classification coverage and define no runtime behaviour. Their counts disagree in many places (C-V39–C-V48, C-V54, C-V56, C-V65–C-V67, C-S1–C-S14). This matters to the bookkeeping, not to a re-implementation |
| Text pipeline (GQ, CBC, RT, PAINT, API, CTX, DISP, MEASURE) | **NOT YET** | No frame-level order across the widget pass, message window, reveal stepper, painter begin/flush and buffer swap (S-1). Control-code meanings (C-V1), the glyph cache's nature (C-V2), the compiled-stream byte meanings (C-V14), what `0020E600` returns (C-V8) and which functions draw (C-V13, C-V15) are each stated two ways. `TextState`, the `~0xD0` state, the 32-byte line record and the 16-byte GS record are partial (S-2, S-3, S-5). The painter's offscreen path may be unreachable: "**Whether anything sets `+0x2378` at all**" (`PAINT:546-547`). The parts that are stated well are a solid base: the ladder table (`PAINT:88-119`), the 44-byte records (`PAINT:137-151`), the render-target key and selection (`RT:60-193`), the pen and UV formulas (`GQ:454-506`) and the glyph table (`GQ:389-401`) |
| Widget tree and backgrounds (WTREE, WBG) | **MOSTLY** | The gate, recursion, transform, brightness and clip rules are stated (`WTREE:52-153`), as are the background descriptor and colour tables (`WBG:62-155`). Open: message 3/4/5 semantics (G-17), node layout (S-12), `002DAF30`'s source (C-V36), the word count (C-V61), and pass order within a frame (S-1) |
| Rectangle primitive (RECT) | **MOSTLY** | The tint formula and the GS packet are decoded (`RECT:63-142`). The batcher path is the one drawn (`RECT:142`). Open: `context + 0x70` and the `00181870`/`00181930` arguments (G-13), the `+0x2C` slot init (C-V35) |
| Nine-patch frame (NINEP, DB) | **NOT YET** | The inputs, the 3×3 derivation and the guard are stated (`DB:302-341`, `NINEP:57-75`). But the per-cell flag rule (C-V3), the corner blend (C-V4), what the fallback draws (C-V5) and which function opens the bracket (C-V7) all conflict. The GS words of `002DC290` are not decoded (S-13) |
| Icons (BLINK, ICON2) | **MOSTLY** | The pulse, the atlas decode, the palette fallback and the tick counter are stated (`BLINK:47-123`, `BLINK:287-288`). Open: the `01E0CE60` overwrite (G-15), the record layout (S-14), whether `002BCB00` reads or writes its position globals (C-V17), and `002DD7E0`'s role (C-V18) |
| Cutscene name slots and DoF sidecar (CS) | **MOSTLY** | Entry, caller chain, slot record, classification order, sidecar keys and the stand-down predicates are stated (`CS:72-264`, `CS:847-905`). Use the favoured side of C-V31 (latch). Open: where the DoF values go and the source object (S-15), the recorder address (S-16), command offsets (C-V32), the flag-B consumer set (C-V33) |
| Render-model binding machine (BIG) | **NOT YET** | The dispatch, the handle and pool layouts and the init are stated (`BIG:697-923`). But which opcode is which palette effect is not stated, nor what the two MMI kernels compute (S-17). Register-bank extents (C-V49, C-V50), tag values (C-V52) and call counts (C-V53) disagree. The payload is 48 B (C-V51, favoured) |
| Effect element type `0x05` mesh draw (BIG chain B) | **NOT YET** | The mesh record and the `+0x1F1` builder are stated (`BIG:1413-1426`, `BIG:1492-1496`). What each of the three draw paths does differently, and the parameter entries, are unread (G-19) |
| Script-verb tail bodies (REF) | **MOSTLY** | The fourteen bodies are decoded instruction by instruction, with verb mappings (`REF:61-76`, `REF:225`). Tail targets `00263A30`, `00269860`, `003B1560`, `004256E0`, `002E1CD0` are named only. The 129 unlisted-only blocks are unread (G-18) |
| libvpx VP8 SIMD (UNL) | **READY** (as a dependency) | Pinned to libvpx 1.6.0 by byte match. The 63 head blocks are dead, and the rtcd pointers are named (`UNL:443-453`). A port links the library. The page itself does not name the 159 routines (S-18) |
| Deferred-work queue `0024B580` (U158) | **NOT YET** | The walk is stated (`U158:1300-1351`). The kinds, the callees and the schedule are not (G-21, S-20) |
