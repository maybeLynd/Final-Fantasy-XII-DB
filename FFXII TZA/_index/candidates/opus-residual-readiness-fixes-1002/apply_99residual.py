"""apply_99residual.py [--apply] - 99-Unresolved-Residual readiness map (cloud-reports/re-readiness/99-residual.md),
section 3.1 value-changing items C-V1..C-V67 and section 3.2 stale / unstruck / banner items C-S1..C-S58, decided at
the shipping image and the shipped data and settled on the pages (OPUS, 2026-10-02).

Each value edit strikes the side the image or the shipped data refutes and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* with the deciding instruction cited as ENTRY+offset. Each stale edit adds
*(answered: see ...; 2026-10-02, OPUS)* beside the stale words, without upgrading any status label.
Every ~~ span opens and closes on one line. Code-block lines get a trailing `<- corrected` comment (their OLD includes
the line end, so NEW never contains OLD); front-matter lines get a trailing `# <- corrected` comment on single-line
values only. No heading is changed. Nothing inside a pass-22 crossing section or an "Interior citations ... (OPUS,
2026-10-02, cloud-drafted)" section is edited. No .tsv, _types or OPEN-QUESTIONS edit.
Items decided as "both right / different scopes" and items left out are listed in
scratchpad res99/verdicts-99.md, not here.
OLD matches in either LF or CRLF form (the pages have mixed line endings); each OLD must occur exactly once.
Dry run unless --apply; prints FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "99-Unresolved-Residual/"
README = F + "README.md"
GQ = F + "Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md"
CBC = F + "Glyph-Run-Rendering/drawing-a-line-character-by-character.md"
RT = F + "Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md"
PAINT = F + "Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md"
API = F + "Glyph-Run-Rendering/the-font-painters-public-api.md"
CTX = F + "Glyph-Run-Rendering/the-shared-drawing-context.md"
DISP = F + "Glyph-Run-Rendering/the-text-element-dispatch-table.md"
CS = F + "Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md"
DBX = F + "Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md"
REF = F + "Unlisted-Code/referenced-code-the-list-never-had.md"
CUT = F + "Unlisted-Code/the-bodies-the-list-cuts-short.md"
UNL = F + "Unlisted-Code/the-code-the-function-list-does-not-contain.md"
BIG = F + "Largest-Unclassified-Code/the-largest-unclassified-functions.md"
CEN = F + "Unowned-Code-Census/why-the-unowned-code-has-no-owner.md"
U158 = F + "the-unresolved-158.md"
RECT = F + "drawing-one-coloured-rectangle.md"
MEAS = F + "measuring-text-by-drawing-it-with-the-output-off.md"
BLINK = F + "the-blinking-icon-and-its-atlas.md"
NINEP = F + "the-nine-patch-window-frame.md"
ICON2 = F + "the-second-icon-drawer-and-what-it-adds.md"
WBG = F + "the-widget-background-and-its-atlas-sets.md"
WTREE = F + "the-widget-tree-draw-pass.md"

C = "*(corrected 2026-10-02, OPUS: "
A = "*(answered: see "
T = "; 2026-10-02, OPUS)*"
REACH = "`00392A00` is `cmp word [rcx+0x58], 0` then `jne 00392A10` at `00392A00`+0x5, and `00392A00` has four callers"
REACH_ROLE = ("the nine-patch box renderer is entered by a conditional jump at +0x5 of its 12-byte opacity gate, "
              "and that gate has four callers")

EDITS = [
    # ---------------- 3.1 value-changing ----------------
    # C-V1: 003647E0 code 1 is the figure space (the 0x30 scan at +0xB3, ungated); 3 is undim (+0x63), 2 dim; only
    #       2 and 3 test [+0x63] bit 0 (+0x70, +0x5A).
    (GQ, "opcode 1 copies `[rdi+0x37]`→`[rdi+0x33]` (`00364843`), opcode 2 writes `[+0x37]/5` via the `0xCCCCCCCD` "
         "multiply (`0036485E`–`00364868`), opcode 3 scans the `[022CBE00]` layer's `0xC`-stride table for "
         "`word == 0x30` (`00364893`) — all gated on `byte[rdi+0x63] & 1` |",
     "~~opcode 1 copies~~ opcode 3 copies `[rdi+0x37]`→`[rdi+0x33]` (`00364843`), opcode 2 writes `[+0x37]/5` via the "
     "`0xCCCCCCCD` multiply (`0036485E`–`00364868`), ~~opcode 3 scans~~ opcode 1 scans the `[022CBE00]` layer's "
     "`0xC`-stride table for `word == 0x30` (`00364893`) — ~~all gated on `byte[rdi+0x63] & 1`~~ only opcodes 2 and 3 "
     "gated on `byte[rdi+0x63] & 1` " + C + "code 1 branches to `003647E0`+0x91 and scans for `0x30` at +0xB3 "
     "with no gate; code 3 tests `[rdi+0x63]` at +0x5A and copies at +0x63; code 2 tests it at +0x70 — §2's table is "
     "right)* |"),
    # C-V2: 00364210 is the LRU fill (unlink tail +0x1B..+0x49, round to 8/16/32/64/128 at +0xC0..+0x124, returns the node
    #       +0x14D); 00365FD0 moves the hit node to the list head (+0x2C..+0x9B).
    (GQ, "| `00364210` (367 B) | the span clipper — u16 tag scan over `[022CBE00]` records, then `byte[rcx+2]`/`byte[rcx+3]` "
         "clamped against the `edx`/`ebx`/`ebp`/`r14d` bounds, returning the clipped span in `eax`/`edx` "
         "(`003642D0`–`00364338`) |",
     "| `00364210` (367 B) | ~~the span clipper~~ the glyph-cache fill on a miss — it unlinks the list tail "
     "`[022CBE00+0x228]` and relinks it at the head `+0x230` (`00364210`+0x1B..+0x49), then a u16 tag scan over "
     "`[022CBE00]` records, then `byte[rcx+2]`/`byte[rcx+3]` ~~clamped against the `edx`/`ebx`/`ebp`/`r14d` bounds, "
     "returning the clipped span in `eax`/`edx`~~ rounded up to 8, 16, 32, 64 or 128 and stored at node `+0x14`/`+0x15`, "
     "returning the node in `rax` (`003642D0`–`00364338`) " + C + "`00364210`+0x14D `mov rax, r8` returns the "
     "node, 0 on a miss; §3's `GlyphCache_FillOnMiss` row is right)* |"),
    (GQ, "with `r8d`/`edx` range checks and a `byte[rax+0x13]` flag (`00365FE7`–`00366073`) |",
     "with ~~`r8d`/`edx` range checks~~ an exact match of the font byte `+0x12` against `edx`, a move of the hit node "
     "to the list head `+0x230`, and a `byte[rax+0x13]` flag (`00365FE7`–`00366073`) " + C + "the relink is "
     "`00365FD0`+0x2C..+0x9B; §3's `GlyphCache_PromoteOnHit` row is right)* |"),
    # C-V3: no-split arm: index 2 gets 4, others 0 (00392A10+0x24C cmp esi,2 / mov eax,4 / cmovne eax,ecx).
    (NINEP, "     flags = (index == 2) ? 0 : 4;     // no split\n",
     "     flags = (index == 2) ? 0 : 4;     // no split   <- corrected 2026-10-02, OPUS: (index == 2) ? 4 : 0 - "
     "00392A10+0x24C is cmp esi, 2 / mov eax, 4 / cmovne eax, ecx (the box-renderer page's reading)\n"),
    # C-V4: the & 8 blend is (((c0 + c1) >> 1 + c2) >> 1 + c3) >> 1 per byte (002DC7F0+0x253..+0x305).
    (DBX, "blended = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   // per channel\n",
     "blended = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   // per channel   <- corrected 2026-10-02, OPUS: "
     "blended = (((c0 + c1) >> 1) + c2 >> 1) + c3 >> 1 per byte, no >> 24 term (002DC7F0+0x253..+0x305; UQ-353 replay "
     "below)\n"),
    (DBX, "blended_channel = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);\n",
     "blended_channel = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   <- corrected 2026-10-02, OPUS: "
     "(((c0 + c1) >> 1) + c2 >> 1) + c3 >> 1 per byte, weights 1/8, 1/8, 1/4, 1/2 (002DC7F0+0x253..+0x305)\n"),
    # C-V5: 00392CE0 is a 3x3 loop calling 002DC290 per non-empty cell (+0x193), special-casing cells (0,0) and (2,2).
    (DBX, "        FUN_00392ce0(ctx, rect, colours);      // ONE gradient quad, no slicing\n",
     "        FUN_00392ce0(ctx, rect, colours);      // ONE gradient quad, no slicing   <- corrected 2026-10-02, OPUS: "
     "nine slices - a 3 x 3 loop (00392CE0+0x1B6, +0x1C6) calling 002DC290 per non-empty cell (+0x193)\n"),
    (DBX, "The fallback `00392CE0` builds a single quad — four\ncorner positions and the same four colours, arranged 2×2 — "
          "and hands it to `002DC290`, the live",
     "The fallback `00392CE0` ~~builds a single quad — four~~\n~~corner positions and the same four colours, arranged "
     "2×2 — and hands it~~ walks the nine cells in a 3 × 3 loop and hands each non-empty one " + C + "loop bounds at "
     "`00392CE0`+0x1B6 and +0x1C6, the `002DC290` call at +0x193, cells (0,0) and (2,2) special-cased at +0x1F7; the "
     "nine-patch window frame page's reading)* to `002DC290`, the live"),
    (DBX, "The un-sliced path: one gradient quad |",
     "The un-sliced path: ~~one gradient quad~~ nine `002DC290` slices " + C + "`00392CE0`+0x193 inside the 3 × 3 "
     "loop)* |"),
    # C-V6: 002DC290 has 11 calling functions / 17 sites including 00392CE0, so 10 others.
    (DBX, "| `002DC290` | — | 1363 B | The **live** cell drawer, 11 other callers — not dead |",
     "| `002DC290` | — | 1363 B | The **live** cell drawer, ~~11 other callers~~ 10 other callers, 11 in all with "
     "`00392CE0` " + C + "rel32 sweep: 17 sites in 11 functions)* — not dead |"),
    (DBX, "   |      \\-> 002DC290  1363 B  the LIVE cell drawer  (11 other callers - not dead)\n",
     "   |      \\-> 002DC290  1363 B  the LIVE cell drawer  (11 other callers - not dead)   <- corrected 2026-10-02, "
     "OPUS: 10 other callers (11 functions, 17 rel32 sites, with 00392CE0)\n"),
    # C-V8 / C-V10: 0020E600 is the 10-byte image-address resolver, 00229E40 a 7-byte getter of [01E02814]; no yield.
    (CBC, "`002A9F00`, `002AAE40`, `002AC2F0` and `002AE610` call the `CoreRuntimeScheduling` yield\n`0020E600`, and "
          "`002AC5F0` calls `00229E40` (8 edges). The account the pass asks for is that\nthese are the walk's yield "
          "points — the draw loop defers to the scheduler mid-glyph, which is\nwhy a text pass can be preempted "
          "between characters. `00229E40` is itself called by\n`Rewards_Progression_Economy` `00317ED0` — the shared "
          "yield accessor has economy-side callers\ntoo.)*",
     "`002A9F00`, `002AAE40`, `002AC2F0` and `002AE610` call the `CoreRuntimeScheduling` ~~yield~~\n`0020E600`, and "
     "`002AC5F0` calls `00229E40` (8 edges). ~~The account the pass asks for is that~~\n~~these are the walk's yield "
     "points — the draw loop defers to the scheduler mid-glyph, which is~~\n~~why a text pass can be preempted "
     "between characters.~~ `00229E40` is itself called by\n`Rewards_Progression_Economy` `00317ED0` — the shared "
     "~~yield accessor~~ getter has economy-side callers\ntoo.)* " + C + "neither is a yield: `0020E600` is "
     "`mov eax, ecx; add rax, [01F83530]; ret` (10 B), the image-address resolver, and `00229E40` is "
     "`mov eax, [01E02814]; ret` (7 B); no text pass is preempted through them)*"),
    (CBC, "`0020E600` returns. What the two render commands",
     "~~`0020E600` returns.~~ " + A + "§7 note: `0020E600` returns `ecx` plus the qword at `01F83530`, an image "
     "address — `mov eax, ecx; add rax, [01F83530]; ret`" + T + " What the two render commands"),
    (MEAS, "`002AAE40`, `002AC2F0`, `002AE610` call the `CoreRuntimeScheduling` yield `0020E600` and\n`002AC5F0` calls "
           "`00229E40` (7 edges), and `00229E40` is itself called by",
     "`002AAE40`, `002AC2F0`, `002AE610` call the `CoreRuntimeScheduling` ~~yield~~ `0020E600` and\n`002AC5F0` calls "
     "`00229E40` (7 edges) " + C + "neither is a scheduler yield: `0020E600` is the 10-byte image-address resolver "
     "`mov eax, ecx; add rax, [01F83530]; ret` and `00229E40` the 7-byte getter `mov eax, [01E02814]; ret`, so they "
     "are not preemption points)*, and `00229E40` is itself called by"),
    (CTX, "*(Pass 22 adjacency, 2026-09-14: `00254A10` calls the `CoreRuntimeScheduling` yield `00229E40`\n",
     "*(Pass 22 adjacency, 2026-09-14: `00254A10` calls the `CoreRuntimeScheduling` ~~yield~~ getter `00229E40` "
     + C + "`00229E40` is `mov eax, [01E02814]; ret`, 7 bytes, the read §3's listing shows at `00254A10`+0x4; it yields "
     "nothing)*\n"),
    (CTX, "The drawing-context setup yields to\nthe scheduler like every other leg of the text walk; the shared yield "
          "accessor is consumed from",
     "~~The drawing-context setup yields to~~\n~~the scheduler like every other leg of the text walk;~~ " + C + "`00229E40` is a 7-byte getter, not a "
     "yield)* the shared ~~yield accessor~~ getter is consumed from"),
    # C-V9: 0053E0B0 calls 003659F0 then 003649A0 twice (+0x159/+0x181, +0x1B2/+0x1D6); no 00364980, 002D8690, 002D87D0.
    (GQ, "     -> 002D8690 / 002D87D0  renderer selection\n",
     "     -> 002D8690 / 002D87D0  renderer selection   <- corrected 2026-10-02, OPUS: 0053E0B0 calls neither; it "
     "calls 003659F0 then 003649A0 twice (0053E0B0+0x159/+0x181 and +0x1B2/+0x1D6), without the ex test\n"),
    # C-V11: 0209C4D0 holds the objects whose handler 002A6190 registers them (+0x6B..+0xAE) and draws a nine-patch
    #        frame (+0x15E) and text (+0x202); "actor" comes from GFZ working names only.
    (U158, "compute **actor-state-aware input remapping**, is an **actor registry**.",
     "compute **actor-state-aware input remapping**, is ~~an **actor registry**~~ the live **message-window "
     "registry** " + C + "the slots are filled by the message handler `002A6190`, case 1 (`002A6190`+0x6B..+0xAE), "
     "whose same object draws a nine-patch frame through `00392A00` (+0x15E) and text through the font painter "
     "(+0x202); the four readers' bodies return the confirm-button mask while a window waits, and *actor* rests only "
     "on their GFZ working names — §\"It is connected\", `MessageWindowRecord`)*."),
    (U158, "and `0209C4D0` is an **8-slot actor\n      registry** whose readers",
     "and `0209C4D0` is an **8-slot ~~actor~~\n      ~~registry~~ message-window registry** " + C + "§11's correction, "
     "slots filled by `002A6190`+0x6B..+0xAE)* whose readers"),
    (CS, "identified as the readers of the eight-slot\n> actor registry at `0209C4D0`.",
     "identified as the readers of the eight-slot\n> ~~actor registry~~ message-window registry " + C + "the slots "
     "are filled by the message-window handler, the-unresolved-158 §11)* at `0209C4D0`."),
    # C-V12: 00364530 calls the mode-2 chooser 0017FD00 at +0xB0 and +0x169.
    (GQ, "| 12 call sites, **zero** render or scope calls, sharing",
     "| 12 call sites, **~~zero~~ two** render-target chooser calls and no scope call " + C + "`0017FD00` at "
     "`00364530`+0xB0 and +0x169, as the render-target page says)*, sharing"),
    # C-V13: 002B2150 measures a run (xmm6 width, xmm7 height, out-params at +0x315/+0x32F); it does not draw.
    (GQ, "`002B2150` draws each text run; `0x03` commits",
     "`002B2150` ~~draws~~ measures each text run " + C + "it sums the width in `xmm6` and the maximum height in "
     "`xmm7` and stores them to its out-parameters at `002B2150`+0x315 and +0x32F; it never calls the glyph draw)*; "
     "`0x03` commits"),
    # C-V15: 002AAE40 draws glyphs itself (0017F7C0 at +0x66E).
    (GQ, "**None of the three draws.** The glyph emitter is `002A9F00`, which is not among them. And the",
     "**~~None of the three draws.~~** ~~The glyph emitter is `002A9F00`, which is not among them.~~ " + C + "`002AAE40` "
     "draws: it calls the painter begin `0017FA10` at `002AAE40`+0x52C and the per-glyph draw `0017F7C0` at +0x66E, "
     "as `002A9F00` does)* And the"),
    # C-V16: both column-1 dispatchers store qword 0 to 0209CC48; the re-point is 002B4730's.
    (CTX, "not a flag clear: the dispatch\nre-points `0209CC48` at the record the swap selected and rewinds `0209CC50` "
          "to its start. The",
     "not a flag clear: ~~the dispatch~~\n~~re-points `0209CC48` at the record the swap selected and rewinds `0209CC50` "
     "to its start.~~ " + C + "the column-1 dispatchers clear it — `mov qword [0209CC48], 0` at `002ABEC0`+0x20 and "
     "`002ABF20`+0xF; the re-point to the selected record and the cursor rewind are the flush `002B4730`'s, at "
     "`002B4730`+0xB7 in the listing above)* The"),
    (CTX, "| `0209CC48` | ~~cleared by both column-1 dispatchers alongside the publish~~ the current render-buffer record, "
          "re-pointed with its cursor `0209CC50` at each dispatch (§3d; corrected 2026-09-30, SWE2-DATA) |",
     "| `0209CC48` | ~~cleared by both column-1 dispatchers alongside the publish~~ the current render-buffer record, "
     "~~re-pointed with its cursor `0209CC50` at each dispatch~~ (§3d; corrected 2026-09-30, SWE2-DATA) " + C +
     "both column-1 dispatchers store 0 here, `002ABEC0`+0x20 and `002ABF20`+0xF; it is re-pointed with its cursor by "
     "the flush `002B4730`, +0xB7)* |"),
    # C-V17: 002BCB00 reads 0209E5D8/0209E5DC (+0x112, +0x17A) and writes neither.
    (RECT, "body stores `0209E5D8`/`0209E5DC` and ends",
     "body ~~stores~~ reads `0209E5D8`/`0209E5DC` " + C + "`movd xmm1` loads at `002BCB00`+0x112 and +0x17A; no "
     "instruction in the image stores either)* and ends"),
    # C-V18: 002DD7E0 is the fontcolor palette getter: [0215E6C8 + id*8] or 0x80808080 (+0x1E).
    (NINEP, "`002DD7E0` fetches the `0x67`/`0x69` string then `0x68`/`0x6A` by the `ecx` arm,",
     "`002DD7E0` fetches the `0x67`/`0x69` ~~string~~ palette colour then `0x68`/`0x6A` by the `ecx` arm " + C +
     "`002DD7E0` returns the dword `[0215E6C8 + id × 8]`, or `0x80808080` at +0x1E when the id is out of range — the "
     "`fontcolor` palette the blinking-icon page reads, not a string)*,"),
    # C-V19: 00181460 expands a strip of n points into n-2 triangles of three 0x30-byte vertices; 15 functions call it.
    (NINEP, "`00181460` — 105 B, 9 A-measured callers; the `00181460(&points, 4)` grid fill this page's",
     "`00181460` — 105 B, 9 A-measured callers " + C + "the image has 16 rel32 call sites in 15 functions)*; the "
     "`00181460(&points, 4)` ~~grid fill~~ strip-to-triangle-list expansion " + C + "for each of the `n - 2` "
     "triangles it appends three `0x30`-byte vertices — the points `i`, `i+1`, `i+2` read through `rbx` — to the "
     "batcher singleton `001B1C00()` through `001B06D0`, the rectangle page's reading)* this page's"),
    (NINEP, "advances `rbx += 0x30` per column and `rsi += 0x30` per row — a (n-2)x3 stamp of\n`0x30`-byte "
            "vertex/quad records, exactly the interior ring a nine-patch needs between its\ncorner rows.",
     "advances `rbx += 0x30` per column and `rsi += 0x30` per row — a (n-2)x3 ~~stamp of~~\n~~`0x30`-byte "
     "vertex/quad records, exactly the interior ring a nine-patch needs between its~~\n~~corner rows.~~ read of "
     "`0x30`-byte source vertices, three per triangle " + C + "`rbx` is the source, passed as `001B06D0`'s second "
     "argument at `00181460`+0x38; the destination is the batcher `001B1C00` returns)*."),
    # C-V20: 002AC5F0 has seven callers; besides 002AAE40 there are six.
    (GQ, "`002B5730`** — the other four callers of the interpreter. **That",
     "`002B5730`** — ~~the other four callers~~ four of the six other callers " + C + "`002AC5F0` has seven calling "
     "functions; `002A9F00` and `002B2150` are the two not named here)* of the interpreter. **That"),
    # C-V21: 002ABEC0 has 5 calling functions (6 rel32 sites).
    (DISP, "`002ABEC0`'s `rcx` is **not the widget**. Its nine callers pass",
     "`002ABEC0`'s `rcx` is **not the widget**. Its ~~nine callers~~ callers " + C + "five functions, six rel32 sites — "
     "the 5 of §4's table)* pass"),
    (DISP, "every embedded base the nine callers use", "every embedded base ~~the nine callers use~~ its callers use " + C +
     "five functions, six sites)*"),
    # C-V22: 001B5FA0 is called from 25 sites in 23 functions: 21 in the band (the table lacks 0017FC00, 0017FC50,
    #        0017FC70) and the two outside.
    (API, "**Every function in FFXII that draws text goes through eighteen entry points**, and they were found",
     "**Every function in FFXII that draws text goes through ~~eighteen~~ twenty-one entry points** " + C + "a rel32 "
     "sweep finds 25 call sites of `001B5FA0` in 23 functions: 21 in the band, including `0017FC00`, `0017FC50` and "
     "`0017FC70`, which §2's table lacks, and the two consumers)*, and they were found"),
    (API, "**22 call sites, 18 distinct functions. Sixteen sit in one contiguous band, `0017F650`–`0017FD30`.**",
     "**~~22 call sites, 18 distinct functions. Sixteen~~ 25 call sites, 23 distinct functions. Twenty-one sit in one "
     "contiguous band, `0017F650`–`0017FD30`.** " + C + "rel32 sweep of `.text` for calls to `001B5FA0`)*"),
    (API, "**The surface is now closed — all eighteen implementations have been opened.** The three that were",
     "**The surface is ~~now closed — all eighteen implementations have been opened~~ not closed** " + C + "three "
     "band entries that fetch the singleton, `0017FC00`, `0017FC50` and `0017FC70`, are not in the table)*. The three "
     "that were"),
    # C-V23: 0017FD30 has 8 calling functions (18 sites).
    (CBC, "`0017FD30` — 63 B, 6 A-measured callers; the arg-marshal",
     "`0017FD30` — 63 B, ~~6 A-measured callers~~ 8 calling functions, 18 sites " + C + "rel32 sweep; the render-"
     "target page's eight)*; the arg-marshal"),
    # C-V24: 001FDD60 returns 0 on a miss (+0x4B) and node+0x28 on a hit (+0x46).
    (RT, "      - **`001FDD60` is the same algorithm byte for byte**, on the container at `[rcx+0xC0]` with",
     "      - **`001FDD60` is the same ~~algorithm byte for byte~~ walk with a different exit** " + C + "a miss returns 0, "
     "`xor eax, eax` at `001FDD60`+0x4B, and a hit returns `node + 0x28` at +0x46; the terminator is never returned)*, "
     "on the container at `[rcx+0xC0]` with"),
    # C-V25: 0017FA10 has 12 sites in 8 functions (adds 002AA800 and 002AAE40).
    (PAINT, "**Who calls it settles the residual cluster with a call edge instead of a string.** Eleven sites in\n"
            "seven functions, and",
     "**Who calls it settles the residual cluster with a call edge instead of a string.** ~~Eleven sites in~~\n"
     "~~seven functions~~ Twelve sites in eight functions " + C + "rel32 sweep; the kind-1 column-2 drawer and `002AAE40` call it too, "
     "at +0x3FD of the kind-1 column-2 drawer and at `002AAE40`+0x52C)*, and"),
    # C-V28: +0x9C is taken modulo 28 (001E8070+0x2B..+0x41), not divided by 7.
    (PAINT, "`dword[rdx+0x9C]` element count read (`001E808A`), magic-divide\n`0x92492493` (÷7, `001E809B`), "
            "`001E94E0` element resolve",
     "`dword[rdx+0x9C]` ~~element count~~ palette index read (`001E808A`), magic-divide\n`0x92492493` (~~÷7~~ "
     "modulo 28, `001E809B`) " + C + "`001E8070`+0x2B..+0x41 divides by 28 and subtracts `quotient × 0x1C`, so "
     "the argument is `[+0x9C] % 28`, §5's formula; a negative value takes `+0x1358` instead)*, `001E94E0` element "
     "resolve"),
    # C-V29: 001E7A20 moves 0x3C-byte elements (add rbx, 0x3c at +0x29).
    (PAINT, "| `001E7A20` (610 B) | `0x38`-stride vector insert —",
     "| `001E7A20` (610 B) | ~~`0x38`-stride~~ `0x3C`-stride vector insert " + C + "`add rbx, 0x3c` at "
     "`001E7A20`+0x29 and the `[r9-0x3c]` moves: the elements are the `0x3C`-byte vertices of §6)* —"),
    # C-V31: 0020AC30 stores the latch first (+0x34) and bounds it after (+0x3A); every exit runs through +0x218.
    (CS, "The first argument is a slot index, bounded before anything else happens:",
     "The first argument is a slot index, ~~bounded before anything else happens~~ stored to the latch first and "
     "bounded after " + C + "`0020AC30`+0x34 stores it to `01DFE40C`, +0x3A tests `≤ 4`; UQ-341 below)*:"),
    (CS, "It resets the latch to\n          `−1` when the name does not parse (`0020AE48`).",
     "It resets the latch to\n          `−1` ~~when the name does not parse~~ on every exit (`0020AE48`) " + C + "the "
     "out-of-range branch, the parse failure and the normal end all reach `0020AC30`+0x218)*."),
    # C-V32: the vertex offsets are from rdx = command + 0x10.
    (CS, "Then **four vertices**, each built the same way:",
     "Then **four vertices**, each built the same way " + C + "the offsets below are from `rdx`, which is "
     "`command + 0x10` (`lea rdx, [rbx+0x10]` at `002DC290`+0x7A), so vertex 0's colour sits at command `+0x60` and "
     "nothing overlaps the matrix at command `+0x20`–`+0x5F`)*:"),
    # C-V33: 00180120 calls the flag-B wrapper 001EC5C0 at +0x4.
    (CS, "it does not name flag B, so the consumer count stands. **PROPOSED-repos9e-20.**",
     "~~it does not name flag B, so the consumer count stands.~~ " + C + "it calls the flag-B wrapper `001EC5C0` "
     "at `00180120`+0x4, so it is a flag-B consumer — the count of four call sites below includes it)* "
     "**PROPOSED-repos9e-20.**"),
    # C-V35b: the record is 02EBEFC0 + index * 0x18; 02EBEFC8 is its buffer-pointer field.
    (NINEP, "**The command block is written into a ring** at `&DAT_02EBEFC8 + DAT_02EBEFF0 * 0x18`, and the ring",
     "**The command block is written into a ring** ~~at `&DAT_02EBEFC8 + DAT_02EBEFF0 * 0x18`~~ through the buffer "
     "pointer stored at `&DAT_02EBEFC8 + DAT_02EBEFF0 * 0x18` " + C + "that cell is field `+8` of the 24-byte record "
     "`02EBEFC0 + index × 0x18`; `002DC290` loads it at +0x5E and writes from buffer `+0x10`)*, and the ring"),
    # C-V36: 002DAF30 copies the 64 bytes at rdx (+0x41..+0x65); 02EBEFC0/02EBEFF0 select the buffer.
    (WTREE, "`002DAF30` loads four rows from `02EBEFC0` / `02EBEFF0` into the shared workbench and emits",
     "`002DAF30` loads four rows ~~from `02EBEFC0` / `02EBEFF0`~~ from its `rdx` argument into the shared workbench "
     + C + "`002DAF30`+0x41..+0x65 copies `[rdx]`..`[rdx+0x30]` to `022D8F30`..`022D8F60`; `02EBEFC0` / `02EBEFF0` "
     "only select the output buffer — the widget-background page's reading)* and emits"),
    # C-V38: 002D6990 has two callers (002D6CA0+0x75, 003C6B70+0x72C).
    (DBX, "`002D6990` (783 B) is the dead nine-patch draw body -",
     "`002D6990` (783 B) is the ~~dead~~ live nine-patch draw body " + C + "called by two functions, a bounded-loop caller at its +0x75 and "
     "`003C6B70` at +0x72C; UQ-355 keeps it live)* -"),
    # C-V39: the 158 run to 005DF890 (33 at or above 0x00500000); heaviest 64 KB page holds 13.
    (U158, "from `0x0018xxxx` to `0x004Fxxxx`. They are",
     "from `0x0018xxxx` to ~~`0x004Fxxxx`~~ `0x005Dxxxx` " + C + "recount of `residual_addrs.txt.GN158`: 37 pages, "
     "the last member in page `0x005D`, 33 members at or above `0x0050xxxx`)*. They are"),
    (U158, "heaviest single page holding 9.",
     "heaviest single page holding ~~9~~ 13 " + C + "pages `0x002A` and `0x0057` hold 13 each, same recount)*."),
    # C-V40: residual-30-GN161.tsv bands all 30 DESCRIBED.
    (U158, "pass on the 29 DESCRIBED bodies in",
     "pass on the ~~29~~ 30 DESCRIBED bodies " + C + "the member TSV's `band` column reads `DESCRIBED` on all 30 "
     "rows, `0036A2A0` included — the split stated in §\"what kind of work the 30 are\")* in"),
    # C-V41: R109's 109 rows include cluster members.
    (U158, "The 109 singletons named here are **no longer",
     "The 109 ~~singletons~~ bodies of `residual-109-classification.tsv` " + C + "the batch's rows include cluster "
     "members `002A4830`, `002A4430`, `002AF960` and `00256CA0`, so they are 109 of the 139, not the singletons)* "
     "are **no longer"),
    # C-V42: 395 rel32 fields carry 1,184 differing bytes.
    (U158, "| rel32 displacements shifted by exactly `0x7810` | ~1,186 | 395+ groups, all the same delta |",
     "| rel32 displacements shifted by exactly `0x7810` | ~~~1,186~~ 1,184 | 395+ groups, all the same delta " + C +
     "byte diff of the twins: 1,228 differing bytes, 1,184 of them in 395 rel32 fields, 44 single bytes)* |"),
    # C-V43a: 00244F50: 231 call + 16 jmp = 247 sites in 206 functions.
    (CEN, "`00244F50`, 203 callers, read in full:",
     "`00244F50`, ~~203 callers~~ 206 calling functions " + C + "231 `call` sites and 16 tail-`jmp` sites, 247 in "
     "all, rel32 sweep)*, read in full:"),
    # C-V43b: 340 certified slots in the battle action handler span.
    (CEN, "| 339 | Battle action handler table — `01EEC460`, 359 slots |",
     "| ~~339~~ 340 " + C + "re-derived as in §17: 340 relocated function-entry slots in `01EEC460`–`01EECD98`)* "
     "| Battle action handler table — `01EEC460`, 359 slots |"),
    (CEN, "| **2,281** | **inside an already-documented table (75.7 %)** | |",
     "| **~~2,281~~ 2,282** " + C + "1,740 + 340 + 202)* | **inside an already-documented table (75.7 %)** | |"),
    (CEN, "| 734 | outside every documented span (24.3 %) | |",
     "| ~~734~~ 733 " + C + "3,015 − 2,282)* | outside every documented span (24.3 %) | |"),
    # C-V43c: 2,350 type descriptors, 2,286 COLs, 2,286 vtables.
    (CEN, "The vtable figure comes from recovering **2,335 RTTI type descriptors → 2,271 complete-object\nlocators → "
          "2,271 vtables** and walking",
     "The vtable figure comes from recovering **~~2,335~~ 2,350 RTTI type descriptors → ~~2,271~~ 2,286 "
     "complete-object\nlocators → ~~2,271~~ 2,286 vtables** " + C + "RTTI recount: 2,350 `.?AV`/`.?AU` descriptors "
     "sharing one `type_info` vftable, 2,286 locators whose self-RVA checks, 2,286 `.rdata` qwords pointing at them — "
     "§3's 2,286; the slot totals above were walked from 2,271 and are not re-derived here)* and walking"),
    # C-V46: 001491CE / 001492FF are one nop each, then the v / h 32x32 predictors (001491D0, 00149300).
    (CUT, "| `001491CE`, `001492FF` | switch data after `repz ret` | read by the predecessor's dispatch |",
     "| `001491CE`, `001492FF` | ~~switch data after `repz ret`~~ one `nop` of padding after `repz ret`, then code " +
     C + "`001491CE`+0x2 begins the v 32x32 intra predictor and `001492FF`+0x1 the h 32x32 predictor, the libvpx bodies UC-3 "
     "names)* | ~~read by the predecessor's dispatch~~ no rel32 or pointer reference to either entry |"),
    # C-V47: continuation count 162 / 3,418 (member TSV).
    (UNL,"**163 of those blocks as continuations of the body before them, not\n> separate functions**",
     "**~~163~~ 162 of those blocks as continuations of the body before them, not\n> separate functions** " + C +
     "`unlisted-body-admissions.tsv` holds 162 continuation rows, 3,418 bytes, since the 2026-09-25 table split)*"),
    (UNL, "**163 blocks - 3,797 bytes - are not separate functions.** The clearest",
     "**~~163 blocks - 3,797 bytes~~ 162 blocks - 3,418 bytes - are not separate functions.** " + C + "the member "
     "TSV's continuation rows after the 2026-09-25 split)* The clearest"),
    # C-V48: the 1,471 are blocks; 874 are bodies (+3 ambiguous).
    (UNL, "and the function list is short by at least 1,471 bodies.**",
     "and the function list is short by ~~at least 1,471 bodies~~ 874 bodies and 3 ambiguous blocks** " + C +
     "`unlisted-body-admissions.tsv`: of 1,471 blocks, 431 are jump tables, 162 continuations and 1 covered)*."),
    (README, "**244,619 of them are\n  code in at least 1,471 blocks",
     "**244,619 of them are\n  code in ~~at least 1,471 blocks~~ 1,471 blocks** " + C + "874 bodies, 162 "
     "continuations, 3 ambiguous, 1 covered and 431 jump tables of data, `unlisted-body-admissions.tsv`)* **"),
    # C-V49: the matrix is 022D91B0..022D91EF (003970A0, 0039AF70).
    (BIG, "| `022D91A0`–`022D91E0` | **the 4×4 matrix**",
     "| ~~`022D91A0`–`022D91E0`~~ `022D91B0`–`022D91EF` " + C + "both accessors move four 16-byte rows at "
     "`022D91B0`, `022D91C0`, `022D91D0`, `022D91E0`)* | **the 4×4 matrix**"),
    # C-V50: the last cell 022D94A0 is a qword, so the file spans 1,432 bytes.
    (BIG, "combined footprint : 32 distinct addresses, 022D8F10..022D94A0 = 1,424 bytes\n",
     "combined footprint : 32 distinct addresses, 022D8F10..022D94A0 = 1,424 bytes   <- corrected 2026-10-02, "
     "OPUS: 1,424 is start-to-start; the last cell 022D94A0 is a qword (its users read it with qword compares), so the file "
     "spans 1,432 bytes, as section 16 says\n"),
    # C-V51: the payload is 48 bytes (003CCC20+0x5E..+0x73).
    (BIG, "- The 32-byte record payload remains opaque apart from its index byte.",
     "- ~~The 32-byte record payload remains opaque apart from its index byte.~~ " + C + "the payload is 48 bytes, "
     "three `movups` pairs at `003CCC20`+0x5E..+0x73, and its fields are read — see the SD-122 correction above)*"),
    (BIG, "movups [entry], [arg0] ; movups [entry+0x10], [arg0+0x10]   ; 32-byte payload\n",
     "movups [entry], [arg0] ; movups [entry+0x10], [arg0+0x10]   ; 32-byte payload   <- corrected 2026-10-02, "
     "OPUS: three movups pairs, 48 bytes (003CCC20+0x5E..+0x73)\n"),
    (BIG, "+0x00..0x1F  32-byte payload              +0x00  byte   refcount\n",
     "+0x00..0x1F  32-byte payload              +0x00  byte   refcount   <- corrected 2026-10-02, OPUS: "
     "+0x00..0x2F, 48 bytes (003CCC20+0x5E..+0x73)\n"),
    # C-V52: tag 2 is written (0036E540+0x46) and tag 3 tested (0036E5E0+0x20).
    (BIG, "manager; …; flags at +0x10}`**, 24 bytes × 32. The two resolved",
     "manager; …; flags at +0x10}`**, 24 bytes × 32 " + C + "the tag list is incomplete: the tag also takes 2, "
     "written by `0036E540`+0x46 when it is 1 and the load state is 2 or 3, and 3 is tested by `0036E5E0`+0x20)*. "
     "The two resolved"),
    # C-V53: 003CD840 three times and 0036B130 four times per dispatcher.
    (BIG, "00181DD0     21 B      0036B130     41 B (x3)    003CD840  21,276 B (x2)\n",
     "00181DD0     21 B      0036B130     41 B (x3)    003CD840  21,276 B (x2)   <- corrected 2026-10-02, OPUS: "
     "0036B130 x4 and 003CD840 x3 (rel32 sites 003CCF20+0x82/+0x248/+0x2D7/+0x32D and +0x9E/+0x25F/+0x2EE)\n"),
    (BIG, "The dispatcher calls `003CD840` twice among ten\n> callees,",
     "The dispatcher calls `003CD840` ~~twice among ten~~ three times among twelve\n> callees " + C + "rel32 "
     "sites at `003CCF20`+0x9E, +0x25F and +0x2EE; §16 and §20)*,"),
    (BIG, "**A typed slot table.** Six accessors clamp the index to `0x1F` — **32 slots** — read the payload at",
     "**A typed slot table.** ~~Six accessors~~ At least nine family members clamp the index to `0x1F` " + C +
     "`mov eax, 0x1F` / `cmovg` in the seven `0x1F` rows of the table above and also in `0036DDC0` (+0xE) and "
     "`0036E320` (+0x14))* — **32 slots** — read the payload at"),
    # C-V54a: 28,028 / 139 are GN160's cells (the GN158 file has 158).
    (BIG, "*(GN158 figures; at GN161 the cells are 28,137 / 9,409 / 585 / 30",
     "*(~~GN158 figures~~ GN160 figures " + C + "`verify_GFZ_GN160/residual_addrs.txt` has 139 rows and the GN158 "
     "file 158; 28,028 + 9,409 + 585 + 139 = 38,161)*; at GN161 the cells are 28,137 / 9,409 / 585 / 30"),
    (BIG, "R109's additive GN161 batch removed 128 functions from the untagged set\n> (the residual cell dropped "
          "139→30; `codeDomain` rose 28,009→28,137).",
     "~~R109's additive GN161 batch removed 128 functions~~ GN159 to GN161 removed 128 functions, R109 109 of "
     "them, from the untagged set\n> (the residual cell dropped ~~139→30~~ 158→30; `codeDomain` rose 28,009→28,137) "
     + C + "`residual-109-classification.tsv` has 109 rows; 158 − 30 = 128 = 28,137 − 28,009)*."),
    # C-V54b: front matter size.
    (BIG, "system: The largest unclassified functions — 2.67 MB the GFZ owns but does not classify\n",
     "system: The largest unclassified functions — 2.67 MB the GFZ owns but does not classify   # <- corrected "
     "2026-10-02, OPUS: 2.67 MB is the GN158 figure 2,666,058 B; GN161 is 2,524,402 B and functions.tsv now 2,485,924 B\n"),
    # C-V55: 0041E000 and 0041E1D0 call through the 01EFFAF0 command table (+0x117, +0xED); it is no vtable.
    (CEN, "`0041E000` (461 B) is a call-free unowned body -",
     "`0041E000` (461 B) is a ~~call-free~~ unowned body " + C + "it calls `qword [r9 + r13]` through the "
     "`01EFFAF0` table at `0041E000`+0x117)* -"),
    (CEN, "`0041E1D0` (348 B) is a call-free record walker -",
     "`0041E1D0` (348 B) is a ~~call-free~~ record walker " + C + "it calls through the `01EFFAF0` table at "
     "`0041E1D0`+0xED)* -"),
    (CEN, "`0x80220040` flag, `01EFFAF0` vtable. Interior anchor",
     "`0x80220040` flag, `01EFFAF0` ~~vtable~~ command table " + C + "16-byte `{handler, 0}` records with no "
     "complete-object locator before them — §19's 128-record table)*. Interior anchor"),
    # C-V56: 121 of the 135 call-referenced blocks are called only from unlisted code.
    (REF, "**129 of the 135 are called only from other unlisted code.** The remaining",
     "**~~129~~ 121 of the 135 are called only from other unlisted code.** " + C + "135 − 14 = 121, rel32 "
     "sweep against the listed extents; 129 is 143 − 14 and counts the six relocated, the one `lea` and the one "
     "`.pdata` block)* The remaining"),
    # C-V58: sixteen distinct callees; AC-9's sites are 002A9F00's.
    (CBC, "The decompilation contains **fifteen\ndistinct calls** —",
     "The decompilation contains **~~fifteen~~ sixteen\ndistinct calls** " + C + "the sixteen listed, `00808C40` "
     "included; the image body has the same sixteen)* —"),
    (CBC, "**0 reported, 15 present**, in the function",
     "**0 reported, ~~15~~ 16 present** " + C + "sixteen distinct callees)*, in the function"),
    (CBC, "`[0209CC6C]` added before each glyph (`002AA0D2`) and `[0209CC68]` after (`002AA734`); the glyph",
     "`[0209CC6C]` added before each glyph (~~`002AA0D2`~~ `002AAE40`+0x1BE) and `[0209CC68]` after "
     "(~~`002AA734`~~ `002AAE40`+0x82A) " + C + "the two cited sites are `002A9F00`'s, +0x1D2 and +0x834; this "
     "loop's own reads are at the offsets given)*; the glyph"),
    # C-V59: +0x70 holds 22 05 93 19 ...
    (GQ, "+0x30   0  0  1  0        +0x70   0  0  0  0     <- referenced by nothing\n",
     "+0x30   0  0  1  0        +0x70   0  0  0  0     <- referenced by nothing   <- corrected 2026-10-02, OPUS: "
     "+0x70 (008C5FF0) holds 22 05 93 19 01 00 00 00 40 45 C3 01, not zeros; the pool ends at +0x70\n"),
    # C-V60: seven slots filled by five bodies.
    (DISP, "Of twelve slots, five are filled by\nfour distinct bodies.",
     "Of twelve slots, ~~five are filled by~~\n~~four distinct bodies.~~ seven are filled by five distinct bodies " +
     C + "the table at `009164C0` read as qwords: `002A9980` ×2, `002A8C50` ×2, `002A9F00`, `002AA800`, "
     "`002AAE40`)*."),
    # C-V61: 002DA7C0 writes thirteen 16-byte words.
    (WTREE, "It writes twelve 16-byte words into a cursor at",
     "It writes ~~twelve~~ thirteen 16-byte words " + C + "thirteen `add [r10+0x10], 0x10` steps, "
     "`002DA7C0`+0x8E..+0x1F0: the descriptor, then three per corner)* into a cursor at"),
    # C-V62: 002DD4B0 has 10 sites in 10 functions including 00392A10, so 9 others.
    (DBX, "| `002DD4B0` | — | 7 B | Static global getter selecting the two paths, 10 other callers — not dead |",
     "| `002DD4B0` | — | 7 B | Static global getter selecting the two paths, ~~10 other callers~~ 9 other "
     "callers " + C + "10 rel32 sites in 10 functions, `00392A10`+0xD4 among them)* — not dead |"),
    (DBX, "`002DD4B0` is a 7-byte static global getter with ten callers elsewhere, so it is",
     "`002DD4B0` is a 7-byte static global getter with ~~ten callers elsewhere~~ nine callers elsewhere " + C +
     "ten functions call it, `00392A10` included)*, so it is"),
    (DBX, "   +-> 002DD4B0     7 B   a static global getter     (10 other callers - not dead)\n",
     "   +-> 002DD4B0     7 B   a static global getter     (10 other callers - not dead)   <- corrected 2026-10-02, "
     "OPUS: 9 other callers (10 functions with 00392A10)\n"),
    # C-V63: 0017F8E0 fetches the singleton twice (+0x8, +0x19).
    (API, "`0017F8E0` — 50 B, 4 callers: the glyph-width query — `001B5FA0()` context,",
     "`0017F8E0` — 50 B, 4 callers: the glyph-width query — `001B5FA0()` context " + C + "fetched twice, at "
     "`0017F8E0`+0x8 and +0x19, once before each callee — §5's reading)*,"),
    # C-V64: the jump table at 002AC1B4 has eight entries; mode 6 and anything above 7 go to the epilogue.
    (U158, "labels **0, 1, 2, 3, 4, 5, 7** (seven, no `default`)",
     "labels **0, 1, 2, 3, 4, 5, 7** (~~seven, no `default`~~ eight table entries, mode 6 and any value above 7 "
     "going to the epilogue " + C + "`cmp eax, 7` / `ja` at `002ABF70`+0x15 and the eight table dwords its +0x22 load indexes, "
     "entry 6 = `002ABF70`+0x23B)*)"),
    # C-V65: 158 - 4 = 154; R109 classified 109.
    (GQ, "Four of them are now found. The other 153 are not,",
     "Four of them are now found. The other ~~153~~ 154 " + C + "158 − 4)* are not,"),
    (GQ, "**30** — R109 classified 128, so",
     "**30** — R109 classified ~~128~~ 109, and GN159 to GN161 128 in all " + C + "`residual-109-classification.tsv` "
     "has 109 rows; 158 − 30 = 128)*, so"),
    # C-V66: 23 functions reference 01DFE40C.
    (CS, "It is written here but read by 24 functions across",
     "It is written here but ~~read by 24 functions~~ referenced by 23 functions " + C + "16 read it only, 7 write "
     "it, 2 of those also read — §2's correction)* across"),
    # C-V67: the shipped VBF holds 337 sidecars; 674 counts each twice.
    (CS, "`jsondata/CutScenes/` and `jsondata/cutscenes/` hold **674** files. **620 parse**,\n        **52 are zero "
         "bytes**, and 2 more have syntax errors. Together they carry **7,560 sections**.",
     "`jsondata/CutScenes/` and `jsondata/cutscenes/` hold **~~674~~ 337** files. **~~620~~ 310 parse**,\n        "
     "**~~52~~ 26 are zero bytes**, and ~~2~~ 1 more ~~have~~ has syntax errors. Together they carry **~~7,560~~ "
     "3,780 sections** " + C + "the shipped VBF has one `jsondata/cutscenes/` directory of 337 files; the two "
     "spellings are the same files counted twice, so every figure here halves — UQ-249's 337 and 26)*."),
    (CS, "Section sizes cluster hard: **9 keys** in 5,148 sections and\n        **4 keys** in 1,360, with a rich "
         "**80-key** variant in 530.",
     "Section sizes cluster hard: **9 keys** in ~~5,148~~ 2,574 sections and\n        **4 keys** in ~~1,360~~ 680, "
     "with a rich **80-key** variant in ~~530~~ 265 " + C + "same shipped-VBF recount)*."),
    (CS, "**Four keys appear in every one of the 7,560 sections**",
     "**Four keys appear in every one of the ~~7,560~~ 3,780 sections** " + C + "same recount)*"),

    # ---------------- 3.2 stale / unstruck / banner ----------------
    # C-S1: README entries say PARTIAL; the pages' front matter says DOCUMENTED.
    (README, "  **PARTIAL, tier 1.** The sharper half of the same defect:",
     "  **PARTIAL, tier 1.** " + A + "the page's front matter, now `status: DOCUMENTED`" + T + " The sharper half of "
     "the same defect:"),
    (README, "  **PARTIAL, tier 1.** A **third residual,",
     "  **PARTIAL, tier 1.** " + A + "the page's front matter, now `status: DOCUMENTED`" + T + " A **third residual,"),
    (README, "  **PARTIAL, tier 1.** A **second, larger residual**:",
     "  **PARTIAL, tier 1.** " + A + "the page's front matter, now `status: DOCUMENTED`; its three largest are "
     "identified there" + T + " A **second, larger residual**:"),
    # C-S2: 158 of 158 have admissible evidence (00392A00+0x5 jne 00392A10).
    (README, "| **at least one admissible reference** | ~~156~~ **157** |",
     "| **at least one admissible reference** | ~~156~~ **~~157~~ 158** " + A + "the-unresolved-158.md, \"The count "
     "is now 158 of 158\" — " + REACH_ROLE + T + " |"),
    (README, "| **no admissible reference of any kind** | ~~2~~ **1** |",
     "| **no admissible reference of any kind** | ~~2~~ **~~1~~ 0** " + A + "the box-renderer page's REFUTED box" + T +
     " |"),
    (README, "~~**156 of 158**~~ **157 of 158 have admissible incoming evidence.**",
     "~~**156 of 158**~~ **~~157 of 158~~ 158 of 158 have admissible incoming evidence.** " + A + "the-unresolved-158.md, "
     "UPDATED 2026-09-16" + T),
    # C-S3: a 158 member references an authored string (0020AC30+0xFA lea of "sum_").
    (README, "| Direct authored strings | **0** |",
     "| Direct authored strings | **0** " + A + "the glyph-quads page, \"Superseded reading\" — the zero was the "
     "scanner's; `0020AC30`, one of the 158, loads `\"sum_\"` at `0020AC30`+0xFA" + T + " |"),
    # C-S4: body banners PARTIAL vs front matter AUDITED.
    (CTX, "**PARTIAL.** The lifecycle, the size, the single initialiser",
     "**PARTIAL.** " + A + "the front matter, now `status: AUDITED` with every register row closed" + T + " The "
     "lifecycle, the size, the single initialiser"),
    (DISP, "**PARTIAL.** The dispatch architecture, the selector,",
     "**PARTIAL.** " + A + "the front matter, now `status: AUDITED`" + T + " The dispatch architecture, the "
     "selector,"),
    # C-S5: BIG banner vs identifications.
    (BIG, "**`PARTIAL` deliberately.** The three largest are characterised and placed in their call chains.\n**None of "
          "the three is identified.**",
     "**`PARTIAL` deliberately.** The three largest are characterised and placed in their call chains.\n**~~None of "
     "the three is identified.~~** " + A + "the front matter, now `status: DOCUMENTED`, and the identifications in "
     "§16 to §20 — the render-model binding machine and the effect mesh draw" + T),
    # C-S6: DB's unstruck "never invoked" lines.
    (DBX, "**It is never invoked.** Nothing in the shipping executable calls it,",
     "**~~It is never invoked.~~** " + A + "the REFUTED box at the top — " + REACH + T + " ~~Nothing in the shipping "
     "executable calls it,~~"),
    (DBX, "00392A10   707 B   nine-patch box renderer          <- NOTHING reaches this\n",
     "00392A10   707 B   nine-patch box renderer          <- NOTHING reaches this   <- corrected 2026-10-02, OPUS: "
     "reached by jne from 00392A00+0x5, whose four callers are live (REFUTED box)\n"),
    (DBX, "**Upstream: none.** Established in §8 by four independent routes.",
     "**~~Upstream: none.~~** " + A + "the REFUTED box — " + REACH + T + " ~~Established in §8 by four independent "
     "routes.~~"),
    (DBX, "- **Do not patch this expecting a visual change.** It is unreachable; edits have no effect.",
     "- **~~Do not patch this expecting a visual change.~~** ~~It is unreachable; edits have no effect.~~ " + A +
     "the REFUTED box — it is reachable through `00392A00`" + T),
    (DBX, "system: The nine-patch box renderer that is never called\n",
     "system: The nine-patch box renderer that is never called   # <- corrected 2026-10-02, OPUS: it is reached "
     "through 00392A00+0x5 (REFUTED box)\n"),
    # C-S7: CS / U158 repeat the refuted no-caller reading.
    (CS, "Static; and the renderer itself still has no caller.",
     "Static; ~~and the renderer itself still has no caller.~~ " + A + "the box-renderer page's REFUTED box — " +
     REACH_ROLE + T),
    (CS, "  — the other function from the same pair, and genuinely dead.",
     "  — the other function from the same pair, ~~and genuinely dead~~ " + A + "the box-renderer page's REFUTED "
     "box: it is reachable" + T + "."),
    (U158, "**`00392A10` is one of the fifteen no-caller residuals** and its own",
     "**~~`00392A10` is one of the fifteen no-caller residuals~~** " + A + "§\"What would settle the cluster\", "
     "UPDATED 2026-09-16: " + REACH + T + " and its own"),
    # C-S8: 1 of 158 without evidence is now 0.
    (CS, "**The corrected figure is 144 of 158 with a direct caller, and 1 of 158 with\nno admissible reference of any "
         "kind.**",
     "**The corrected figure is 144 of 158 with a direct caller, and ~~1 of 158~~ 0 of 158 with\nno admissible "
     "reference of any kind.** " + A + "the-unresolved-158.md, \"158 of 158\" — " + REACH_ROLE + T),
    (DBX, "The corrected figure is **1 of 158, not 2**, and `00392A10` is that one:",
     "The corrected figure is **~~1 of 158, not 2~~ 0 of 158** " + A + "the REFUTED box above" + T + ", and "
     "~~`00392A10` is that one:~~"),
    # C-S9: the re-census has been run.
    (CEN, "One was found by intersecting with relocations; the full re-census has not been run.",
     "One was found by intersecting with relocations; ~~the full re-census has not been run.~~ " + A + "the "
     "category README, \"The re-census has now been run\", and the-unresolved-158.md, 158 of 158" + T),
    # C-S10: the 96 % figure is qualified.
    (U158, "finding that 96 % of their incoming references are banned exception metadata.",
     "finding that 96 % of their incoming references are banned exception metadata " + A + "the category README, "
     "QUALIFIED 2026-09-02: the figure describes the reference dump, not the image" + T + "."),
    # C-S11: fifteen no-caller re-measured as thirteen.
    (U158, "and **15\nfunctions have no caller at all**, which is itself",
     "and **~~15~~\n~~functions have no caller at all~~** " + A + "§7, NARROWED 2026-09-16: thirteen of the 139 have "
     "no incoming edge, and edges are not reach" + T + ", which is itself"),
    # C-S12: every member now has a reading.
    (U158, "**Eight of 158 have been read** (section 9). The other 150 have not.",
     "**~~Eight of 158 have been read~~** ~~(section 9). The other 150 have not.~~ " + A + "§7: \"Every member now has "
     "a reading\"" + T),
    # C-S14: _RDATA carries no relocations, so no slots.
    (CEN, "pointer slots found in data:   29,000 in .rdata,  3,015 in .data,  8 in _RDATA\n",
     "pointer slots found in data:   29,000 in .rdata,  3,015 in .data,  8 in _RDATA   <- answered 2026-10-02, OPUS: "
     "_RDATA has no base relocation, so 0 slots (\"The _RDATA 8 were never real\")\n"),
    (CEN, "| `_RDATA` holds 8 slots | independent scan | **exact** |",
     "| ~~`_RDATA` holds 8 slots~~ " + A + "§15, \"The `_RDATA` 8 were never real\"; `_RDATA` carries no base "
     "relocation" + T + " | independent scan | **exact** |"),
    # C-S15: ex strings go to this page's 003649A0 (002D8690+0xAC); the others go elsewhere.
    (GQ, "handed to a completely different drawing path. Which strings those are is not established here.",
     "handed to ~~a completely different drawing path~~ this page's glyph-run path, and the others to `002B0280` " +
     C + "`002D8690`+0x90 tests the prefix and an `ex` string goes to `003649A0` at +0xAC)*. ~~Which strings those "
     "are is not established here.~~ " + A + "§7, ANSWERED 2026-09-25: an `ex` string is `ex00` and UTF-16LE text" + T),
    (GQ, "     002D8690 / 002D87D0   pick a renderer: strings tagged \"ex\" go elsewhere\n",
     "     002D8690 / 002D87D0   pick a renderer: strings tagged \"ex\" go elsewhere   <- corrected 2026-10-02, OPUS: "
     "inverted - ex strings come here (002D8690+0xAC calls 003649A0); the others go to 002B0280\n"),
    # C-S16: the 001ED130 operand is story progress.
    (CS, "names: `edx = movsx(00265270())` is the field id, `ecx` the",
     "names: `edx = movsx(00265270())` is the ~~field id~~ story-progress value " + A + "§\"The two values in "
     "`001ED130` are story progress\" and UQ-337" + T + ", `ecx` the"),
    # C-S17: {i} has no reader.
    (GQ, "| `{i}` | — | 3 bytes | an inline icon |",
     "| `{i}` | — | 3 bytes | an inline icon " + A + "§7: the three bytes have no reader in this build" + T + " |"),
    # C-S18: there is no callback; the call is the empty 0016D6A0 (003649A0+0x5D8).
    (GQ, "projectCallback(&packed[4], &TL);      // -> four packed screen positions\n",
     "projectCallback(&packed[4], &TL);      // -> four packed screen positions   <- answered 2026-10-02, OPUS: no "
     "callback - a direct call of the empty 0016D6A0 (ret 0) at 003649A0+0x5D8 (UQ-365)\n"),
    # C-S19: the pool reading is overturned.
    (GQ, "| **a pool of six ± axis vectors, not a matrix object.** Four of them",
     "| **a pool of six ± axis vectors, not a matrix object.** " + A + "§10, \"Both readings are over-reads\": "
     "`+0x60` is no axis vector and `+0x70` is past the pool" + T + " Four of them"),
    # C-S20 + C-V25: 002AC5F0 is classified and called by name.
    (PAINT, "`002AC5F0` (7,489 B — still residual,\nthe largest unclassified function in the game)",
     "`002AC5F0` (7,489 B — ~~still residual,~~\n~~the largest unclassified function in the game~~ classified at "
     "GN162 as `UI.Text.ControlCodeInterpreter` " + A + "the dispatch-table page §1" + T + ")"),
    (DISP, "> The largest unclassified function in the game is not called by name from anywhere. It is reached",
     "> ~~The largest unclassified function in the game is not called by name from anywhere.~~ " + C + "`002AC5F0` "
     "is classified at GN162 (§1) and has seven direct callers; it is the column-1 and column-2 handlers, not it, "
     "that are reached through the table)* It is reached"),
    # C-S21: the suspend-flag and seeded-once readings are corrected below.
    (PAINT, "takes the *flush-and-forget* path of §5 and the suspend flag is off.",
     "takes the *flush-and-forget* path of §5 ~~and the suspend flag is off~~ " + A + "\"CORRECTED — `+0x2379` is "
     "not a suspend flag\" below" + T + "."),
    (PAINT, "the values are seeded once at construction and thereafter only\never carry a run's own alphas.",
     "~~the values are seeded once at construction and thereafter only~~\n~~ever carry a run's own alphas.~~ " + A +
     "the begin re-seeds them each frame, and the falsification row \"An earlier version of this row\"" + T),
    # C-S22: the score has moved.
    (PAINT, "score therefore still reads 154 unresolved**; that is a staging state,",
     "score therefore still reads 154 unresolved** " + A + "the correction above, 158 → 139, and the-unresolved-158.md: "
     "30 at GN161" + T + "; that is a staging state,"),
    # C-S23: RT's not-read lines.
    (RT, "| `001B5FB0`, `001B51C0`, `001FDD60` | resource acquisition | — | **not read** |",
     "| `001B5FB0`, `001B51C0`, `001FDD60` | resource acquisition | — | **not read** " + A + "UQ-359 in §8: all "
     "read" + T + " |"),
    (RT, "| `006B5C70`, `005C5310` | buffer rebuild | — | **not read** |",
     "| `006B5C70`, `005C5310` | buffer rebuild | — | **not read** " + A + "UQ-359 in §8: plain field getters" + T +
     " |"),
    (RT, "primary resource, from `001B51C0`; **null means the whole call failed** |",
     "primary resource, from `001B51C0`; **~~null means the whole call failed~~** " + A + "§8: \"This falsifies "
     "§4.1's null means the whole call failed\"" + T + " |"),
    (RT, "were\n**not read at all**; and the `0x1E` bound",
     "were\n**~~not read at all~~** " + A + "UQ-359 in §8" + T + "; and the `0x1E` bound"),
    # C-S25: the 2x scale label is the FrameLimit time base.
    (DISP, "001EDEC0  cmp dword ptr [01F82E38], 0   ; scale mode active?\n",
     "001EDEC0  cmp dword ptr [01F82E38], 0   ; scale mode active?   <- answered 2026-10-02, OPUS: the FrameLimit "
     "time base, not a scale mode (name corrected 2026-09-21 above)\n"),
    (DISP, "So the predicate says: **\"1 unless the 2x scale mode is on, unsuppressed,",
     "So the predicate says: **\"1 unless the ~~2x scale mode~~ 60 fps time base is on " + A + "\"Name corrected "
     "2026-09-21\" above" + T + ", unsuppressed,"),
    # C-S26: the null test is in the listing now.
    (DISP, "As printed, `002ABF20` runs `mov rax, [rax + r8*8]` straight into `jmp rax` — no null test.",
     "As printed, `002ABF20` runs `mov rax, [rax + r8*8]` straight into `jmp rax` — no null test " + A + "§4's "
     "listing, which now carries the `test rax, rax` / `je` pair" + T + "."),
    # C-S27: CBC §7 open items answered elsewhere.
    (CBC, "What `002AC2F0` decodes. What",
     "~~What `002AC2F0` decodes.~~ " + A + "the glyph-quads page §7: `002AC2F0` resolves the object bytes to glyph "
     "indices, and `+0x1102` is the line-start flag (UQ-370)" + T + " What"),
    (CBC, "Why the counter at `+0x10D4` triggers\n`002B4730(1)` every twenty characters.",
     "~~Why the counter at `+0x10D4` triggers~~\n~~`002B4730(1)` every twenty characters.~~ " + A + "the flush note "
     "below and the glyph-quads page's emit row: the queue is flushed at `0x14` items" + T),
    # C-S28: falsification pass 1 exists.
    (GQ, "**Still owed: a first falsification pass, by a session that did not write this.** One",
     "**~~Still owed: a first falsification pass, by a session that did not write this.~~** " + A + "\"Falsification "
     "pass 1 — 2026-09-03\" below; front matter `falsification_passes: 1`" + T + " One"),
    # C-S29: word 9 is the register list (XYZF2), decoded from the GIF tag 0x1022400000008004.
    (RECT, "| 9 | `4` — the vertex count |",
     "| 9 | `4` — ~~the vertex count~~ the register list, XYZF2 " + C + "word 8 is a GIF tag with NLOOP 4 and NREG "
     "1, so word 9 is its REGS descriptor, register 4; the vertex count is the tag's NLOOP)* |"),
    (RECT, "— `local_1a0[9] = 4` in the first,",
     "— `local_1a0[9] = 4` in the first " + A + "the 2026-09-18 read: that `4` is the register list XYZF2, and the "
     "four comes from the tag's NLOOP" + T + ","),
    # C-S30: no dropped indirect call.
    (RECT, "The target of the indirect call in §5. What `00202B70` computes",
     "~~The target of the indirect call in §5.~~ " + A + "\"CORRECTED 2026-09-18 (FABLE): there is no dropped "
     "indirect call\"" + T + " What `00202B70` computes"),
    # C-S31: the counter counts 60 Hz ticks.
    (BLINK, "**`DAT_0208F570` is a frame counter and the argument advances",
     "**`DAT_0208F570` is a ~~frame counter~~ 60 Hz tick counter** " + A + "the falsification row: it counts 60 Hz "
     "ticks whatever the present interval" + T + " **and the argument advances"),
    # C-S33: the lea at 002B6427 is a code reference.
    (BLINK, "and the three references it has are all `DATA`. |",
     "and the three references it has are ~~all `DATA`~~ not all data " + A + "§3: `lea r8` at `002B6350`+0xD7 takes "
     "`002B7B80`'s address in code" + T + ". |"),
    # C-S34: BLINK open list partly answered.
    (BLINK, "What `002D8530`, `002DBDD0`, `00403970`, `00403BC0`, `00404120` and `00404730` do.",
     "What `002D8530`, `002DBDD0`, `00403970`, `00403BC0`, `00404120` and `00404730` do " + A + "`002DBDD0` and "
     "`00403970` on the rectangle page, `002D8530`, `00403BC0` and `00404120` on the second-icon page; `00404730` "
     "stays open" + T + "."),
    # C-S35: the crossref TSV now has the 30.
    (U158, "backlog. They are listed in the TSV with an empty `pages` column.",
     "backlog. ~~They are listed in the TSV with an empty `pages` column.~~ " + A + "the member TSV now holds the 30 "
     "of GN161, each `interior_cited=yes` and none with an empty `pages` column" + T),
    # C-S36: 002DD4B0 returns [0215E6D0].
    (NINEP, "What `002DD4B0` tests, and therefore which of the two paths actually runs. What",
     "~~What `002DD4B0` tests, and therefore which of the two paths actually runs.~~ " + A + "`002DD4B0` is `mov eax, "
     "[0215E6D0]; ret`, the widget-tree page's reading, and the box-renderer page's UQ-352" + T + " What"),
    (NINEP, "runtime by a predicate this document does not resolve.",
     "runtime by a predicate ~~this document does not resolve~~ " + A + "§9's note: `002DD4B0` returns the word "
     "`0215E6D0`" + T + "."),
    # C-S37: 001AED50 is read below.
    (NINEP, "**NOT CLAIMED: what it does** —",
     "**~~NOT CLAIMED: what it does~~** " + A + "SWE2-EC7-53 below: a `0x30`-stride vector erase/move helper" + T +
     " —"),
    # C-S38: 002DD2F0 translates and clips; the markers are answered.
    (ICON2, "**What it draws is not established** — only that it receives a",
     "**~~What it draws is not established~~** " + A + "SWE2-EC7-18 below and the rectangle page: `002DD2F0` "
     "translates a child rectangle by its parent's origin and clips, it draws nothing; the blinking-icon page "
     "answers what the drawer shows, the track map's markers" + T + " — only that it receives a"),
    (ICON2, "What `002DD2F0` draws. What `01E0CE80` is set from.",
     "~~What `002DD2F0` draws.~~ " + A + "the note above" + T + " What `01E0CE80` is set from."),
    # C-S39: WBG unknowns answered on the widget-tree page and on this page.
    (WBG, "What `002DAC70`, `002DAF30`, `002DD4B0` and `002DD7B0` do — `002DD7B0` is",
     "~~What `002DAC70`, `002DAF30`, `002DD4B0` and `002DD7B0` do~~ " + A + "the widget-tree page's 2026-09-18 note: "
     "`002DD4B0` returns `0215E6D0`, `002DD7B0` is the `fontcolor` shadow-byte getter; `002DAF30` is read below" +
     T + " — `002DD7B0` is"),
    # C-S40: mode 3 also steps.
    (MEAS, "| `+0x88` | a **countdown**; states 3 and 7 decrement it and act at zero |",
     "| `+0x88` | a **countdown**; states 3 and 7 decrement it and act at zero " + A + "§7, corrected 2026-09-30: "
     "state 3 also steps the target by `+0xA0` on every tick while it is non-zero" + T + " |"),
    # C-S41: modes read; all 13 have a reading.
    (MEAS, "What states `0`, `1`, `4`, `5` and `7` of §5 distinguish~~, or what~~",
     "~~What states `0`, `1`, `4`, `5` and `7` of §5 distinguish~~ " + A + "the reveal-stepper row below" + T +
     "~~, or what~~"),
    (MEAS, "| unread | `002A4830`, `002AE610`, `002AF960`, `002A4430`, `00573BE0`, `002B5390`, `002B2DF0` |",
     "| unread | `002A4830`, `002AE610`, `002AF960`, `002A4430`, `00573BE0`, `002B5390`, `002B2DF0` " + A + "the row "
     "above: all 13 have a reading since 2026-09-18, UQ-383" + T + " |"),
    # C-S42: the third call needs bit 24 too (00245E60+0x533) as well as bit 12 (+0x53B).
    (WTREE, "**The third call is gated on flag bit 12** and the first two on bit 24 matching a global",
     "**The third call is gated on flag bit 12** and ~~the first two~~ like the first two " + C + "the bit-24 "
     "compare against `0208F564` precedes it at `00245E60`+0x533 and the bit-12 test is +0x53B)* on bit 24 "
     "matching a global"),
    # C-S43: CS not-read lines answered later on the page.
    (CS, "are located in the dispatch table and none of their bodies was read. **PROPOSED-repos9e-23.**",
     "are located in the dispatch table and ~~none of their bodies was read~~ " + A + "§12: all twenty-three handler "
     "bodies are read" + T + ". **PROPOSED-repos9e-23.**"),
    (CS, "  Naming it would say what cancels every scripted wait — likely the highest-value single lookup left\n  in "
         "this thread. **PROPOSED-repos9e-24.**",
     "  Naming it would say what cancels every scripted wait — likely the highest-value single lookup left\n  in "
     "this thread " + A + "§13, which names `FUN_00267310`" + T + ". **PROPOSED-repos9e-24.**"),
    (CS, "`00360A50`, `00360880`, `003603F0` — none of which was read. **PROPOSED-repos9e-25.**",
     "`00360A50`, `00360880`, `003603F0` — ~~none of which was read~~ " + A + "§7, ANSWERED 2026-09-15: bit *k* is "
     "the manager's skip request *k*" + T + ". **PROPOSED-repos9e-25.**"),
    (CS, "  was not read. Do not assume the flags cause anything on their own.",
     "  ~~was not read.~~ " + A + "§10 and UQ-336: all four consumers are read" + T + " Do not assume the flags "
     "cause anything on their own."),
    (CS, "  opaque predicates. Naming what they test would sharpen the gate considerably and none was read.",
     "  opaque predicates. Naming what they test would sharpen the gate considerably and ~~none was read~~ " + A +
     "§7, \"The predicates in the gate\", ANSWERED 2026-09-03: all five read" + T + "."),
    # C-S44 / C-S45 / C-S46 / C-S47.
    (CS, "A wider family of about fifteen functions in `001C…` and `001EC…` references the same three strings,",
     "A wider family of ~~about fifteen~~ twelve functions " + A + "§7, ANSWERED 2026-09-26: twelve, each with a "
     "role" + T + " in `001C…` and `001EC…` references the same three strings,"),
    (CS, "**What the prefixes denote\nis not established here** —",
     "**~~What the prefixes denote~~\n~~is not established here~~** " + A + "§7: `sum_` is the summon scenes and "
     "`spc_` the special-attack event" + T + " —"),
    (CS, "      - **Still open, and it is what the row now asks:** what the 64-bit value selects.",
     "      - **~~Still open, and it is what the row now asks:~~** ~~what the 64-bit value selects.~~ " + A + "the "
     "ANSWERED 2026-09-18 line above: a VIF1 UNPACK header" + T),
    (CS, "`0024AF50` (368 B) is a cutscene-slot body - `0024B150`/`003A2090`/`003A21A0`.",
     "`0024AF50` (368 B) is a ~~cutscene-slot body~~ transfer-queue body " + A + "the correction above: its caller "
     "`0024A710` is the UI atlas registry's layout pass, not cutscene code" + T + " - `0024B150`/`003A2090`/"
     "`003A21A0`."),
    # C-S49: the extensions are applied.
    (CUT, "controls. The 159 extensions not yet applied are prepared as",
     "controls. The 159 extensions ~~not yet applied~~ " + A + "\"The 159 extensions applied (OPUS, 2026-09-29)\" and "
     "\"Resolved 2026-09-30\" below" + T + " are prepared as"),
    # C-S50: UNL stale lines.
    (UNL, "larger bands\n      stay NOT YET.",
     "larger bands\n      ~~stay NOT YET~~ " + A + "UC-1: every size band is now adjudicated" + T + "."),
    (UNL, "the library's banner at `01CEB6A5`; no block matched to a named routine |",
     "the library's banner at `01CEB6A5`; ~~no block matched to a named routine~~ " + A + "UC-3, narrowed "
     "2026-09-27: the intra predictors are matched byte for byte" + T + " |"),
    # C-S51: the denominator moved.
    (UNL, "**The denominator is NOT changed by this document.** Changing it",
     "**The denominator is NOT changed by this document.** " + A + "the applied populations 34,965, 35,064 and "
     "35,065 recorded later on this page" + T + " Changing it"),
    (UNL, "The denominator stays at 34,270 until this package is reviewed and applied.",
     "The denominator stays at 34,270 until this package is reviewed and applied " + A + "the applied UC-1 bands "
     "later on this page" + T + "."),
    # C-S52: operation bodies and kind 0x52 are read.
    (BIG, "- **No operation body was read.** BI-1's semantic core is untouched.",
     "- **~~No operation body was read.~~** ~~BI-1's semantic core is untouched.~~ " + A + "SD-120, answered "
     "2026-10-01: the eight `0050xxxx` operations are palette animation effects" + T),
    (BIG, "**not one of the eight bodies has been read** to say what it does.",
     "**~~not one of the eight bodies has been read~~** " + A + "SD-120 in §20" + T + " to say what it does."),
    (BIG, "Its meaning is not read here (`SD-123`).",
     "~~Its meaning is not read here~~ " + A + "§7, SD-123 answered 2026-09-30" + T + " (`SD-123`)."),
    # C-S55: the circular pointer.
    (GQ, "the population is carried by 99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md. "
         "See the register row.*\n",
     "the population is carried by 99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md. "
     "See the register row.* " + A + "this pointer names this page; the residual population is carried by "
     "the-unresolved-158.md and its member TSVs" + T + "\n"),
    # C-S56: three of the four.
    (GQ, "> **Corrected 2026-09-14 (OPUS): two of the four are no longer residual.** The certified parent",
     "> **Corrected 2026-09-14 (OPUS): ~~two~~ three of the four are no longer residual** " + A + "the paragraph "
     "above and the end of this note: `002AF960` followed at GN161" + T + ". The certified parent"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel)
        if t is None:
            t = open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if old in new or old.replace("\n", "\r\n") in new.replace("\n", "\r\n"):
            print("REFUSING (NEW contains OLD)", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], repr(old[:50])); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
