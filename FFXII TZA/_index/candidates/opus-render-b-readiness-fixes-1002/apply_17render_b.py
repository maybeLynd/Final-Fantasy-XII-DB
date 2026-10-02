"""apply_17render_b.py [--apply] - 17-Presentation-Rendering readiness map (cloud-reports/re-readiness/17-render.md),
section 3.1 value-changing items GP.CV-10 .. CM.CV-23 (report lines 2800-3212, part B), settled at the shipping image
and, where a census decides, at the shipped data (OPUS, 2026-10-02).

Each edit strikes the side the image (or FFXII_TZA.vbf through vbf_read_entry) REFUTES and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)*; every deciding address inside a function is cited as entry+offset. The verdict
table is scratchpad re17b/verdicts-17b.md (copied into consumer-check.md when this candidate is published).
Items decided with no page wrong, or left undecided, carry no edit: GP.CV-10/11, EF.CV-15/18, ET.CV-4/7/10,
MF.CV-4/6/10, MM.CV-9 (part A), MM.CV-13/17/18/19/20, PP.CV-7/8/12, CM.CV-9/18. EF.CV-21's line already opens a
two-line strike, so no per-line-balanced edit fits it. Refuted text outside 17-Presentation-Rendering (CM.CV-4/5/17 on
the world-tick page, CM.CV-23 on the frame page, CM.CV-11's register row) is left for its own folder's owner.
Sections 3.2 (counts) and 3.3 (stale/banner items) are not covered by this candidate.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment in the block's comment syntax instead of a strike (their OLD
includes the line end, so NEW never contains OLD); the one front-matter edit is a trailing `# <- corrected` comment.
No heading changes; no census TSV edits.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "17-Presentation-Rendering/"
VIF = F + "Legacy-PS2-GS/the-vif1-vu1-layer.md"
TEX = F + "Legacy-PS2-GS/texture-mip-local-memory-budget.md"
TRAIL = F + "Character-Render-Records/the-bone-trails.md"
GI = F + "Gi-Render-Commands/gi-render-command-family.md"
DISP = F + "Effect-File-Formats/effect-element-type-dispatch.md"
EFX = F + "Effect-File-Formats/efx-and-efb-effect-containers.md"
E00 = F + "Effect-File-Formats/the-element-types-00-0a.md"
E80 = F + "Effect-File-Formats/the-element-types-80-97.md"
E60 = F + "Effect-File-Formats/the-element-types-60-74.md"
E40 = F + "Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md"
MENU = F + "Effect-File-Formats/the-menu-effect-registry.md"
FCP = F + "Model-And-Motion-Formats/fcp-character-parameter-block.md"
MR = F + "Model-And-Motion-Formats/README.md"
FDM = F + "Model-And-Motion-Formats/fdm-and-for-entries.md"
FTR = F + "Model-And-Motion-Formats/ftr-node-table.md"
FRP = F + "Model-And-Motion-Formats/frp-object-container.md"
FTE = F + "Model-And-Motion-Formats/fte-fct-texture-colour-tables.md"
FEF = F + "Model-And-Motion-Formats/fef-and-motion-entries.md"
OSC = F + "Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md"
POSE = F + "Model-And-Motion-Formats/the-pose-sequencer.md"
CS = F + "Post-Processing/CONTRACT-post-processing-subsystem.md"
CAT = F + "Post-Processing/the-post-processing-effect-catalogue.md"
CP = F + "Post-Processing/CONTRACT-ppfx-effect-creation.md"
PI = F + "Post-Processing/ppfx-function-identification.md"
RR = F + "Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md"
L = F + "Render-Command-List/the-ordered-render-command-list.md"
SF = F + "Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md"
PTS = F + "Position-To-Scalar/how-a-position-becomes-a-single-number.md"
P = F + "Scripted-Camera/the-scripted-camera-player.md"
MH = F + "Movie-Containers/mh-movie-seek-index.md"
AF = F + "Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md"
FADE = F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md"

T = "*(corrected 2026-10-02, OPUS: "
C = "<- corrected 2026-10-02, OPUS - "
SETUP = "`005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type "
RENDERER = ("the renderer object `&GameApplication[0xE8]` (a `PRendererBase`), whose `+0x18C0` is the device " + T +
            "`0017D000`+0x4F `lea rcx, [rbx + 0xe8]` is stored at record `+8` by `00184F20`+0x2C; "
            "`00187950`+0x3AF `mov r8, qword ptr [r14 + 8]` passes it; Gi family page section 19b)*")
FIXUP = ("`0072DCF0` formats `%s%d` for each counted variant (`0072DCF0`+0x90..+0xA4) and registers each one under "
         "all 22 suffixes of the table at `02EA2250` (`0072DCF0`+0x1EC `lea rdi, [02EA2250]`, +0x1F3 `lea esi, [rbp + 0x16]`)")

EDITS = [
    # GP.CV-12: only OFFSET/BASE mask with 0x3FF (0022C970+0x99, +0xBD); the MPG arm indexes unmasked (+0xD5, +0xDF).
    (VIF, "MSCAL then calls it. The `0x3FF` masks and the 1,024-entry\naddress space are VU1's.",
     "MSCAL then calls it. ~~The `0x3FF` masks and the 1,024-entry~~ On PS2 the `0x3FF` masks and the 1,024-entry\n"
     "~~address space are VU1's.~~ address space are VU1's; here only the OFFSET and BASE arms mask, and MPG stores at "
     "the unmasked imm16 " + T + "`0022C970`+0x99 and +0xBD `and bx, r8w`; `0022C970`+0xD5 `movzx ecx, bx`, +0xDF "
     "`mov qword ptr [r9 + rcx*8], rax`; the micro-memory row below)*."),

    # GP.CV-13: 004EF860 stores a DWORD word[02064DB8]+0x8000 and the last 12 bytes of the DD0 cell.
    (VIF, "1. writes a 16-bit word `+ 0x8000` into the VU cell at register `02064DB0` (`004EF8A7`–`004EF8B6`);\n"
          "2. copies the cell at register `02064DD0` beside it;",
     "1. writes ~~a 16-bit word `+ 0x8000`~~ the dword `word[02064DB8] + 0x8000` into the VU cell at register "
     "`02064DB0` (`004EF8A7`–`004EF8B6`) " + T + "`004EF860`+0x3C `movzx eax, word ptr [02064DB8]`, +0x47 "
     "`add ax, r9w`, +0x56 `mov dword ptr [rcx], eax`)*;\n"
     "2. ~~copies the cell at register `02064DD0` beside it;~~ copies bytes `+0x04`..`+0x0F` of the cell at register "
     "`02064DD0` into `+0x04`..`+0x0F` of it, staged at `02064C60` " + T + "`004EF860`+0x26 `movups xmm1, xmmword ptr "
     "[r8 + rbx]`, +0x8C `movsd qword ptr [rdx + rbx + 4], xmm0`, +0x92 `movd dword ptr [rdx + rbx + 0xc], xmm1`)*;"),

    # GP.CV-17: 0018B100's third argument is &GameApplication[0xE8], not the device.
    (VIF, "`0018B100(list, whole, device)` twice a frame. `0018B100` asks",
     "~~`0018B100(list, whole, device)`~~ `0018B100(list, whole, renderer)`, with " + RENDERER + ", twice a frame. "
     "`0018B100` asks"),
    (GI, "**The drain is the render pass list.** `FUN_0018B100(list, whole, device)` is called twice",
     "**The drain is the render pass list.** ~~`FUN_0018B100(list, whole, device)`~~ `FUN_0018B100(list, whole, "
     "renderer)`, with " + RENDERER + ", is called twice"),

    # GP.CV-14: the command object is 0x640 bytes (001DB840+0x35); 0x488 is the payload size (0051BC70+0x4F4).
    (TRAIL, "  queues one render command of `0x488` bytes with the VU1 microprogram",
     "  queues one render command ~~of `0x488` bytes~~ with a `0x488`-byte payload (the `GiVmax` command itself is "
     "`0x640` bytes) " + T + "`0051BC70`+0x4F4 `mov dword ptr [rsp + 0x20], 0x488`; `001DB840`+0x35 `mov edx, 0x640` "
     "before the arena call at +0x3A)* with the VU1 microprogram"),

    # GP.CV-15: 00467AA0 subtracts both runtime totals before the page mask (+0x17, +0x1D, +0x23).
    (TEX, "**fixed 1.375 MiB / 176 pages** on every machine. Section 6 now says so.",
     "**~~fixed 1.375 MiB / 176 pages~~** at most 1.375 MiB / 176 pages on every machine, less the two runtime totals "
     "rounded to whole pages, so 175 pages or fewer once any texture record with a level is present " + T + "`00467AA0`"
     "+0x17 and +0x1D subtract `[02CA6008]` and `[02CA6004]` before the `and eax, 0xfffff800` at +0x23; every "
     "class's minimum footprint is `0x800` words, section 6's precision)*. Section 6 now says so."),
    # GP.CV-16: the published maximum is the whole mip chain's footprint (002F7380+0xB1..+0xBB).
    (TEX, "3. compute the maximum single-image footprint and a weighted aggregate; publish both through",
     "3. compute the maximum ~~single-image~~ single-record mip-chain footprint " + T + "`002F7380`+0xB1 `call "
     "00466190` (the chain sum), +0xB6 `cmp esi, eax`, +0xBB `cmovl esi, eax`)* and a weighted aggregate; publish "
     "both through"),

    # EF.CV-1 / ET.CV-9: 02EBEF88 points at the current context's +0x1B8 block; the stamp is its first dword.
    (DISP, "If `+0x38` already equals the global frame stamp `[02EBEF88]`, it returns 0. Otherwise",
     "If `+0x38` already equals ~~the global frame stamp `[02EBEF88]`~~ the frame stamp `dword [[02EBEF88]]`, the "
     "first dword of the current context's `+0x1B8` block that `02EBEF88` points to " + T + "`002F2530`+0x44 `mov rax, "
     "qword ptr [02EBEF88]`, +0x4B `mov ecx, dword ptr [rax]`, +0x4D `cmp dword ptr [rbx + 0x38], ecx`; `0024D540`+0xC6 "
     "`lea rax, [rdi + 0x1b8]` is what +0xCD stores)*, it returns 0. Otherwise"),

    # EF.CV-2 / EF.CV-3: element +0x20 is the definition; +0x44 is the element's current frame, not an expression id.
    (DISP, "*Read for its shape, not whole.* `rdi` is the element and `r14 = qword[element + 0x20]` its owner, the same two",
     "*Read for its shape, not whole.* `rdi` is the element and `r14 = qword[element + 0x20]` ~~its owner~~ its "
     "definition " + T + "`002F2D60`+0x3B `mov qword ptr [rcx + 0x20], rax` stores the instance's `+0x108` "
     "definition there)*, the same two"),
    (DISP, "0042FDB0(owner + 0x170 + n*0x50, dword[element + 0x44])   ; the transform workbench, with the element's "
           "expression id\n",
     "0042FDB0(owner + 0x170 + n*0x50, dword[element + 0x44])   ; the transform workbench, with the element's "
     "expression id   ; " + C + "owner is the definition and +0x44 the element's current frame, trunc(+0x3C) or its "
     "loop remainder (002F2530+0xB4..+0xFA); 0042FDB0+0x15 keeps it as the time argument of 004314E0\n"),
    (DISP, "slot handed to `0042FDB0` with the element's expression id from `+0x44` and **skipped",
     "slot handed to `0042FDB0` with the element's ~~expression id~~ current frame " + T + "`002F2530`+0xB4..+0xFA "
     "stores `trunc(+0x3C)`, or its remainder by the definition's loop length, in `+0x44`; `0042FDB0`+0x15 passes it on "
     "as the key time)* from `+0x44` and **skipped"),

    # EF.CV-4 / EF.CV-5: +0x3C += dt in every update; the step adds 1.0 once, at birth, on the 60 fps arm; 001EDDA0 is a
    #     frame-rate test, not a pause.
    (DISP, "         +0x3C  f32  frame counter, +1.0 per step (unless paused)\n",
     "         +0x3C  f32  frame counter, +1.0 per step (unless paused)   " + C + "+= dt in every update "
     "(002F2530+0x52); the step adds 1.0 once, at birth, and only when 00314960() is non-zero and 001EDDA0() is 0 "
     "(002F3BC0+0x281..+0x2A0); 001EDDA0 is the frame-rate test (0 only while 01F82E38 is set by 001EDDC0+0x28 and "
     "01DFE0C0 is 0), not a pause\n"),
    (DISP, "and either the pause predicate `001EDDA0` true or `+0x40` bit 0 clear,",
     "and either ~~the pause predicate~~ the frame-rate test `001EDDA0` true " + T + "it returns 0 only while "
     "`[01F82E38]` is set and `[01DFE0C0]` is 0, `001EDDA0`+0x0..+0x12; the 60 fps arm `001EDDC0`+0x28 sets "
     "`01F82E38`)* or `+0x40` bit 0 clear,"),
    (DISP, "*Return*: when the pause predicate is false, the owner record",
     "*Return*: when ~~the pause predicate~~ the frame-rate test `001EDDA0` " + T + "not a pause, as above)* is false, "
     "the owner record"),

    # EF.CV-6 / EF.CV-14: the chains are walked only for six kinds or with the action-context bit; they are one
    #     doubly-linked list walked from either end.
    (DISP, "3. **It then walks one of two element chains** (`00441A15`–`00441A82`), calling",
     "3. **It then walks ~~one of two element chains~~** the instance's one doubly-linked element list, forward from "
     "head `+0x118` or backward from tail `+0x128`, but only on the step-2 path or for the six kinds `0x40`, `0x41`, "
     "`0xA1`, `0xA2`, `0xA5`, `0xD0`; every other kind returns without walking " + T + "`00441970`+0x3C..+0x5E "
     "switch, other kinds to the tail at +0x119; `002F31C0`+0x90..+0xC4 unlinks through `+0x28` prev / `+0x30` next "
     "with head `+0x118` and tail `+0x128`; section 2.8)* (`00441A15`–`00441A82`), calling"),

    # EF.CV-7: step 47 types -> 41 functions, update 47 -> 38; the audit's "no two share" is wrong.
    (DISP, "Within the step, update and walk methods each type has its own function. The setup method alone",
     "~~Within the step, update and walk methods each type has its own function.~~ The step and update methods "
     "share too: 47 step cases call 41 functions (`0x80`/`0x82`/`0x83` share `0044CC10`, `0x8C`/`0x94`/`0x95`/`0x97` "
     "`00455390`, `0x8F`/`0x90` `00457E10`) and 47 update cases reach 38 " + T + "decoded from the case blocks of "
     "`002F3BC0` and `002F3910`)*. ~~The setup method alone~~ The setup method also"),
    (DISP, "and every open item the page lists as unread.\n",
     "and every open item the page lists as unread. # " + C + "the 47 step case blocks call only 41 distinct "
     "functions (0044CC10, 00455390 and 00457E10 are shared), so types do share step handlers\n"),

    # EF.CV-8: draw-list entry +8 is the sort key (003A3A50+0x103, +0x233).
    (DISP, "So the entry is **40 bytes (`0x28`)**: `qword[+0]` zero, the **24-bit flags** at `+8` with a nibble from",
     "So the entry is **40 bytes (`0x28`)**: `qword[+0]` zero, the **24-bit ~~flags~~ sort key** " + T + "the merge "
     "sort compares it, `003A3A50`+0x103 and +0x233; below)* at `+8` with a nibble from"),
    (DISP, "at `[02F8F2F8]`, each carrying a 24-bit flags word.",
     "at `[02F8F2F8]`, each carrying a 24-bit ~~flags word~~ sort key " + T + "`003A3A50`+0x103 `mov eax, dword ptr "
     "[rsi + r9 + 8]`; `00540DB0`+0x44 stores it)*."),

    # EF.CV-9: 0024D540 is the per-frame effect pass; both callers of 003A9BA0 rebase contexts by a delta.
    (DISP, "from instance creation `0024D540` / `0024D970`. **So it is the setup method**",
     "from ~~instance creation~~ the context rebase arms of the per-frame effect pass `0024D540` (`0024D540`+0x114) and "
     "of `0024D970` (`0024D970`+0x26), which pass the relocation delta " + T + "`003A9BA0` adds the delta to each "
     "element pointer and calls `005004C0`; `0024D540`+0x16 drains the draw list)*. **So it is the setup method**"),

    # EF.CV-10: 002F2D60+0x44 `and byte ptr [rcx + 1], 0xf9` clears bits 1 and 2 only.
    (DISP, "its definition → `+0x20`, and clears the flag byte `+0x1`; the tail",
     "its definition → `+0x20`, and ~~clears the flag byte `+0x1`~~ clears bits 1 and 2 of the flag byte `+0x1` "
     + T + "`002F2D60`+0x44 `and byte ptr [rcx + 1], 0xf9`)*; the tail"),
    (DISP, "copies the `+0x80`/`+0x90` quads to `+0x60`/`+0xB0`, clears `+1` bits\n`0xF9`), then switches",
     "copies the `+0x80`/`+0x90` quads to `+0x60`/`+0xB0`, ~~clears `+1` bits~~ ANDs `+1` with `0xF9`, clearing "
     "bits 1 and 2 " + T + "`002F2D60`+0x44)*\n~~`0xF9`~~), then switches"),

    # EF.CV-11: the fifteen creation arms' type labels, by 005004C0's table (members/effect-type-methods.tsv agrees).
    *[(DISP, "`%s` (%s) is the `+0x44 = %s`%s creation arm" % (fn, sz, old, tail),
       "`%s` (%s) is the ~~`+0x44 = %s`%s~~ `+0x44 = %s`%s %s" % (fn, sz, old, tail, new, tail2, T + SETUP + new +
                                                                  " here)*") + " creation arm")
      for fn, sz, old, tail, new, tail2 in (
          ("00539030", "316 B", "0x47", "", "0x08", ""),
          ("00539740", "302 B", "0x52", "", "0x89", ""),
          ("00539610", "302 B", "0x51", "", "0x88", ""),
          ("00539870", "260 B", "0x53", "", "0x8A", ""),
          ("00538DB0", "254 B", "0x44", "", "0x05", ""),
          ("00539170", "246 B", "0x48", "", "0x0A", ""),
          ("005393B0", "232 B", "0x4E", "", "0x85", ""),
          ("00539E90", "225 B", "0x5B", "/`0x5C` shared", "0x91", "/`0x92` shared"),
          ("00539DA0", "225 B", "0x59", "/`0x5A` shared", "0x8F", "/`0x90` shared"),
          ("00539C10", "223 B", "0x56", "", "0x8D", ""),
          ("00539F80", "222 B", "0x5F", "", "0x97", ""),
          ("00539980", "218 B", "0x4D", "/`0x54` shared", "0x84", "/`0x96` shared"),
          ("00539B30", "211 B", "0x58", "/`0x5D`/`0x5E` shared", "0x8C", "/`0x94`/`0x95` shared"),
          ("00539A60", "204 B", "0x57", "", "0x8B", ""),
          ("005394A0", "178 B", "0x4F", "", "0x86", ""))],

    # EF.CV-12: the leaf routes 17 types to bodies, not eight.
    (DISP, "*Measured across the whole leaf after reading `'h'`: **12,463 bytes in eight bodies, and one pattern.*** Every arm",
     "*Measured across ~~the whole leaf~~ the eight arms in bold above after reading `'h'`: **12,463 bytes in eight "
     "bodies, and one pattern.*** " + T + "the leaf routes nine more types through its jmp stubs to bodies of their "
     "own - `0047BFA0`, `005294F0`, `0052A360`, `0052B080`, `0052D920`, `0052EA90`, `00528150`, `00528B50` and "
     "`0052C070`, decoded at `0043ED30`+0x14..+0x28; most of them also call `0042FDB0` and test `0x80808080`)* Every "
     "arm"),

    # EF.CV-13: four movaps copy +0x250..+0x28F (00449AB0+0xB4..+0xD7).
    (DISP, "then four `movaps` copy `element + 0x250 … +0x27F` — a",
     "then four `movaps` copy ~~`element + 0x250 … +0x27F`~~ `element + 0x250 … +0x28F` " + T + "`00449AB0`+0xB4.."
     "+0xD7 read `+0x250`, `+0x260`, `+0x270` and `+0x280`)* — a"),

    # EF.CV-16: the floor-probe gate is mask 4 = bit 2 (002F3750+0x2A).
    (DISP, "when `byte[[rcx+0x20]+0x4B]` lacks bit `4` the answer",
     "when `byte[[rcx+0x20]+0x4B]` ~~lacks bit `4`~~ lacks bit 2 (mask `0x04`) " + T + "`002F3750`+0x2A `test byte "
     "ptr [rdi + 0x4b], 4`)* the answer"),

    # EF.CV-17: the chunk header has a fourth field, i32 +0x08, and the handler takes chunk + 0xC.
    (EFX, "+0x06  u16   type      0x600 | 0x610 | 0x620 | 0x630 | 0x700 | 0x800 | 0xA00   (0x701 withdrawn 2026-09-12)\n",
     "+0x06  u16   type      0x600 | 0x610 | 0x620 | 0x630 | 0x700 | 0x800 | 0xA00   (0x701 withdrawn 2026-09-12)   "
     + C + "the header is 0x0C bytes: an i32 at +0x08 follows, stored to 02EBB738 before each handler "
     "(003EDAD0+0x4A6..+0x4AC), and the handler gets chunk + 0xC (003EDAD0+0x4C3); section 2b\n"),
    # EF.CV-19: four callers read +0x0C.
    (EFX, "version number, compared byte-by-byte, a 16-byte header whose second half nothing reads, and a",
     "version number, compared byte-by-byte, a 16-byte header ~~whose second half nothing reads~~ whose `+0x0C` is "
     "the stream length four of the loader's callers pass " + T + "`003B0660`+0xDF `mov edx, dword ptr [rbx + 0xc]` "
     "before the loader call; section 2b)*, and a"),
    # EF.CV-20: 00333C80 rewrites EFX0009/EFX0008 records.
    (EFX, "**What loading normalises:** nothing in the header. The `0x600` chunk zero-fill (§2) is the only\n"
          "normalisation found, and it is per-chunk rather than per-file.",
     "**What loading normalises:** nothing in the header. ~~The `0x600` chunk zero-fill (§2) is the only~~\n"
     "~~normalisation found, and it is per-chunk rather than per-file.~~ Per chunk, the `0x600` zero-fill and the "
     "binder `00333C80`, which rewrites an `EFX0009` / `EFX0008` record into the `EFX0010` layout " + T + "`00333C80`"
     "+0x21 `mov ecx, dword ptr [01EFF3B0]`, +0x27 `cmp ecx, 9`; section 2b)*."),
    # EF.CV-21 (no 0x710 type; the loader compares 0x600-0x630, 0x700, 0x800, 0xA00 from 003EDAD0+0xF5) is left: its
    #     line already opens a two-line strike, so no per-line-balanced edit fits it.

    # EF.CV-22: type 0x06's ten floats land in an explicit permutation (00447830+0x1B4..+0x29B).
    (E00, "ten floats `def+0x140`..`def+0x1D0` -> `+0x240`..`+0x264` (each `def+0x10*k` to its own field);",
     "ten floats `def+0x140`..`def+0x1D0` -> `+0x240`..`+0x264` (~~each `def+0x10*k` to its own field~~ "
     "`+0x1C0`/`+0x1D0` to `+0x240`/`+0x244`, `+0x140`..`+0x160` to `+0x254`..`+0x25C`, `+0x170`..`+0x190` to "
     "`+0x248`..`+0x250`, `+0x1A0`/`+0x1B0` to `+0x260`/`+0x264` " + T + "`00447830`+0x1B4..+0x29B)*);"),
    # ET.CV-6: type 0x05's record ends at +0x620; 0x06/0x07's at +0x6E0 is larger.
    (E00, "`RS@+0x5A0` — the record reaches `+0x5A0`, the largest of the group.",
     "`RS@+0x5A0` — the record ~~reaches `+0x5A0`, the largest of the group~~ ends at `+0x620`, and types "
     "`0x06`/`0x07`'s at `+0x6E0` is larger " + T + "`00538DB0`+0xE7 `lea rax, [rbp + 0x620]`; `00538EB0`+0x15E "
     "`lea rax, [rbp + 0x6e0]`)*."),

    # ET.CV-1: the step order is base, tail, then PRNG for 0x80-0x97, 0x0A and 0xA0.
    (E80, "- `0x80`/`0x82`/`0x83` — identical step `0044CC10` (54 B = base + PRNG `0044B960` +\n"
          "  tail `00450CE0`), identical update",
     "- `0x80`/`0x82`/`0x83` — identical step `0044CC10` (54 B = base + ~~PRNG `0044B960` +~~\n"
     "  tail `00450CE0` + PRNG `0044B960` " + T + "`0044CC10`+0x1B calls the tail, +0x20 the PRNG)*), identical update"),
    (E80, "  `003A6E60` + `003D8E50` + PRNG + tail `0045B640`), identical update `0045B260`,",
     "  `003A6E60` + `003D8E50` + ~~PRNG + tail `0045B640`~~ tail `0045B640` + PRNG " + T + "`00455390`+0xB4 and +0xB9)*), "
     "identical update `0045B260`,"),
    # ET.CV-2: the 0x95 / 0x97 walks jump to their own bodies, not to 0045B640.
    (E80, "| `0045B2A0` (`0x95`) | `*rcx != 0` | shared tail `0045B640` (read 2026-09-29, GI-11 group B1) |",
     "| `0045B2A0` (`0x95`) | `*rcx != 0` | ~~shared tail `0045B640`~~ its own body `0045B2B0` (902 B) " + T + "`0045B2A0`"
     "+0x3 `jne 0045B2B0`; `0045B640` is the step's tail)* (read 2026-09-29, GI-11 group B1) |"),
    (E80, "| `0045BAD0` (`0x97`) | `*rcx != 0` | shared tail `0045B640` (read 2026-09-29, GI-11 group B1) |",
     "| `0045BAD0` (`0x97`) | `*rcx != 0` | ~~shared tail `0045B640`~~ its own body `0045BAE0` (1,068 B) " + T +
     "`0045BAD0`+0x3 `jne 0045BAE0`)* (read 2026-09-29, GI-11 group B1) |"),
    # ET.CV-3: 0x96 shares setup 00539980 with 0x84, so it is family A.
    (E80, "+ `00431770` init(s) + one resource store | `0x8C`–`0x92`, `0x94`–`0x97` |",
     "+ `00431770` init(s) + one resource store | ~~`0x8C`–`0x92`, `0x94`–`0x97`~~ `0x8C`–`0x92`, `0x94`, `0x95`, "
     "`0x97`; `0x96` is family A " + T + SETUP + "`0x84` and `0x96` to the same setup `00539980`)* |"),

    (E60, "called inside the step bodies of `0x0A`, `0x60`–`0x62`, `0x65`, `0x66` before the type tail |",
     "called inside the step bodies of `0x0A`, `0x60`–`0x62`, `0x65`, `0x66` before the type tail, except in "
     "`0x0A`'s, where it runs ~~before~~ after its tail " + T + "`0044BA80`+0x1B calls the tail `0044C850`, +0x20 "
     "the PRNG)* |"),
    (E40, "| `0xA0` | step `00460B80` (54 B: base+PRNG+tail `00460F30`),",
     "| `0xA0` | step `00460B80` (54 B: ~~base+PRNG+tail `00460F30`~~ base + tail `00460F30` + PRNG " + T +
     "`00460B80`+0x1B and +0x20)*),"),

    # ET.CV-5: the 4-track-group ranges.
    (E60, "of **nine** 4-track groups `+0x1C0`–`+0x460`, `00431770@+0x490`, record end",
     "of **nine** 4-track groups ~~`+0x1C0`–`+0x460`~~ starting `+0x1C0`–`+0x440` " + T + "`0053A5D0`+0xBE `lea "
     "rbx, [r14 + 0x1c0]`, nine passes of +0xD5..+0xED)*, `00431770@+0x490`, record end"),
    (E60, "  stride `+0x1C0`–`+0x3F0` plus 12 singles and three `00431770` inits",
     "  stride ~~`+0x1C0`–`+0x3F0`~~ starting `+0x1C0`–`+0x440` " + T + "`0054F7C0`+0x84 to +0xF4, the last at "
     "`lea rcx, [rdi + 0x440]`)* plus 12 singles and three `00431770` inits"),
    (E60, "start for `0x73`/`0x74` then group runs at `+0x190`–`+0x480`), 14–20 single heads,",
     "start for `0x73`/`0x74` ~~then group runs at `+0x190`–`+0x480`~~, which carry only those three 4-track groups and "
     "then 1-track / 3-track pairs from `+0x180` " + T + "`0054FFF0`+0x2B, +0x39 and +0x47 are its only `0042FCF0` "
     "calls, likewise in `00550200`)*), 14–20 single heads,"),

    # ET.CV-8: 00460120 releases +0x338 directly (003697F0); only +0x3B0 goes to the queue.
    (MENU, "as a pointer pushed to the deferred-free queue (`005294B0`, `00460120`), so",
     "as a pointer pushed to the deferred-free queue (`005294B0`~~, `00460120`~~) " + T + "`00460120`+0x15 releases "
     "`+0x338` directly through `003697F0`; only its `+0x3B0` goes to the queue, `00460120`+0x45 `jmp 0024B1C0`)*, so"),

    # MF.CV-1 / MF.CV-2: section 3's ids against the table at 01EED320.
    (FCP, "| `+0x178` | 0 (7) | `0x09000000` (`0x09000706`) | 9 · 0 · 0 (0), or 6 (7) |",
     "| `+0x178` | 0 (7) | `0x09000000` (~~`0x09000706`~~ `0x09000606`) | 9 · 0 · 0 (0), or ~~6 (7)~~ 6 (6) " + T +
     "`01EED320` index 7)* |"),
    (FCP, "| `+0x180` → `+0x17C` → `+0x150` | 1 (8) | `0x09000202` (`0x09000908`) | 9 · 0 · 2 (2), or 8 (9) |",
     "| `+0x180` → `+0x17C` → `+0x150` | 1 (8) | `0x09000202` (~~`0x09000908`~~ `0x09000808`) | 9 · 0 · 2 (2), or "
     "~~8 (9)~~ 8 (8) " + T + "`01EED320` index 8)* |"),
    (FCP, "| 2 (9) | `0x09000201` (`0x09000807`) | 9 · 0 · 1 (2), or 7 (8) | × y-scale; `003E6150` leaves it |",
     "| 2 (9) | ~~`0x09000201` (`0x09000807`)~~ `0x09000101` (`0x09000707`) | ~~9 · 0 · 1 (2), or 7 (8)~~ 9 · 0 · 1 (1), "
     "or 7 (7) | × y-scale; `003E6150` ~~leaves it~~ × " + T + "`01EED320` indices 2 and 9; `003E6150`+0x7D `cmp ebx, "
     "0x9000101` and +0x71 `cmp ebx, 0x9000707` are on its multiply list)* |"),
    (FCP, "| `+0x16C` | 3 (10) | `0x09000403` (`0x09000A09`) | 9 · 0 · 3 (4), or 9 (10) |",
     "| `+0x16C` | 3 (10) | ~~`0x09000403` (`0x09000A09`)~~ `0x09000303` (`0x09000909`) | ~~9 · 0 · 3 (4), or 9 (10)~~ "
     "9 · 0 · 3 (3), or 9 (9) " + T + "`01EED320` indices 3 and 10)* |"),
    (FCP, "| `+0x164` | 4 | `0x09000504` | 9 · 0 · 4 (5) |",
     "| `+0x164` | 4 | ~~`0x09000504`~~ `0x09000404` | ~~9 · 0 · 4 (5)~~ 9 · 0 · 4 (4) " + T + "`01EED320` index 4)* |"),
    (FCP, "| `+0x168` | 5 | `0x09052A2F` | 9 · 5 · 47 (42) |",
     "| `+0x168` | 5 | ~~`0x09052A2F`~~ `0x09052B2F` | ~~9 · 5 · 47 (42)~~ 9 · 5 · 47 (43) " + T + "`01EED320` index 5)* |"),
    (FCP, "| `+0x1AC` | 32 | `0x09082032` | 9 · 8 · 50 (32) |",
     "| `+0x1AC` | 32 | ~~`0x09082032`~~ `0x09082C32` | ~~9 · 8 · 50 (32)~~ 9 · 8 · 50 (44) " + T + "`01EED320` index "
     "32)* |"),
    (FCP, "| `+0x1B0` (int) | 31 | `0x29081131` | 9 · 8 · 49 (17), dword mode |",
     "| `+0x1B0` (int) | 31 | ~~`0x29081131`~~ `0x29081031` | 9 · 8 · 49 ~~(17)~~ (16), dword mode " + T + "`01EED320` "
     "index 31)* |"),
    # MF.CV-3: section 9 slots 10, 14-25 and 31 are read through the same table.
    (FCP, "+0x00  f32[49]   slot           authored floats; slots 0-9, 30, 32-36, 38-41, 43, 45-48 are read (section 3)\n",
     "+0x00  f32[49]   slot           authored floats; slots 0-9, 30, 32-36, 38-41, 43, 45-48 are read (section 3)   "
     + C + "slots 10, 14-25 and 31 are read too: 01EED320 indices 11, 12-23 and 33 hold 09000A0A, 09000E0F..09001819 "
     "and 09001E1F; slots 40 and 41 are read as dwords (29010128, 29010229)\n"),

    # MF.CV-5: .adm opens with an i16 track count, not a magic.
    (MR, "`.adm` is `04 00 01 00` and the binary names it",
     "~~`.adm` is `04 00 01 00`~~ `.adm` opens with an `i16` track count, so 35 of the 39 files begin `04 00 01 00` "
     "and the two-track and one-track files do not; nothing compares a magic " + T + "`001BE1A0`+0x5B reads the count "
     "with `movsx`; the add-motion sheet's census)* and the binary names it"),

    # MF.CV-7: @FOR +0x01 is the fourth list's packing kind.
    (FDM, "| `+0x01` | u8 = 0 | sampled |",
     "| `+0x01` | u8 ~~= 0~~ packing kind of the fourth list " + T + "`0053AB50`+0x16DF `movzx eax, byte ptr [rbx + 1]` "
     "on the flag-1 pass)* | sampled |"),
    # MF.CV-8: the @FOR offset is at the model resource's +0x208; the view depth is the record's (or argument's) +0x208.
    (FDM, "1. Resolves the `@FOR` entry (index `rec+0x208` + base `rec+0x1F8`), checks",
     "1. Resolves the `@FOR` entry (index ~~`rec+0x208` + base `rec+0x1F8`~~ `+0x208` + base `+0x1F8` of the model "
     "resource `004780B0(word[record+0x64])`, not of the render record " + T + "`004201F0`+0x42 `call 004780B0`, "
     "+0x50 `mov ecx, dword ptr [rax + 0x208]`, +0x6C; the view depth `f32[+0x208]` of step 4 is read from the record "
     "or the second argument at +0x192)*), checks"),
    # MF.CV-9: @FTR +0x38 is read as a word.
    (FDM, "  `00373060` bounds the ordinal by `@FTR u32 +0x38` (`003730BA`) — the data",
     "  `00373060` bounds the ordinal by ~~`@FTR u32 +0x38`~~ `@FTR u16 +0x38` " + T + "`00373060`+0x5A `movzx ecx, word "
     "ptr [rax + 0x38]`)* (`003730BA`) — the data"),
    (FTR, "+0x38  u32      tailU16    count of the u16 override slots after the node list\n",
     "+0x38  u32      tailU16    count of the u16 override slots after the node list   " + C + "read as a u16: "
     "00373060+0x5A and 003712E0+0x25 movzx word ptr [rax + 0x38]\n"),
    # MM.CV-6: the @FCT record stride is 0x10.
    (FDM, "(`word[@FCT + (pal+3)·8]` summed, `0053B620`–`0053B64D`).",
     "(~~`word[@FCT + (pal+3)·8]`~~ `word[@FCT + (pal+3)·0x10]` " + T + "`0053AB50`+0xADC `add rax, rax` then +0xADF "
     "`movzx eax, word ptr [rdi + rax*8]`)* summed, `0053B620`–`0053B64D`)."),

    # MM.CV-1 / MM.CV-2: NameEquals returns 0 on a match and the finder hits on non-zero; the name field is 32 bytes.
    (FRP, "      if (NameEquals(blob+0x10, wantName)) -> hit       0x00409006 / 0x00409066\n",
     "      if (NameEquals(blob+0x10, wantName)) -> hit       0x00409006 / 0x00409066   " + C + "the helper returns "
     "0 when the 32 bytes match (00408F30+0x3E) and 1 otherwise (+0x41), and the finder takes non-zero as the hit "
     "(00408FA0+0x6E jne), so a supplied name selects files whose name differs (section 7)\n"),
    (FRP, "+0x10  char[16]  name           NUL-terminated; matches the filename stem 4,230 / 4,230\n",
     "+0x10  char[16]  name           NUL-terminated; matches the filename stem 4,230 / 4,230   " + C + "char[32]: "
     "00408F30+0x0..+0x3C compares eight dwords, so +0x20..+0x2F below are the name's NUL tail (section 7)\n"),
    # MM.CV-3: @FMN's kind dword is 0x02001111 or 0x02001011.
    (FRP, "`2, n`; `@FMN` carries `0x02000211` and a count)",
     "`2, n`; `@FMN` carries ~~`0x02000211`~~ `0x02001111` or `0x02001011` " + T + "read through `vbf_read_entry` from "
     "`FFXII_TZA.vbf`, a 200-file `.ca` sample: no `@FMN` carries `0x02000211`)* and a count)"),
    # MM.CV-4 / MM.CV-5: @FTE / @FCT +0x0C is the record count.
    (FTE, "+0x00  '@FTE', u32 kind = 0, u32 entryLen, u32 0\n",
     "+0x00  '@FTE', u32 kind = 0, u32 entryLen, u32 0   " + C + "the last u32 (+0x0C) is the record count, 1 to 12 "
     "and never 0 in the 1,044 @FTE entries of the shipped .cm files (vbf_read_entry)\n"),
    (FTE, "+0x00  '@FCT', u32 kind = 0, u32 entryLen, u32 0\n",
     "+0x00  '@FCT', u32 kind = 0, u32 entryLen, u32 0   " + C + "the last u32 is the +0x0C count below, never 0 in "
     "the 1,044 @FCT entries (vbf_read_entry)\n"),

    # MM.CV-7: 003E7450(obj, event = low nibble of byte +2, choice = byte +3, 0).
    (FEF, "else hi nibble gates `byte+0x413` counter, lo nibble → `003E7450(obj, byte+3, 0, lo)`.",
     "else hi nibble gates `byte+0x413` counter, lo nibble → ~~`003E7450(obj, byte+3, 0, lo)`~~ `003E7450(obj, lo, "
     "byte+3, 0)` " + T + "`00520D30`+0x8D `and edx, 0xf`, +0xA1 `movzx r8d, byte ptr [rdi + 3]`, +0xA6 `xor r9d, "
     "r9d`, +0xAC the call)*."),
    # MM.CV-8: op 0x09's payload is a name unless the stream header's byte +4 has bit 0 or 1.
    (FEF, "index `s16[ctx+0x2A] + word[cmd+2]>>1` (`word[cmd+4]==1` selects the alternate arm). |",
     "~~index `s16[ctx+0x2A] + word[cmd+2]>>1` (`word[cmd+4]==1` selects the alternate arm)~~ by the name at "
     "`cmd+2`, or, when the stream header's byte `+4` has bit 0 or 1, by index `s16[ctx+0x2A] + word[cmd+2]>>1` " + T +
     "`00417F40`+0xA3 `test byte ptr [r12 + 4], 3`; +0xBB looks the name up, +0x11C..+0x147 build the index)*. |"),
    # MM.CV-10: op 0x2C stores the score at +0x32A when it is at least the value held.
    (FEF, "scanned for match/`0xFF`; match advances cursor `+0x32A`. |",
     "scanned for match/`0xFF`; ~~match advances cursor `+0x32A`~~ the match score is stored at `+0x32A` when it is "
     "at least the rank held there " + T + "`00417DE0`+0x92 `movsx eax, word ptr [r8 + 0x32a]`, +0x9A `cmp r11d, eax`, "
     "+0xA3 the store)*. |"),
    # MM.CV-11: the leaf setters' map and index form.
    (FEF, "leaf setters (`f32[obj + nodeKey*0x10 + chIdx*4 + {0x190,0x1B0,0x1D0}]`).",
     "leaf setters (~~`f32[obj + nodeKey*0x10 + chIdx*4 + {0x190,0x1B0,0x1D0}]`~~ `f32[node + group*0x10 + chIdx*4 + "
     "base]` on each node of the `+0x278` chain, base `+0x190` for `00418650`, `+0x1D0` for `004186A0` and `+0x1B0` "
     "for `00418700` " + T + "`00418650`+0x20, `004186A0`+0x30, `00418700`+0x20)*)."),
    # MM.CV-12: 0041C260 strides the 0x290 bone records, not the node rows.
    (FEF, "`container+0x54` (`@FMN`); `0041C260`'s snapshot arm copies the eight dwords\n`row+0xF0..0x10C` to `+0x130..+0x14C`.",
     "`container+0x54` (`@FMN`); `0041C260`'s snapshot arm copies the eight dwords\n~~`row+0xF0..0x10C`~~ "
     "`+0xF0..+0x10C` of a `0x290`-stride bone record, not of this node row, to `+0x130..+0x14C` " + T + "`0041C260`"
     "+0x85 `imul rbx, rax, 0x290`)*."),
    # MM.CV-14: @FMW +0x0C is the channel count and +0x30/+0x34/+0x40 are header fields.
    (FEF, "Header `{'@FMW', kind 0, entryLen, u32 +0x0C = 0}`, `char[0x10]` name at `+0x10`\n"
          "(only half the name field — the u16 stream starts at `+0x20`). Exactly `1:1`",
     "Header `{'@FMW', kind 0, entryLen, ~~u32 +0x0C = 0~~ u32 +0x0C = channel count}`, `char[0x10]` name at `+0x10`\n"
     "~~(only half the name field — the u16 stream starts at `+0x20`)~~ (header fields follow at `+0x30`, `+0x34` and "
     "the u16 table at `+0x40` " + T + "`00409170`+0x7 `cmp edx, dword ptr [rcx + 0xc]`, +0xF `movzx eax, word ptr "
     "[rcx + rax*2 + 0x40]`; `0041B650`+0x16 `cmp dword ptr [rdx + 0x34], 1`)*). Exactly `1:1`"),

    # MM.CV-15: the mode byte is forced to 0 while 02B59D68 is ZERO.
    (OSC, "12). While it is set, section 3's mode byte is forced to 0 (the light stage) for records whose byte `+7` is set, and the",
     "12). ~~While it is set, section 3's mode byte is forced to 0~~ While it is clear, section 3's mode byte is forced "
     "to 0 " + T + "`0040ACF0`+0x23A `cmp byte ptr [rdi + 7], r15b`, +0x240 `cmp dword ptr [02B59D68], r15d` / `jne`, "
     "+0x249 `xor esi, esi`; `r15d` is zero)* (the light stage) for records whose byte `+7` is set, and the"),
    # MM.CV-16: the scope-open runs for modes 0 and 2.
    (OSC, "| `01FD4A90` | `.data` ptr | shared table stored to `02CA43C0` by mode-1/0 arms |",
     "| `01FD4A90` | `.data` ptr | shared table stored to `02CA43C0` by ~~mode-1/0~~ mode-0/2 arms " + T + "`0040ACF0`"
     "+0x270 `cmp esi, 1` skips the store at +0x287)* |"),
    # MM.CV-21: 0040AA20 is the per-frame wind phase tick, not a parameter setup.
    (OSC, "| `0040AA20` / `0040AAD0` | param setup | ◐ call shape |",
     "| `0040AA20` / `0040AAD0` | ~~param setup~~ wind phase tick / preset setter " + T + "`0040AA20`+0x6..+0x7F "
     "advances `+0x20` by `+0x24` while `02CA4390` is set and reseeds on the wrap; `0040AAD0` stores the preset)* | ◐ "
     "call shape |"),
    # MM.CV-22: the wind globals are six floats, three bytes and a dword.
    (OSC, "| `02CA4380`–`02CA439C` | `.data` f32 ×4-ish |",
     "| `02CA4380`–`02CA439C` | `.data` ~~f32 ×4-ish~~ six f32 (`80`/`84`/`88`/`8C`/`98`/`9C`), bytes `90`–`92`, dword "
     "`94` " + T + "`0040B3B0`+0x0 byte store, +0x6F dword store; `0040AAD0`+0x2A and +0x31 byte stores)* |"),
    (POSE, "reseeded from `003D8E50` random draws over the `02CA4380`/`02CA4398` ranges",
     "reseeded from `003D8E50` random draws ~~over the `02CA4380`/`02CA4398` ranges~~ over the ranges `02CA439C` / "
     "`02CA4384` added to the bases `02CA4398` / `02CA4380` " + T + "`0040AA20`+0x50..+0x7F)*"),

    # PP.CV-1 / PP.CV-2: step 7's lens is the constant 35.0 at 008F312C, not cfg+0x2C.
    (CS, "| `+0x2C` | `+0x120` | the `35.0` both loaders pass — the lens length step 7 divides by 1000 |",
     "| `+0x2C` | `+0x120` | the `35.0` both loaders pass ~~— the lens length step 7 divides by 1000~~; step 7 does not "
     "read it: its lens is the constant `35.0` at `008F312C`, and it passes `cfg+0x21`, `+0x30` and `+0x34` too " + T +
     "`00193DA0`+0x150 `movss xmm0, dword ptr [008F312C]`; `00193DA0`+0x126..+0x146 the other arguments)* |"),
    # PP.CV-3: 006CC1F0 copies 0x40 bytes into its own +0x28..+0x67.
    (CAT, "| `&cfg+0x9C`: its contents land in two 16-byte stores at `+0x28`/`+0x38` of an object `006CC1F0` resolves "
          "through `006DB900`/`006DB8C0` |",
     "| `&cfg+0x9C`: its contents land in ~~two 16-byte stores at `+0x28`/`+0x38` of an object `006CC1F0` resolves "
     "through `006DB900`/`006DB8C0`~~ four 16-byte stores at `+0x28`..`+0x58` of the receiver itself, which also "
     "clears byte `+0x24`; `006DB900`/`006DB8C0` run first only while that byte is clear " + T + "`006CC1F0`+0xA, "
     "+0x3D..+0x5C)* |"),
    # PP.CV-4: the catalogue is built lazily by the post-process callback.
    (CAT, "It runs once, at start-up. It loads a compiled shader file,",
     "It runs once, ~~at start-up~~ on the first frame the post-process command runs " + T + "`00193DA0`+0x31..+0x48 "
     "calls create only when `0065E5B0` reports the library absent; UQ-226)*. It loads a compiled shader file,"),
    (CAT, "start-up / device init\n",
     "start-up / device init   " + C + "the first post-processed frame: 00193DA0+0x31..+0x48 (UQ-226)\n"),
    # PP.CV-5: each counted variant of a 0072DCF0 site carries 22 suffix handles.
    (CAT, "registers **25** handles under one name — the `_Sn` suffix is a family of shader variants, and the",
     "registers ~~**25** handles~~ **25 × 22 = 550** handles under one name " + T + FIXUP + "; the handle slots of "
     "`ppfx-handle-layout.tsv` step `0x898` bytes from `0xDB60` to `0xE3F8`)* — the `_Sn` suffix is a family of shader "
     "variants, and the"),
    (CAT, "That registers **1,172 handles** in all, and every site's count resolves.",
     "That ~~registers **1,172 handles** in all~~ names 1,172 counted variants; the 640 of them at `0072DCF0`'s 65 "
     "sites carry 22 handles each, so the two helpers register 14,612 handles " + T + FIXUP + ")*, and every site's "
     "count resolves."),
    # PP.CV-10: 0078A120 is IGPUEffect::CreateEffect.
    (CAT, "| `0078A120` | — | 273 B | `IGPUEffect::CreateEffectFromFile` wrapper; called once |",
     "| `0078A120` | — | 273 B | ~~`IGPUEffect::CreateEffectFromFile` wrapper~~ `IGPUEffect::CreateEffect` " + T +
     "`0078A120`+0xEA logs `IGPUEffect::CreateEffect()`; `0078A240`+0x109 is the `CreateEffectFromFile` string)*; "
     "called once |"),
    (CAT, "        -> 0078A120                CreateEffectFromFile(\"<base>\" + \"_LUMINANCE_REMAP_S1.pso\")\n",
     "        -> 0078A120                CreateEffectFromFile(\"<base>\" + \"_LUMINANCE_REMAP_S1.pso\")   " + C +
     "0078A120 is IGPUEffect::CreateEffect (its own log string at 0078A120+0xEA)\n"),
    (CP, "`IGPUEffect::CreateEffectFromFile` via `0078A120` is called once",
     "~~`IGPUEffect::CreateEffectFromFile`~~ `IGPUEffect::CreateEffect` " + T + "`0078A120`+0xEA logs that name)* via "
     "`0078A120` is called once"),
    (CP, "   0078A120   IGPUEffect::CreateEffectFromFile wrapper, once\n",
     "   0078A120   IGPUEffect::CreateEffectFromFile wrapper, once   " + C + "IGPUEffect::CreateEffect "
     "(0078A120+0xEA)\n"),
    (CP, "    hr = CreateEffectFromFile(device, <name>, \"_LUMINANCE_REMAP_S1.pso\", 0)   # via 0078A120\n",
     "    hr = CreateEffectFromFile(device, <name>, \"_LUMINANCE_REMAP_S1.pso\", 0)   # via 0078A120   # " + C +
     "0078A120 is IGPUEffect::CreateEffect (0078A120+0xEA)\n"),
    (CP, "The two helpers that take a count (`0072DCF0`, 65 sites; `0072EB20`, 26) register *n* handles under\none name,",
     "The two helpers that take a count (`0072DCF0`, 65 sites; `0072EB20`, 26) register ~~*n* handles~~ *n* handles, "
     "*n* × 22 for `0072DCF0` " + T + FIXUP + ")*, under\none name,"),
    # PP.CV-6: the highest store is r14 + 0x221D0, i.e. this + 0x221D8.
    (PI, "> **The object is at least `0x220E0` bytes.** The highest displacement `CreateEffect` touches is\n"
         "> `+0x220DC`, and that is through `r14 = rcx + 8`, so the allocation is at least `0x220E4` from\n"
         "> `rcx`.",
     "> **The object is at least ~~`0x220E0`~~ `0x221DC` bytes.** The highest displacement `CreateEffect` touches is\n"
     "> ~~`+0x220DC`~~ `+0x221D0`, and that is through `r14 = rcx + 8`, so the allocation is at least ~~`0x220E4`~~ "
     "`0x221DC` from\n> `rcx` " + T + "`0072A320`+0x176 `lea r14, [rbx + 8]`, +0x34B8 `mov dword ptr [r14 + 0x221d0], "
     "eax`; the catalogue's `+0x221D8`)*."),

    # PP.CV-11: the scene keys are JSON keys read by the loaders' lookups.
    (RR, "These follow the `m<Name>` member convention and are **the embedded strings that Phyre\n"
         "reflection's `PClassDataMember` holds** — the reflection document",
     "These follow the `m<Name>` member convention and are ~~**the embedded strings that Phyre~~\n"
     "~~reflection's `PClassDataMember` holds**~~ JSON keys: the strings checked are reached only by code `lea`s into "
     "the scene loaders' key lookups " + T + "`001C3D50`+0x556 `lea rdx, [008FA4D0]` then +0x560 `call 001C51D0`; "
     "W-3 below)* — the reflection document"),
    # PP.CV-13: mDofSpecialApertureFnumber is read only by the map loader.
    (RR, "  mDofSpecialApertureFnumber alternate aperture (cutscene?)\n",
     "  mDofSpecialApertureFnumber alternate aperture (cutscene?)   " + C + "a map key: its only readers are "
     "001C7940+0x171 and +0x188, the map loader\n"),

    # PP.CV-9: 00194250 has five call sites in four functions.
    (L, "`+0x120` receives the constant `35.0f` at `008F312C`. The two callers are `001C3D50`'s PresetDof arm",
     "`+0x120` receives the constant `35.0f` at `008F312C`. The ~~two~~ callers are four functions, five sites " + T +
     "`001C3D50`+0x499 and +0x551, `001C5750`+0x177, `001C7940`+0x24E, `001F38B0`+0x45)*: `001C3D50`'s PresetDof arm"),

    # CM.CV-1: the flag is 022BDD5C and the colour 022BDD58..5B (002EFE10).
    (SF, "**The colour** (`002EFBD5`–`002EFC6F`): when the one-shot byte `022BDD58` is set, the four bytes\n"
         "`022BDD59`–`022BDD5C` are copied in",
     "**The colour** (`002EFBD5`–`002EFC6F`): when the one-shot byte ~~`022BDD58`~~ `022BDD5C` is set, the four bytes\n"
     "~~`022BDD59`–`022BDD5C`~~ `022BDD58`–`022BDD5B` " + T + "`002EFE10`+0x0 `mov byte ptr [022BDD5C], 1`, +0x7.."
     "+0x1A the four colour bytes; `002EFA70`+0x165 tests `022BDD5C`)* are copied in"),
    (SF, "| `002EFE10(colour…)` | arm the one-shot colour override at `022BDD58` |",
     "| `002EFE10(colour…)` | arm the one-shot colour override ~~at `022BDD58`~~: flag `022BDD5C`, colour "
     "`022BDD58`–`022BDD5B` " + T + "`002EFE10`+0x0..+0x1A)* |"),
    # CM.CV-2 / CM.CV-3: the descriptor handed to 00375900 is 0x68 bytes; +9 and +0xB come from 022BDEB4/022BDD5D
    #     and 022BDEB0.
    (SF, "| `+0x08`–`+0x2F` | the 0x28-byte descriptor handed to `00375900`: `+8 = 1`, `+9` two nibbles from `022BDD57` "
         "and `022BDD5D` (`002EFC85`–`002EFCC9`), `+0xA = 1`, `+0xB` = byte `022BDD5B`,",
     "| `+0x08`–`+0x2F` | the ~~0x28-byte~~ descriptor handed to `00375900`, which copies `0x68` bytes from `+0x08`, "
     "into the next records " + T + "`00375900`+0xC9..+0x101)*: `+8 = 1`, `+9` two nibbles from ~~`022BDD57`~~ "
     "`022BDEB4` (low) and `022BDD5D` (high) (`002EFC85`–`002EFCC9`), `+0xA = 1`, `+0xB` = byte ~~`022BDD5B`~~ "
     "`022BDEB0` " + T + "`002EFA70`+0x20B and +0x225 for `+0xB`, +0x215 and +0x244 for `+9`)*,"),
    # 002EFA70 and 002EFA20 reset 022BDD5D, not 022BDD56.
    (SF, "The globals `022BDD56 = 3`, `022BDEB0 = 0`, `022BDEB4 = 6`",
     "The globals ~~`022BDD56 = 3`~~ `022BDD5D = 3`, `022BDEB0 = 0`, `022BDEB4 = 6` " + T + "`002EFA70`+0x284 "
     "`mov byte ptr [022BDD5D], 3`)*"),
    (SF, "| `002EFA20()` | reset: state byte `022BDD56 = 3`,",
     "| `002EFA20()` | reset: state byte ~~`022BDD56 = 3`~~ `022BDD5D = 3` " + T + "`002EFA20`+0x2 `mov byte ptr "
     "[022BDD5D], 3`)*,"),
    # CM.CV-7: +3 is the fade-out lead and +4 the fade-out length.
    (SF, "row  +0  id            +1 fadeInStart   +2 fadeInLength   +3 fadeOutLength   +4 fadeOutLead   +7 flags "
         "(bit 0 white in, bit 1 white out)\n",
     "row  +0  id            +1 fadeInStart   +2 fadeInLength   +3 fadeOutLength   +4 fadeOutLead   +7 flags "
     "(bit 0 white in, bit 1 white out)   " + C + "+3 is fadeOutLead and +4 fadeOutLength: 0037DEA0+0x7F gates "
     "the fade-out on byte +4, and +0x8E subtracts byte +3 from the length for the frame count\n"),
    # CM.CV-6: flags 1 is bit 0, the fade-in's white argument.
    (SF, "ids 17, 19, 21 fade to white on\nthe way out (flags 1), 26, 35, 43",
     "ids 17, 19, 21 fade to white on\nthe way ~~out~~ in " + T + "flags 1 is bit 0, the fade-in's white argument, "
     "`0037DEA0`+0x46..+0x4E)* (flags 1), 26, 35, 43"),
    # CM.CV-8: the start copies the two words into its descriptor before resetting them.
    (SF, "to black in zero frames** — the instant cut a skipped scene shows — with kind 6 and a wait of\n"
         "`0xFF` recorded in the two words for whoever resumes the scene.",
     "to black in zero frames** — the instant cut a skipped scene shows — with kind 6 and a wait of\n"
     "`0xFF` ~~recorded in the two words for whoever resumes the scene.~~ in the two words, which this same start "
     "copies into its descriptor before resetting them to 6 and 0 " + T + "`002EFA70`+0x20B and +0x215 read them, "
     "+0x284..+0x295 reset them)*."),
    # CM.CV-11: 002DEE50 / 002DEDE0 drive the music track, not a fade layer.
    (SF, "follow-up. The write is the layer's armed/visible flag; the counter gate is \"no fade state\nloaded\".",
     "follow-up. ~~The write is the layer's armed/visible flag; the counter gate is \"no fade state~~\n~~loaded\".~~ "
     "The call is a music volume fade: `0215EF44` is the current track, and `001DBCA0` hands the track, the frame "
     "count and the volume to the sound side, which divides them by `60.0` and `127.0` " + T + "`002DEE50`+0x15 `jmp "
     "001DBCA0`; `00222B70`+0x3A and +0x42 `divss`; the mode machine's state 9 calls it with `0x5A` frames and volume "
     "0)*."),
    (SF, "`002DEDE0` (80 B) maintains the fade-layer singleton\n",
     "`002DEDE0` (80 B) maintains the ~~fade-layer singleton~~ current music track " + T + "the same sound-side chain "
     "as `002DEE50`)*\n"),
    # CM.CV-10: the issued markers are masks 8 and 0x10, bits 3 and 4.
    (SF, "with `+0xF0` bit 8 clear and the `[rbp+2]`/`[rbp+1]` window reached by `[rsi+0x14]`, it fires `002EFE40(5)` "
         "then `002EFA70(0, edi, 1, [rbp+7]&1)` and sets bit 8; the mirror block under bit `0x10` does",
     "with `+0xF0` ~~bit 8~~ bit 3 (mask `8`) clear and the `[rbp+2]`/`[rbp+1]` window reached by `[rsi+0x14]`, it "
     "fires `002EFE40(5)` then `002EFA70(0, edi, 1, [rbp+7]&1)` and sets ~~bit 8~~ that bit; the mirror block under "
     "~~bit `0x10`~~ bit 4 (mask `0x10`) " + T + "`0037DEA0`+0x1D `test byte ptr [rcx + 0xf0], 8`, +0x6F `or dword "
     "ptr [rsi + 0xf0], 8`, +0x76 and +0xD3 for `0x10`)* does"),

    # CM.CV-12: 0x4B7FFBFF is 16,776,191.0.
    (PTS, "map z between the constants `1024.0` and `16,777,215.0` (`0x44800000` / `0x4B7FFBFF` at `+0x4C` /",
     "map z between the constants `1024.0` and ~~`16,777,215.0`~~ `16,776,191.0` " + T + "`004679C0`+0x17 `mov dword "
     "ptr [rcx + 0x50], 0x4b7ffbff`; `16,777,215.0` would be `0x4B7FFFFF`)* (`0x44800000` / `0x4B7FFBFF` at `+0x4C` /"),
    # CM.CV-13: 02AED5F0 is written by the camera update.
    (PTS, "    stash   = *(vec4 *)02AED5F0;            /* a constant, §4 */\n",
     "    stash   = *(vec4 *)02AED5F0;            /* a constant, §4 */   /* " + C + "not a constant: the camera "
     "update writes it (003820C0+0x3A0) */\n"),
    (PTS, "| `02AED5F0` | the stashed constant | 16 B |",
     "| `02AED5F0` | the stashed ~~constant~~ camera vector " + T + "`003820C0`+0x3A0 writes it)* | 16 B |"),

    # CM.CV-14: the third factor is the frame-rate step [01DFE0BC], and the source is 02B4E4B0.
    (P, "        step = *(float*)0x02B4E4B0 * c->rate * 1.0f;\n",
     "        step = *(float*)0x02B4E4B0 * c->rate * 1.0f;   // " + C + "the third factor is float [01DFE0BC] "
     "(003DA050+0xB0), 1.0 in the image and 0.5 on the 60 fps arm\n"),
    (P, "`float[0264E4B0] × rate × float[01DFE0BC]` (`003DA0F3`–`003DA100`)",
     "~~`float[0264E4B0] × rate × float[01DFE0BC]`~~ `float[02B4E4B0] × rate × float[01DFE0BC]` " + T + "`003DA050`"
     "+0xA3 `movss xmm1, dword ptr [02B4E4B0]`)* (`003DA0F3`–`003DA100`)"),
    # CM.CV-15: 003DA050 does not call 00257AD0.
    (P, "`00257AD0` is the same playhead evaluator `003DA050`'s track loop\ncalls — the camera-shot and attachment "
        "paths share it.",
     "~~`00257AD0` is the same playhead evaluator `003DA050`'s track loop~~\n~~calls — the camera-shot and attachment "
     "paths share it.~~ `00257AD0` finds the Nth kind-3 member and is not called by `003DA050` " + T + "`003DA050`"
     "+0xDC calls `00257A00`; `00257AD0`+0x3A `cmp eax, 3`)*."),
    # CM.CV-16: +0x16C/+0x170 are the cached angles.
    (P, "+0x169 u8[15]    unread169     not observed accessed; between the running array tail and stream\n",
     "+0x169 u8[15]    unread169     not observed accessed; between the running array tail and stream   " + C +
     "+0x16C / +0x170 are the cached yaw / pitch (00256960+0x19E, +0x305, +0x30D; 00256CA0+0x199, +0x287; section 7a)\n"),

    # CM.CV-19: 90 populated slots among the first 98.
    (MH, "the 45 pairs occupy 92 of\n",
     "the 45 pairs occupy ~~92 of~~ 90 " + T + "the 98 qwords from `01ECB4D0` hold 90 non-null pointers)* of\n"),
    (MH, "(us 36 / in 8 / jp 1) in 92 populated slots, exactly as §3 says.",
     "(us 36 / in 8 / jp 1) in ~~92~~ 90 populated slots " + T + "slots 0-97, less the NULLs at 76-81 and 92-93)*, "
     "exactly as §3 says."),
    # CM.CV-20: 0067A9B0 tears the sub-record down.
    (MH, "zero, `0067A9B0(rcx + 0x678)`\ninitializes the trailing\n",
     "zero, `0067A9B0(rcx + 0x678)`\n~~initializes~~ tears down " + T + "state 1 to 3, `0067A9B0`+0x12..+0x18)* the "
     "trailing\n"),

    # CM.CV-21: (W - H) / W is 0 for every W > H.
    (AF, "`(W - H) / W` truncates to **0** for everything up to `W = 2H`, so `+0x0C`",
     "`(W - H) / W` truncates to **0** ~~for everything up to `W = 2H`~~ for every `W > H`, the whole branch " + T +
     "`001DDAC0`+0xBD `div r10d` with `0 < W - H < W`)*, so `+0x0C`"),

    # CM.CV-22: the eight elements are replaced only under the device override.
    (FADE, "copies the working camera's view matrix from `02AED580` to `02AEDE70` and adjusts eight of its elements, and",
     "copies the working camera's view matrix from `02AED580` to `02AEDE70` and ~~adjusts eight of its elements~~, "
     "only when the device override predicate `00181DD0` is true, replaces eight of its elements " + T + "`003820C0`"
     "+0x5BF `call 00181DD0`, +0x5CE `je` past the eight stores)*, and"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
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
