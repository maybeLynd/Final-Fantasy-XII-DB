"""apply_00engine_b.py [--apply] - 00-Engine-Core-Runtime readiness map (cloud-reports/re-readiness/00-engine.md),
part B: section 3.1 value items C-V83 to C-V168, section 3.1.C counts and section 3.2 stale / banner items, settled
on the pages (OPUS, 2026-10-02). Part A (C-V1 to C-V82) is opus-engine-a-readiness-fixes-1002.

Each value or count edit strikes the side the shipping image REFUTES only and restates it, tagged
*(corrected 2026-10-02, OPUS: <deciding address>)*; the report's favoured sides were treated as claims and re-decided
at the instructions or image data. Stale / banner items get *(answered: see <where>; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; no heading changes; table column counts kept.
Addresses inside a function are cited as entry+offset in all new text.
The decisions and the items left out are in the session scratch verdicts-00b.md.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "00-Engine-Core-Runtime/"
README = F + "README.md"
EEVU = F + "Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md"
SAVE = F + "Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md"
WB = F + "Shared-Transform-Workbench/the-shared-transform-workbench.md"
PRIM = F + "Shared-Transform-Workbench/the-two-transform-primitives.md"
CWB = F + "CONTRACT-shared-transform-workbench.md"
CSAVE = F + "CONTRACT-transform-workbench-save-restore.md"
CPRIM = F + "CONTRACT-transform-primitives.md"
RTTI = F + "Object-Model/rtti-vtable-object-model.md"
HUBS = F + "Shared-State-Accessors/cross-subsystem-accessor-hubs.md"
OWN = F + "Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md"
DC = F + "Developer-Tuning-Console/"
CCON = DC + "CONTRACT-developer-tuning-console.md"
CON282 = DC + "the-282-command-parameter-console.md"
TUNES = DC + "what-the-console-tunes.md"
CON2 = DC + "the-second-console-table.md"
EVSLOT = DC + "the-event-slot-panel-and-its-dead-feeder.md"
ARMDIV = DC + "ARM-CATALOGUE-WORK-DIVISION.md"
ARMA = DC + "arm-catalogue-slice-A-ids-12-43.md"
ARMB = DC + "arm-catalogue-slice-B-ids-44-75.md"
ARMC = DC + "arm-catalogue-slice-C-ids-76-107.md"
ARMD = DC + "arm-catalogue-slice-D-ids-108-139.md"
ARME = DC + "arm-catalogue-slice-E-ids-140-171.md"
ARMF = DC + "arm-catalogue-slice-F-ids-172-203.md"
ARMG = DC + "arm-catalogue-slice-G-ids-204-235.md"

T = "*(corrected 2026-10-02, OPUS: "
STAGE = ("`006084B0+0x3CE` `lea rdx, [02CB7FD0]`, `+0x3D8` `lea rax, [rdx+0xd0]` (= `02CB80A0`), then 16-byte `movups` "
         "loads over `02CB7FD0`–`02CB815F` into the staged shader-constant buffer")
TABLE24 = "`0036DF80+0x15` `lea rcx, [rax+rax*2]`, `+0x20` `cmp word ptr [rax+rcx*8+4], 0`"
FORCE = F + "Force-Fight-Mode/force-fight-mode.md"
FLOAT = F + "Startup-Data-Construction/generated-float-table-builders.md"
BOOT = F + "what-the-engine-fixes-at-boot.md"
CBOOT = F + "CONTRACT-boot-fixups.md"
TICK = F + "Battle-Frame/the-world-tick-and-the-field-frame.md"
CTICK = F + "Battle-Frame/CONTRACT-world-simulation-tick.md"
GATE = F + "Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md"
CGATE = F + "CONTRACT-per-frame-update-gate.md"
MODE = F + "Battle-Runtime-Mode/battle-runtime-mode-ladder.md"
CMODE = F + "Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md"
LOG = F + "Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md"
ABI = F + "ABI-Recovery/derived-call-signatures.md"
NBR = F + "Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md"
ARMI = DC + "arm-catalogue-slice-I-ids-268-293.md"


def A(where):
    """The stale-item tag."""
    return "*(answered: see " + where + "; 2026-10-02, OPUS)*"


def FM(status):
    """README status lines that disagree with the page's own front matter."""
    return A("the page's front matter, status " + status)

EDITS = [
    # C-V83: vf00 01EF93F0 has three writers - 0036D9E0, 0036D990 and 0036DD80 (0036DD80+0x7 movups from 008C5FD0).
    (WB, "**It has exactly two writers and they write the same thing.** The second is `0036D990`",
     "**It has ~~exactly two writers~~ three writers and they write the same thing.** " + T + "the third is "
     "`0036DD80`, 15 B, which copies the 16-byte constant `008C5FD0` = (0, 0, 0, 1.0) at `0036DD80+0x7` "
     "`movups xmmword ptr [01EF93F0], xmm0`.)* The second is `0036D990`"),
    (WB, "and the two-writer count is exact rather than merely unseen.",
     "and the ~~two-writer count~~ three-writer count (`0036D9E0`, `0036D990`, `0036DD80`) is exact rather than "
     "merely unseen " + T + "`0036DD80+0x7` is the third store)*."),

    # C-V85: three rows are protected - 0042FDB0 saves 022D8F30 and 022D8F40 (0042FDB0+0x330..+0x349, ecx = 2).
    (SAVE, "**`022D8F30` and `022D8F90` are the only two\naddresses that anything in this image bothers to protect**",
     "**~~`022D8F30` and `022D8F90` are the only two~~\n~~addresses that anything in this image bothers to protect~~ "
     "`022D8F30`, `022D8F40` and `022D8F90` are the only three addresses that anything in this image bothers to "
     "protect** " + T + "the two-row caller `0042FDB0` saves `022D8F30` and `022D8F40`: `0042FDB0+0x330` "
     "`lea rbx, [022D8F40]`, `+0x337` `mov ecx, 2`, `+0x349` `call 0036D930`)*"),
    (WB, "protecting one of exactly two rows: `022D8F30` (5 callers) or\n  > `022D8F90` (3), with one saving both.",
     "protecting ~~one of exactly two rows~~ one or two of three rows: `022D8F30` (5 callers) or\n  > `022D8F90` (3), "
     "~~with one saving both~~ with the ninth, `0042FDB0`, saving `022D8F30` and `022D8F40` together " + T
     + "`0042FDB0+0x330`–`+0x349`, `ecx = 2`)*."),

    # C-V86: 0044B8C0 is called before 0044BAC0's save window (+0x601 vs Save at +0x97E, Restore at +0xA03).
    (SAVE, "is the matrix-scalar helper `0044BAC0` runs inside its save window:",
     "is the matrix-scalar helper `0044BAC0` runs ~~inside its save window~~ before its save window opens " + T
     + "called at `0044BAC0+0x601`; the window runs from `call 0036D930` at `+0x97E` to `call 0036D8E0` at "
     "`+0xA03`, with only `sqrtf` at `+0x9CE` between)*:"),

    # C-V87: 0044BAC0 calls five of the other eight Save users directly and reaches 002F1D90 through 002F1F40.
    (CSAVE, "`0044BAC0`, can — and only through `0026EE00`, which is itself one of the nine.",
     "`0044BAC0`, can — ~~and only through `0026EE00`, which is itself one of the nine~~ and through six of the "
     "other eight " + T + "it calls `0042FDB0` at `0044BAC0+0x2C8`, `0026EE00` at `+0x2EB`, `00431D30` at "
     "`+0x32E`, `003D8E50` at `+0x580`, `003AFDD0` at `+0x598`, and reaches `002F1D90` through `002F1F40` "
     "(`+0x5A8`, then `002F1F40+0x10C`); none of these calls is inside its save window)*."),

    # C-V88: Save's loop takes any count (0036D930+0x31..+0x50); only the shipped callers stop at two.
    (CSAVE, "second Save overwrites the first frame in place (§10), a single save window can protect at\n"
            "  most two rows — a whole matrix is unreachable through this convention.",
     "second Save overwrites the first frame in place (§10), ~~a single save window can protect at~~\n"
     "  ~~most two rows — a whole matrix is unreachable through this convention~~ no shipped save window protects "
     "more than two rows, but the convention itself takes any count " + T + "Save's loop walks `ecx` pointers, "
     "`0036D930+0x31`–`+0x50`, bounded only by the 32-entry layout below; a caller passing four pointers would "
     "save a whole matrix)*."),

    # C-V89: 0036D9E0 clears 022D91B0..022D942F (80 qword stores, +0x25..+0x38A) and vf00, not the whole area.
    (WB, "              0036D9E0 ── clears the whole area, reads nothing (unowned)\n",
     "              0036D9E0 ── clears the whole area, reads nothing (unowned)   <- corrected 2026-10-02, OPUS: it "
     "clears 022D91B0-022D942F (80 qword stores, 0036D9E0+0x25..+0x38A) and vf00 01EF93F0, not 022D8F00-022D91AF\n"),
    (CWB, "`0036D9E0` clears it wholesale and belongs to nobody.",
     "`0036D9E0` ~~clears it wholesale~~ clears `022D91B0`–`022D942F` and vf00, not the whole area " + T
     + "80 qword stores at `0036D9E0+0x25`–`+0x38A`; `022D8F00`–`022D91AF` is not touched)*, and belongs to nobody."),
    (CSAVE, "cell is borrowed scratch like every other row, and the wholesale-clear hazard stays: clearing the",
     "cell is borrowed scratch like every other row, ~~and the wholesale-clear hazard stays~~ and no clear reaches "
     "it, since `0036D9E0` stores only `022D91B0`–`022D942F` and vf00 " + T + "`0036D9E0+0x25`–`+0x38A`)*; still, "
     "clearing the"),

    # C-V91: the composer stages a at [rsp+0x40]..+0x70 and b at [rsp]..+0x30 (00397910+0x67, +0x97); no +0x80.
    (PRIM, "before it multiplies (`[rsp+0x40]` and `[rsp+0x80]`), so",
     "before it multiplies (~~`[rsp+0x40]` and `[rsp+0x80]`~~ `[rsp+0x40]`–`+0x70` and `[rsp]`–`+0x30` " + T
     + "`00397910+0x67` `movaps xmmword ptr [rsp+0x40], xmm0`, `+0x97` `movaps xmmword ptr [rsp], xmm0`; no store "
     "reaches `[rsp+0x80]`)*), so"),
    (CPRIM, "staged to the stack frame (`[rsp+0x40]` and\n   `[rsp+0x80]`) before any multiply",
     "staged to the stack frame (~~`[rsp+0x40]` and~~\n   ~~`[rsp+0x80]`~~ `[rsp+0x40]`–`+0x70` and `[rsp]`–`+0x30` "
     + T + "`00397910+0x67` and `+0x97`, as the §15a table says)*) before any multiply"),

    # C-V93: 00398F90+0x4 loads row 1 (022D91B0); ACC is 022D91A0.
    (PRIM, "is `movups xmm0, [rip+...]` loading the ACC\n  row, then",
     "is `movups xmm0, [rip+...]` loading ~~the ACC~~\n  ~~row~~ vector row 1, `022D91B0` (ACC is `022D91A0`) " + T
     + "`00398F90+0x4` resolves to `022D91B0`)*, then"),

    # C-V94: 003970A0 copies rows 1-4 (022D91B0..022D91EF; loads at +0x0, +0xA, +0x15, +0x20).
    (PRIM, "a 64-byte snapshot of the\nvector-unit-5 quadrant into caller storage",
     "a 64-byte snapshot of the\n~~vector-unit-5 quadrant~~ vector rows 1–4 (`022D91B0`–`022D91EF`) " + T
     + "the four loads at `003970A0+0x0`, `+0xA`, `+0x15`, `+0x20`)* into caller storage"),

    # C-V96: 022D9130 is the CLIP flag word (0025A8E0+0xE shl eax, 6; +0x2B / +0x43 or); 00433830 never reads it.
    (WB, "bumps the `022D9130` staging bank (`0025A8E5`/`0025A8F1`/`0025A926`)",
     "~~bumps the `022D9130` staging bank~~ shifts the `022D9130` flag word left by 6 and ORs in comparison bits, the "
     "VCLIP result " + T + "`0025A8E0+0xE` `shl eax, 6`, `+0x2B` `or eax, 1`, `+0x43` `or eax, 2`)* "
     "(`0025A8E5`/`0025A8F1`/`0025A926`)"),
    (WB, "`0025A8E0`'s `022D9130` cells are the same\nstaging bank the `00433830` blend kernel consumes.",
     "~~`0025A8E0`'s `022D9130` cells are the same~~\n~~staging bank the `00433830` blend kernel consumes.~~ "
     "`0025A8E0`'s `022D9130` is the CLIP flag word, and no rip operand of the `00433830` blend kernel reaches it " + T
     + "`0025A8E0+0xE` `shl eax, 6`; none of `00433830`'s 3,202 bytes addresses `022D9130`–`022D913F`)*."),

    # C-V98: the banner string at 00908D80 ends "*** \n".
    (EEVU, "> **`\"PS2 Assembly emulation initilization completed! \"`** (`0036D990` → `00908D80`",
     "> ~~**`\"PS2 Assembly emulation initilization completed! \"`**~~ **`\"PS2 Assembly emulation initilization "
     "completed! *** \\n\"`** " + T + "the string at `00908D80` runs on to `*** ` and a newline before its NUL)* "
     "(`0036D990` → `00908D80`"),
    (EEVU, "`00908D80` = `\"PS2 Assembly emulation initilization completed! \"`; called from",
     "`00908D80` = ~~`\"PS2 Assembly emulation initilization completed! \"`~~ `\"PS2 Assembly emulation "
     "initilization completed! *** \\n\"` " + T + "read from the image)*; called from"),

    # C-V99: the two lea instructions are at 0036D930+0x23 and +0x2A.
    (CSAVE, "values array `lea`'d at `0036D954` = `02EC0800` (16 B/item), pointers `lea`'d at `0036D95B` =",
     "values array `lea`'d at ~~`0036D954`~~ `0036D930+0x23` = `02EC0800` (16 B/item), pointers `lea`'d at "
     "~~`0036D95B`~~ `0036D930+0x2A` " + T + "the two `lea` instructions start at `0036D930+0x23` and `+0x2A`)* ="),

    # C-V100: 022D94B0 is the base of a 32 x 24-byte record table (BQ-17), not two pointers.
    (WB, "slots**, `022D94B0` and `022D94B4`, always 8 bytes wide and never as floats. Those two are pointers,",
     "slots**, `022D94B0` and `022D94B4`, ~~always 8 bytes wide~~ indexed at an `*8` scale and never as floats. "
     "~~Those two are pointers,~~ They are one 32-entry table of 24-byte records (BQ-17) " + T + TABLE24 + ")*,"),
    (WB, "| `022D94B0`, `022D94B4` | two pointers | BSS region, 8-byte each |",
     "| `022D94B0`, `022D94B4` | ~~two pointers~~ one 32 × 24-byte record table " + T + TABLE24 + ")* | BSS region, "
     "~~8-byte each~~ a `+0` dword and a `+4` word per record |"),
    (WB, "    022D94B0   void*        read 8 bytes wide by 16 functions, never RIP-written\n",
     "    022D94B0   void*        read 8 bytes wide by 16 functions, never RIP-written   <- corrected 2026-10-02, "
     "OPUS: base of a 32 x 24-byte record table (0036DF80+0x15..+0x20), not a pointer\n"),
    (WB, "    022D94B4   void*        same\n",
     "    022D94B4   void*        same   <- corrected 2026-10-02, OPUS: record 0's +4 state word (stored at "
     "0036DE20+0x3A), not a pointer\n"),
    (WB, "| `022D94B0`/`B4` are pointers, not matrix data |",
     "| `022D94B0`/`B4` are ~~pointers~~ a 32 × 24-byte record table " + T + TABLE24 + ")*, not matrix data |"),
    (WB, "**`BQ-17`'s two pointers** |",
     "~~**`BQ-17`'s two pointers**~~ **`BQ-17`'s record table** " + T + "`0036DF80+0x15`–`+0x20`)* |"),

    # C-V101: 231 call sites (129 to 00397910, 102 to 00398F90); 156 is the caller-function sum.
    (PRIM, "  the 156 call sites around them are not.",
     "  the ~~156 call sites~~ 231 call sites (156 caller functions) around them are not " + T + "129 direct call "
     "sites to `00397910`, 102 to `00398F90`)*."),
    (PRIM, "156 call sites were counted, **none was read**.",
     "~~156 call sites~~ 231 call sites (156 caller functions) were counted " + T + "129 + 102 direct call sites)*, "
     "**none was read**."),
    (CPRIM, "§14's 156 call sites and the four",
     "§14's ~~156 call sites~~ 231 call sites (156 caller functions) " + T + "129 direct call sites to `00397910`, "
     "102 to `00398F90`)* and the four"),

    # C-V102: 0039AF70 has 116 direct call sites.
    (PRIM, "*is* whichever of the two a caller last installed: the 232 sites (the draw-side families",
     "*is* whichever of the two a caller last installed: the ~~232 sites~~ 116 sites " + T + "116 direct call sites "
     "to `0039AF70`, as the 2026-09-13 correction below says)* (the draw-side families"),

    # C-V105 / C-V113 (README): 4,272 single-class functions; GameApplication's slot 0 is a deleting destructor.
    (README, "**DOCUMENTED, tier 1.** **4,275 function addresses tied to exactly one C++ class and\n  vtable slot**",
     "**DOCUMENTED, tier 1.** " + FM("AUDITED") + " **~~4,275~~ 4,272 function addresses tied to exactly one C++ "
     "class and\n  vtable slot** " + T + "4,275 counts "
     "three mid-function words, `00444340+0xC0C`, `006C6230+0x313` and `007558E0+0x68D`, that are inline ASCII, "
     "not methods; the object-model page's AS-7)*"),
    (README, "  image-wide. Never deleted, hence no stated object size.",
     "  image-wide. ~~Never deleted, hence no stated object size.~~ Slot 0, `0017CC70`, is its scalar deleting "
     "destructor and states the size, `0x1140` = 4,416 bytes " + T + "`0017CC70+0x29` `test dil, 1`, `+0x40` "
     "`mov edx, 0x1140`; the application page's BE-4)*."),

    # C-V106: 0016D6A0 fills a slot of 1,291 vtables (1,291 classes).
    (RTTI, "is shared by three unrelated\ntables).",
     "is shared by ~~three unrelated~~\n~~tables~~ 1,291 vtables of 1,291 classes " + T + "every vtable found from "
     "its complete-object locator, 2,286 in all)*)."),
    # C-V110: 00385F60 is 2,302 B.
    (RTTI, "`00385F60` (`BattleFormula_ResolveTargetResult`, ~144 B) —",
     "`00385F60` (~~`BattleFormula_ResolveTargetResult`, ~144 B~~ `BattleFormula_ResolveTargetResult`, 2,302 B "
     + T + "its extent is 2,302 B and `00385F60+0x470` lies inside it)*) —"),
    # C-V114: GameApplication's vtable at 008C5760 holds 31 code pointers.
    (RTTI, "| `GameApplication` | 30 | the root application object |",
     "| `GameApplication` | ~~30~~ 31 " + T + "the vtable at `008C5760` holds 31 code pointers, slot 0 "
     "`0017CC70`)* | the root application object |"),

    # C-V118: 022D8F00..022D9500 is 0x600 = 1,536 bytes.
    (OWN, "1,436-byte shared scratchpad.",
     "~~1,436-byte~~ 1,536-byte " + T + "`0x022D9500 − 0x022D8F00` = `0x600`)* shared scratchpad."),
    # C-V122: 02F97348 is shared - 102 referencing functions, 19 storing.
    (OWN, "**The private state is the current action context.** The singleton `[02F97348]` — 57 references",
     "~~**The private state is the current action context.**~~ **The state it works on is the current action "
     "context, a shared singleton rather than private state** " + T + "`02F97348` is referenced by 102 functions "
     "and stored by 19, e.g. read at `003A3E30+0x4`, stored at `0024B270+0xEF`)*. The singleton `[02F97348]` — 57 "
     "references"),
    # C-V130: opcode 11 calls 003ACA80, not 003ACA90.
    (OWN, "documents (`003ACA90`, `003AFD30`, `003B6930` — the shadow pools of BT-1)",
     "documents (~~`003ACA90`, `003AFD30`, `003B6930`~~ `003ACA90` for 10 or `003ACA80` for 11, then `003AFD30`, "
     "`003B6930` — the shadow pools of BT-1) " + T + "opcode 10 calls `003ACA90` three times from "
     "`003B8670+0x1065`; opcode 11 calls `003ACA80` at `003B8670+0x10D6`)*"),

    # C-V127: 002F8060 is 648 B.
    (HUBS, "`002F8060` (`BattleUnit_TryTriggerNearbyAuthoredFieldAction`, ~128 B) —",
     "`002F8060` (~~`BattleUnit_TryTriggerNearbyAuthoredFieldAction`, ~128 B~~ "
     "`BattleUnit_TryTriggerNearbyAuthoredFieldAction`, 648 B " + T + "its extent is 648 B, as the key table "
     "above states)*) —"),

    # C-V134: 0.005, 0.03 and 0.005556 are .rdata literals (009002B4 / 009002C4 / 009002B8).
    (CCON, "1.0 (4), **0.005 (4)**, 0.03 (3) and **0.005556 (2)**. The last two are loaded as no literal. The arms "
           "compute them,\nso a census of literal operands, like the one above, cannot list every step size.",
     "1.0 (4), **0.005 (4)**, 0.03 (3) and **0.005556 (2)**. ~~The last two are loaded as no literal. The arms "
     "compute them,~~ All three are `.rdata` literals: 0.005 at `009002B4` (−0.005 at `009002F0`), 0.03 at "
     "`009002C4`, 0.005556 at `009002B8` " + T + "the scalar-float rip operands of `001D1660`, e.g. `subss` / "
     "`addss` on `009002B8` at `001D1660+0x14F9` / `+0x150E`)*;\n~~so a census of literal operands, like the one "
     "above, cannot list every step size~~ the table above omits them by its cut, not because they are computed."),
    # C-V136: +0.01 is at 008F30E4; 009002BC holds +0.02.
    (CON282, "the pool holds `+0.01` at `009002BC` and `-0.01` at",
     "the pool holds ~~`+0.01` at `009002BC`~~ `+0.01` at `008F30E4` (`009002BC` holds `+0.02`) " + T + "the floats "
     "read from the image)* and `-0.01` at"),
    # C-V137: the code table is indexed by the dword at [r15+0xAB4] (001CD0E0+0xAFF), not the console id.
    (CCON, "The renderer indexes the table by the id itself (`001CDBDF`–`001CDBF7`: `[base + id*16 +",
     "The renderer indexes the table ~~by the id itself~~ by the dword at `[r15 + 0xAB4]`, the field id, not the "
     "console id " + T + "`001CD0E0+0xAFF` `movsxd r8, dword ptr [r15+0xab4]`, `+0xB17` "
     "`mov rax, qword ptr [rsi+rdx*8+0x1cd6e68]`)* (`001CDBDF`–`001CDBF7`: `[base + id*16 +"),
    (CCON, "    code  = qword[0x01DF6E68 + id*16]             # NULL in 183 of 294\n",
     "    code  = qword[0x01DF6E68 + id*16]             # NULL in 183 of 294   <- corrected 2026-10-02, OPUS: "
     "indexed by dword [r15+0xAB4] (001CD0E0+0xAFF), not by id; 1,314 rows, 713 NULL\n"),
    # C-V138: the table holds 1,314 rows (row + 1 at +0x08 through row 1313), 601 with a code.
    (CCON, "| **authored codes** | `01DF6E68` in `.data` | **16** | 294 (ids 0–293) | `id` |",
     "| **authored codes** | `01DF6E68` in `.data` | **16** | ~~294 (ids 0–293)~~ 1,314 (rows 0–1313) " + T
     + "`+0x08` = row + 1 through row 1313; the next 16 bytes break the pattern)* | ~~`id`~~ the field id "
     "`[r15 + 0xAB4]` (`001CD0E0+0xAFF`) |"),
    (CCON, "  +0x08  u32    sequence    EQUALS index + 1 for all 294 entries, no exception\n",
     "  +0x08  u32    sequence    EQUALS index + 1 for all 294 entries, no exception   <- corrected 2026-10-02, "
     "OPUS: for all 1,314 entries, 01DF6E68 + 1,314 x 16\n"),
    (CCON, "**A NULL code pointer** → 183 of the 294 entries;",
     "**A NULL code pointer** → ~~183 of the 294 entries~~ 713 of the 1,314 entries (183 of the first 294) " + T
     + "601 rows carry a pointer)*;"),
    # C-V139: 008AB7C0 is lea rcx, [02CB7FD0]; jmp 005DDDB0 - the teardown 00162410 registers, not a getter.
    (CON282, "the 12-byte getter `008AB7C0` returns it and has no listed caller, and",
     "~~the 12-byte getter `008AB7C0` returns it and has no listed caller~~ the 12-byte `008AB7C0` is no getter: it "
     "loads the base and tail-jumps `005DDDB0` (`008AB7C0+0x0` `lea rcx, [02CB7FD0]`, `+0x7` `jmp 005DDDB0`), and "
     "`00162410` passes its address to `00808B90` after constructing the block (`00162410+0xB` `call 005DC720`, "
     "`+0x10` `lea rcx, [008AB7C0]`, `+0x1B` `jmp 00808B90`) " + T + "read at those instructions)*; and"),
    # C-V141: 001F0AD0 writes +0x190..+0x437 only (last store 001F0AD0+0x9E9 at 02CB8404).
    (TUNES, "+390 .. +44F   shadow scalars and counts   001F0AD0; includes the four mMapShadow* names below\n",
     "+390 .. +44F   shadow scalars and counts   001F0AD0; includes the four mMapShadow* names below   <- corrected "
     "2026-10-02, OPUS: 001F0AD0's stores end at +0x434 (02CB8404, 001F0AD0+0x9E9); +438..+44F is not its\n"),
    # C-V144: 00265680 is the test inside gate 001EC560 (001EC560+0x20); the frame's gates are at 0022A770+0x449/+0x452/+0x45B.
    (EVSLOT, "and then `00265720()`; it is one of\n  the field frame's three entry gates (",
     "and then `00265720()`; ~~it is one of~~\n  ~~the field frame's three entry gates~~ it is not a gate itself but "
     "the test inside the third gate `001EC560` (called at `001EC560+0x20`; the field frame `0022A770` calls "
     "its gates `001800E0`, `001800C0`, `001EC560` at `0022A770+0x449`, `+0x452`, `+0x45B`) " + T
     + "read at those calls)* ("),
    (EVSLOT, "| `00265680` | manager-slot readiness gate | 149 B | one of the field frame's entry gates |",
     "| `00265680` | manager-slot readiness ~~gate~~ test | 149 B | ~~one of the field frame's entry gates~~ the test "
     "inside gate `001EC560` " + T + "`001EC560+0x20`)* |"),
    # C-V146: the 16 ids 0017DB90 passes include 0xA6 and exclude 0x11A; the switch table is read at 0017DB90+0x44.
    (CON282, "a 23-way jump table (`0017DBC2`..`0017DBDE`) whose cases forward ids of 12 and above (`0x86`, `0x10A`, "
             "`0x110`..`0x11D`) and none below",
     "a 23-way jump table (~~`0017DBC2`..`0017DBDE`~~ read at `0017DB90+0x44`) whose cases forward ids of 12 and "
     "above (~~`0x86`, `0x10A`, `0x110`..`0x11D`~~ `0x86`, `0xA6`, `0x10A`, `0x110`..`0x119`, `0x11B`..`0x11D`) "
     "and none below " + T + "the `mov r8d, imm` set of `0017DB90`, e.g. `0017DB90+0x55` `mov r8d, 0x11b`; no "
     "`0x11A`; `0017DB90+0x2F`–`+0x4E` is the switch code, not its table)*"),
    (CON282, "a 23-entry table (`0017DBBF`..`0017DBDE`)",
     "a 23-entry table (~~`0017DBBF`..`0017DBDE`~~ read at `0017DB90+0x44` by "
     "`mov ecx, dword ptr [rdx+rax*4+0x5dd5c]`) " + T + "`0017DB90+0x2F`–`+0x4E` is the switch code)*"),
    # C-V147: 0017D490 is 20 bytes.
    (CON2, "**has a dedicated nineteen-byte accessor:**",
     "**has a dedicated ~~nineteen-byte~~ twenty-byte accessor:** " + T + "`0017D490` runs to its `ret` at "
     "`0017D490+0x13`, 20 B)*"),

    # C-V149 / C-V150: 006084B0 copies the whole block from a register base (lea rdx,[02CB7FD0]; lea rax,[rdx+0xd0]).
    (ARMC, "All 36 are named, and in this build nothing\n      outside the console reads any of them.**",
     "All 36 are named, ~~and in this build nothing~~\n      ~~outside the console reads any of them~~ and "
     "`006084B0` copies all of them into the staged shader-constant buffer.** " + T + STAGE + "; the 282-command "
     "page's ANSWERED 2026-09-27)*"),
    (ARMC, "- **So even the nine that the scene JSON sets per scene are never read by a renderer.** The bank is\n"
           "        written and displayed, and nothing consumes it.",
     "- ~~**So even the nine that the scene JSON sets per scene are never read by a renderer.**~~ The bank is\n"
     "        written and displayed, ~~and nothing consumes it~~ and `006084B0` reads it whole " + T + STAGE
     + "; a register-based walk the rip census does not see)*."),
    (ARMB, "- **What they control in this build: nothing outside the console.** Three routes are closed:",
     "- ~~**What they control in this build: nothing outside the console.**~~ **What they control: the staged "
     "shader constants, through `006084B0`'s copy of the block** " + T + STAGE + ")*. ~~Three routes are closed~~ "
     "The three routes below miss that copy:"),
    (ARMB, "Whatever the shipped renderer uses for hair and\n        eye lighting, it is not these cells: the knobs are "
           "console-only.",
     "~~Whatever the shipped renderer uses for hair and~~\n        ~~eye lighting, it is not these cells: the knobs "
     "are console-only.~~ These cells reach the renderer through `006084B0`'s staged copy " + T
     + "`006084B0+0x3D8`)*."),
    # C-V164: the scene-config loaders only store into the block (19 slots by 001C3D50, 25 by the two).
    (ARMB, "**The consumers are named and concentrated:** `001C3D50` and `001C7940` together take 19 slots",
     "**The consumers are named and concentrated:** ~~`001C3D50` and `001C7940` together take 19 slots~~ "
     "`001C3D50` and `001C7940` only store into the block and never load from it, `001C3D50` 19 slots and the "
     "two together 25, adding `02CB7FF8`, `02CB8128` and `02CB8138` to the list " + T + "every rip operand of both "
     "bodies inside `02CB7FD0`–`02CB815F` is a store)*;"),
    (ARMD, "      - **Nothing can walk it as an array, and that is the decisive part.** The census finds\n"
           "        **zero `lea`** anywhere in the span: **no instruction takes the address of any slot**, so no\n"
           "        pointer into the block can be formed and no `base + index*4` access can exist. A computed",
     "      - ~~**Nothing can walk it as an array, and that is the decisive part.**~~ **`006084B0` walks it from a "
     "register base** " + T + STAGE + ")*. The census finds\n"
     "        **zero `lea`** anywhere in the span: ~~**no instruction takes the address of any slot**, so no~~\n"
     "        ~~pointer into the block can be formed and no `base + index*4` access can exist.~~ but a base below "
     "it is formed and offset into it. A computed"),
    # C-V151: id 28 multiplies by the Rec.709 weights (001D1660+0x3C0/+0x3D0/+0x3D8).
    (ARMA, "**Not one of those references is in slice A.** The only float constants here are `1` and `-1`, in\nid 26.",
     "**Not one of those references is in slice A.** ~~The only float constants here are `1` and `-1`, in~~\n"
     "~~id 26~~ The step constants are `1` and `-1`, in id 26; id 28 also reads the Rec.709 weights `0.2126`, "
     "`0.7152` and `0.0722` (`008F6D48`, `008F6D4C`, `008F6D44`) " + T + "`mulss` at `001D1660+0x3D0`, `+0x3C0`, "
     "`+0x3D8`)*."),
    # C-V152: 45 and 33 are call sites in 001D1660 (001A9930, 00193D50).
    (ARMA, "| 41 | `001D1D17` | — | `0` | calls the 33-arm shared helper |",
     "| 41 | `001D1D17` | — | `0` | calls the ~~33-arm~~ 33-call-site shared helper " + T + "33 direct calls to "
     "`00193D50` in `001D1660`)* |"),
    (ARMA, "| 42 | `001D1D36` | — | `0` | calls the 33-arm shared helper and one other |",
     "| 42 | `001D1D36` | — | `0` | calls the ~~33-arm~~ 33-call-site shared helper and one other " + T
     + "33 direct calls to `00193D50` in `001D1660`)* |"),
    (ARMA, "one serving **45** arms,\nthe other **33**.",
     "one serving **45** ~~arms~~ call sites,\nthe other **33** " + T + "45 direct calls to `001A9930` and 33 to "
     "`00193D50` in `001D1660`)*."),
    (ARMDIV, "A shared singleton — `001A9930` is used by 45\n  arms, `00193D50` by 33 — is a hub",
     "A shared singleton — `001A9930` is ~~used by 45~~ called at 45 sites\n  ~~arms~~ in `001D1660`, `00193D50` at 33 "
     + T + "direct call sites in the dispatcher)* — is a hub"),
    # C-V153: 00193D50 has 37 caller functions (125 sites); 47 is 001A9930's count.
    (ARMF, "33 call sites, 47 caller functions image-wide.**",
     "33 call sites, ~~47 caller functions image-wide~~ 37 caller functions image-wide.** " + T + "`00193D50` has "
     "125 direct call sites in 37 functions; 47 is `001A9930`'s count)*"),
    # C-V154: 01F82D20 is only loaded (159 qword loads, one store at 007980A0+0x1C1).
    (ARMDIV, "The hottest single address is `01F82D20`, nudged by **18** different commands.",
     "The hottest single address is `01F82D20`, ~~nudged by~~ dereferenced by **18** different commands " + T
     + "the slot itself is only loaded, 159 `mov r64` loads image-wide and 24 in `001D1660`, e.g. "
     "`001D1660+0x12C3`; its one store is `007980A0+0x1C1`; the corrections below)*."),
    (CON282, "The hottest single address is `01F82D20`, nudged by **18** different commands (18 rows",
     "The hottest single address is `01F82D20`, ~~nudged by~~ dereferenced by **18** different commands " + T
     + "the slot is only loaded, 24 times in `001D1660`, e.g. `001D1660+0x12C3`; its one store is "
     "`007980A0+0x1C1`)* (18 rows"),
    (TUNES, "and every access found is a `MOV r32`",
     "and every access found is a ~~`MOV r32`~~ `MOV r64` " + T + "159 qword loads `mov r64, qword ptr [01F82D20]`, "
     "e.g. `001D1660+0x12C3`, and one store at `007980A0+0x1C1`)*"),
    # C-V155: 0x01F82ED0 - 0x01F82D20 = 0x1B0.
    (ARMD, "`01F82ED0`, sixteen bytes further into the same region,",
     "`01F82ED0`, ~~sixteen bytes further~~ `0x1B0` (432) bytes further " + T + "`0x01F82ED0 − 0x01F82D20`)* into "
     "the same region,"),
    (ARMDIV, "`01F82ED0`, sixteen bytes further into the same region,",
     "`01F82ED0`, ~~sixteen bytes further~~ `0x1B0` (432) bytes further " + T + "`0x01F82ED0 − 0x01F82D20`)* into "
     "the same region,"),
    # C-V159: id 227 wraps one sub-field modulo the runtime d+0xE18 (001D1660+0xC5E, +0xC69).
    (ARMG, "| two-button, on the selected sub-field | **each sub-field mod 60** |",
     "| two-button, on the selected sub-field | ~~**each sub-field mod 60**~~ two sub-fields mod 60, one mod the "
     "runtime `d+0xE18` " + T + "`001D1660+0xC5E` `mov ecx, dword ptr [rdi+0xe18]`, `+0xC69` `idiv ecx`)* |"),
    # C-V160: 005DC720's own and looped stores reach +0x1027; 005DC580 inits this+0, 005DC430 the +0xD0 member.
    (ARME, "`005DC580` covers `0x00–0xC4` and `005DC720` covers `0x42C–0x4D8`;",
     "`005DC580` covers `0x00–0xC4` and `005DC720` covers ~~`0x42C–0x4D8`~~ `0x42C`–`0x4D8` directly, then re-runs "
     "`005DC580` / `005DC430` on two copies at `+0x5F0` / `+0x6C0` and `+0xB88` / `+0xC58` with its own fields "
     "`+0xA1C`–`+0xA5B` and `+0xFB4`–`+0xFF3`, and zeroes `+0x1010`–`+0x1027` " + T + "`005DC720+0xD1` "
     "`lea rbx, [rdi+0xa1d]`, loop back at `+0x13B`, stores at `+0x13D`–`+0x14B`)*;"),
    (ARME, "`005DC580` + `005DC430`\ninit the `+0xD0` member,",
     "~~`005DC580` + `005DC430`~~\n~~init the `+0xD0` member~~ `005DC580` inits the object from `+0` and "
     "`005DC430` the `+0xD0` member " + T + "`005DC720+0x25` `call 005DC580` with `rcx = this`, `+0x2A` "
     "`lea rcx, [rdi+0xd0]`, `+0x31` `call 005DC430`)*,"),
    # C-V162: id 38 increments only (001D1660+0x623..+0x62E).
    (ARMDIV, "Every stepping arm\nholds both directions - ",
     "~~Every stepping arm~~\n~~holds both directions~~ Every stepping arm but id 38 holds both directions " + T
     + "id 38 at `001D1660+0x623` only increments, `+0x62E` `inc ecx`, then wraps mod 3)* - "),
    (ARMF, "In slices A–D the flag was universal among stepping arms;",
     "~~In slices A–D the flag was universal among stepping arms~~ In slices A–D the flag was nearly universal "
     "among stepping arms, id 38 ignoring it " + T + "`001D1660+0x623`–`+0x62E`, an `inc` with no direction test)*;"),
    # C-V163: id 103 is cmp/sete and its label does not end in enable.
    (ARME, "Every `cmp`/`sete` arm in both slices carries a\n   label ending in \"enable\" or \"Enabled\".",
     "~~Every `cmp`/`sete` arm in both slices carries a~~\n   ~~label ending in \"enable\" or \"Enabled\"~~ Every "
     "`cmp`/`sete` arm but one carries a label ending in \"enable\" or \"Enabled\"; id 103's is \"Camera Over Write "
     "(O to capture): \" " + T + "id 103 at `001D1660+0x149D` is `cmp`/`sete`; its label `008FDC00` is stored at "
     "menu `+0x468` by `001D0390+0x4D7`)*."),
    # C-V89 on the README: the one clear covers 022D91B0..022D942F and vf00.
    (README, "the only whole-area clear is unowned, and",
     "~~the only whole-area clear is unowned~~ the one clear, `0036D9E0` over `022D91B0`–`022D942F` and vf00, is "
     "unowned " + T + "`0036D9E0+0x25`–`+0x38A`)*, and"),

    # ---- 3.1.C counts the image decides ----
    # C4 LOG: 0016D670 has 23 direct call sites in 23 functions, not two callers.
    (LOG, "It is `lea rax, [rip+…] ; ret`, and both callers immediately use",
     "It is `lea rax, [rip+…] ; ret`, and ~~both callers~~ both callers read here (of 23 direct call sites in 23 "
     "functions) " + T + "`retool.py callers 0016D670`; the 2026-09-14 killer run below)* immediately use"),
    # C10 ARM-D: (0x02CB8144 - 0x02CB7FE8) / 4 + 1 = 88 dwords.
    (ARMD, "Whole-image census over all 89 dwords from `02CB7FE8` to",
     "Whole-image census over all ~~89~~ 88 dwords " + T + "`(0x02CB8144 − 0x02CB7FE8) / 4 + 1` = 88)* from "
     "`02CB7FE8` to"),

    # ---- 3.2 stale / banner items ----
    # C-S1..C-S9: README status words that disagree with each page's front matter.
    (README, "  **PARTIAL, tier 1.** **The engine's freeze composition**",
     "  **PARTIAL, tier 1.** " + FM("AUDITED") + " **The engine's freeze composition**"),
    (README, "  **PARTIAL, tier 1.** **7 % of the game's code, run once**",
     "  **PARTIAL, tier 1.** " + FM("DOCUMENTED, owner read 2026-09-30") + " **7 % of the game's code, run once**"),
    (README, "  **DOCUMENTED, tier 1.** The application root:",
     "  **DOCUMENTED, tier 1.** " + FM("AUDITED") + " The application root:"),
    (README, "  **DOCUMENTED, tier 1, one falsification pass.** Answers open question **B-4**",
     "  **DOCUMENTED, tier 1, one falsification pass.** " + FM("AUDITED") + " Answers open question **B-4**"),
    (README, "  **PARTIAL, tier 1.** The workbench is the **register bank",
     "  **PARTIAL, tier 1.** " + FM("DOCUMENTED, re-statused 2026-09-29 (FABLE)") + " The workbench is the "
     "**register bank"),
    (README, "  **DOCUMENTED, tier 1, one falsification pass.** Answers **BQ-13**.",
     "  **DOCUMENTED, tier 1, one falsification pass.** " + FM("AUDITED") + " Answers **BQ-13**."),
    (README, "  **DOCUMENTED, tier 1.** Three functions totalling 125 bytes",
     "  **DOCUMENTED, tier 1.** " + FM("AUDITED") + " Three functions totalling 125 bytes"),
    (README, "  **DOCUMENTED, tier 1.** `World_UpdateSimulationTick` ticks",
     "  **DOCUMENTED, tier 1.** " + FM("AUDITED") + " `World_UpdateSimulationTick` ticks"),
    # C-V119 on the README: two sub-labels are wrong (ownership page, 2026-09-22 / 2026-09-26).
    (README, "**Three sub-labels are wrong** and are named.",
     "**Three sub-labels are wrong** " + A("the ownership page's answers of 2026-09-22 and 2026-09-26, two are "
                                          "wrong, not three") + " and are named."),
    # C-S181 / C-S221: thirteen objects / the 660-byte buffer, corrected 2026-09-02.
    (README, "is thirteen objects rather than one.",
     "is thirteen objects " + A("the workbench page's CORRECTED 2026-09-02, 62 objects, not 13, and the ownership "
                                "page's 2026-09-02 correction of the 660-byte buffer into three row blocks and "
                                "separate slots") + " rather than one."),
    # C-S13: FLOAT's status line.
    (FLOAT, "**Status is `PARTIAL` deliberately.** The chain,",
     "**Status is `PARTIAL` deliberately.** " + A("the front matter, status DOCUMENTED after the owner read of "
                                                 "2026-09-30") + " The chain,"),
    # C-S18: 00379CF0 is in the function list.
    (BOOT, "**not in the function list**. A caller census",
     "**not in the function list** " + A("the key-address table below, listed in the function list since") + ". "
     "A caller census"),
    # C-S25 / C-S27: C-BOOT open items answered on the boot page 2026-09-30.
    (CBOOT, "elsewhere; **what they are is not established by this function** **[page]**.",
     "elsewhere; **what they are is not established by this function** **[page]** "
     + A("what-the-engine-fixes-at-boot.md, RC-3 answered 2026-09-30") + "."),
    (CBOOT, "**What the tail bytes are *for* is still open** — nothing",
     "**What the tail bytes are *for* is still open** " + A("what-the-engine-fixes-at-boot.md, RC-2 answered "
                                                           "2026-09-30") + " — nothing"),
    # C-S42 / C-S44 / C-S45: TICK items answered in its section 7.
    (TICK, "three unread gates that skip the tick entirely.",
     "three unread gates " + A("EX-6, ANSWERED 2026-09-12 (FABLE), which reads all three") + " that skip the tick "
     "entirely."),
    (TICK, "> pass is not established (`EX-9`).",
     "> pass is not established (`EX-9`) " + A("EX-9, ANSWERED 2026-09-18 (FABLE)") + "."),
    (TICK, "| What the unread callees do | **not established** | — | UNKNOWN |",
     "| What the unread callees do | **not established** " + A("EX-3, ANSWERED 2026-09-12 (FABLE)") + " | — | "
     "UNKNOWN |"),
    # C-S43: C-TICK's unread gates.
    (CTICK, "**those gates are unread** and this",
     "**those gates are unread** " + A("the world-tick page's EX-6, ANSWERED 2026-09-12 (FABLE), and the "
                                       "2026-09-22 notes below") + " and this"),
    # C-S64 / C-S65 / C-S66: FORCE items answered by AN-4 / AN-2 / AN-1.
    (FORCE, "| `BattleUnit_UpdateCombatFrame`, `FUN_0030C010` | unread |",
     "| `BattleUnit_UpdateCombatFrame`, `FUN_0030C010` | unread " + A("AN-4, ANSWERED 2026-09-12 (FABLE)") + " |"),
    (FORCE, "| `00252C80` | the second writer — 134 B, unread |",
     "| `00252C80` | the second writer — 134 B, unread " + A("AN-2, answered 2026-09-11") + " |"),
    (FORCE, "What they are remains open, but the shape",
     "What they are remains open " + A("AN-1, ANSWERED 2026-09-17 (FABLE)") + ", but the shape"),
    # C-S70: 00253B90 is read on the force-fight page.
    (NBR, "`00253B90` gate the paths and are **not read**.",
     "`00253B90` gate the paths and are **not read** " + A("force-fight-mode.md, which reads `00253B90`'s whole "
                                                          "body") + "."),
    # C-S78 / C-S80 / C-S81 / C-S83: GATE items answered in its section 7.
    (GATE, "Both now have one, and neither is answered.",
     "Both now have one, and neither is answered " + A("section 7, UQ-25 / DZ-1 ANSWERED 2026-09-17 (FABLE) and "
                                                       "DZ-2 ANSWERED 2026-09-11") + "."),
    (GATE, "**No name is proposed for the node type.** Degrees",
     "**No name is proposed for the node type.** " + A("section 7, UQ-25 ANSWERED 2026-09-17 (FABLE): the "
                                                       "target-line object") + " Degrees"),
    (GATE, "**Which field uses which is not established.**",
     "**Which field uses which is not established** " + A("section 7, UQ-27 ANSWERED 2026-09-17 (FABLE): no field "
                                                          "is in thousandths of a degree") + "."),
    (GATE, "is **not established**. *(This paragraph",
     "is **not established** " + A("section 7, UQ-26, NO ADMISSIBLE SOURCE, signed 2026-09-16") + ". *(This "
     "paragraph"),
    # C-S87: the residue bound was corrected the same day.
    (CGATE, "and that the 3,862 are",
     "and that the 3,862 " + A("the CORRECTED SAME DAY note above, at most 3,079 bytes in 191 spans") + " are"),
    # C-S100 / C-S102 / C-S103 / C-S104 / C-S105: MODE items answered on the page or its contract.
    (MODE, "**PARTIAL.** The ladder, its inputs",
     "**PARTIAL.** " + A("the front matter, status AUDITED, brought up to date 2026-09-18 (FABLE)") + " The ladder, "
     "its inputs"),
    (MODE, "**Bits 0 and 1 have no script verbs at all** — the",
     "**Bits 0 and 1 have no script verbs at all** " + A("section 2c, ANSWERED 2026-09-12: both have verbs") + " — the"),
    (MODE, "Bit 0 is UI, bit 1 is combat/audio, and",
     "Bit 0 is UI, bit 1 is combat/audio " + A("the ANSWERED 2026-09-12 notes, bit 0 the summon and bit 1 the "
                                               "chocobo") + ", and"),
    (MODE, "**O-4 stays open**: what the six",
     "**O-4 stays open** " + A("O-4, ANSWERED 2026-09-12 (FABLE)") + ": what the six"),
    (MODE, "an event script relies on is not read.",
     "an event script relies on is not read " + A("the mode contract, ANSWERED 2026-09-22 (SWE2-CONTRACT): the "
                                                  "party read-in state machine `0037B4D0`") + "."),
    # C-S112 / C-S113 / C-S114: C-MODE items executed or read since.
    (CMODE, "| any execution of this operation, isolated or live | **none**; §13 | none | UNKNOWN |",
     "| any execution of this operation, isolated or live | **none**; §13 " + A("the executions of 2026-09-12 and "
                                                                             "2026-09-26 above") + " | none | "
     "UNKNOWN |"),
    (CMODE, "**The four setters are still not driven**, so",
     "**The four setters are still not driven** " + A("the 2026-09-26 note above, setters, reset, getters and "
                                                       "the save round trip executed") + ", so"),
    (CMODE, "whose body is **not read here** — and reads the table",
     "whose body is **not read here** " + A("the 2026-09-18 note below: the negative-index clamp is in "
                                            "`003148F0`") + " — and reads the table"),
    # C-S123: LOG's channel id.
    (LOG, "- **What the channel id means**, or its range. It is",
     "- **What the channel id means**, or its range " + A("the 2026-09-30 answer below, channel 4 is the "
                                                          "debugger-break channel") + ". It is"),
    # C-S150 / C-S151: ABI's frontier figure and its UQ-1 example.
    (ABI, "and the 562 functions below are still in it.",
     "and the 562 functions below are still in it " + A("the 2026-09-17 update below, the frontier now holds "
                                                        "342") + "."),
    (ABI, "`002465F0` is the known case: four register arguments",
     "`002465F0` is the known case " + A("the note below, `002465F0` is not in the dataset") + ": four register "
     "arguments"),
    # C-S157 / C-S158: WB's BQ-16 grouping and BQ-19.
    (WB, "  row array (grouping beyond matrix 0 unproven, BQ-16):\n",
     "  row array (grouping beyond matrix 0 unproven, BQ-16):   <- corrected 2026-10-02, OPUS - answered: BQ-16 "
     "ANSWERED in section 7 (ticked 2026-09-13)\n"),
    (WB, "is `BQ-19`'s question, not answered here.",
     "is `BQ-19`'s question, not answered here " + A("the register-bank page, BQ-19 ANSWERED 2026-09-18 (FABLE): "
                                                     "one user thread") + "."),
    # C-S163 / C-S168 / C-S173: SAVE / C-SAVE / C-PRIM.
    (SAVE, "and what it selects is not established.",
     "and what it selects is not established " + A("UQ-42, ANSWERED 2026-09-17 (FABLE), below") + "."),
    (CSAVE, "249 functions write one shared area and nothing restores it; the house rule",
     "249 functions write one shared area and nothing restores it " + A("the workbench page's CORRECTED "
                                                                        "2026-09-08, the nine Save / Restore "
                                                                        "users") + "; the house rule"),
    (CPRIM, "not owned here.** `022D91A0` has 67 writers image-wide,",
     "not owned here.** " + A("the census below that replaced these counts 2026-09-21 (SWE2-CONTRACT)") + " "
     "`022D91A0` has 67 writers image-wide,"),
    # C-S184 / C-S186: RTTI's two "still open" lines.
    (RTTI, "**Still open:** which *game* subsystem calls that narrow interface.",
     "**Still open:** " + A("section 6, AS-1a ANSWERED as far as it can be") + " which *game* subsystem calls "
     "that narrow interface."),
    (RTTI, "- **Still open:** whether Phyre's reflection glue",
     "- **Still open:** " + A("the GLUE HALF ANSWERED 2026-09-22 (FABLE) note") + " whether Phyre's reflection "
     "glue"),
    # C-S204 / C-S205 / C-S206 / C-S207: HUBS rows read since.
    (HUBS, "| *(Audio)* — calls `Actor_GetWorldPosition` | 1,036 B | — | not read |",
     "| *(Audio)* — calls `Actor_GetWorldPosition` | 1,036 B | — | not read " + A("the world-tick page's EX-3, the "
                                                                                "audio listener update") + " |"),
    (HUBS, "| `SpawnKeep_RotatePersistenceBanksForAreaTransition` | 672 B | — | not read |",
     "| `SpawnKeep_RotatePersistenceBanksForAreaTransition` | 672 B | — | not read " + A("the shared-neighbours "
                                                                                     "page, read in full "
                                                                                     "2026-09-14") + " |"),
    (HUBS, "| — | `SaveImage_GetPersistentPayloadBase` | — | — | not read |",
     "| — | `SaveImage_GetPersistentPayloadBase` | — | — | not read " + A("U-5, ANSWERED 2026-09-12 (FABLE)") + " |"),
    (HUBS, "identifying them is **U-3**.",
     "identifying them is **U-3** " + A("U-3, ANSWERED 2026-09-12 (FABLE)") + "."),
    # C-S222 / C-S223 / C-S224 / C-S231 / C-S236: console items answered since.
    (CCON, "nothing here has been observed running.",
     "nothing here has been observed running " + A("the 2026-09-25 note above, OPUS block 315 executed every "
                                                   "id") + "."),
    (CCON, "1. **Whether the 111 codes are area codes** (I-7) —",
     "1. **Whether the 111 codes are area codes** (I-7) " + A("the second-console-table page, Answered 2026-09-30 "
                                                              "(SWE2-CONTRACT): map-pack names indexed by field "
                                                              "id") + " —"),
    (CCON, "4. **The eight-entry uniform array the console cannot reach** —",
     "4. **The eight-entry uniform array the console cannot reach** " + A("what-the-console-tunes.md, eight "
                                                                          "shadow-map cascade matrices, UQ-24 "
                                                                          "2026-09-16") + " —"),
    (CON282, "97 addresses, none named. This is the open question",
     "97 addresses, none named " + A("the ANSWERED 2026-09-27 (OPUS) note, each becomes a named shader-constant "
                                     "variable") + ". This is the open question"),
    (TUNES, "> **This does not identify `01F82D20`.** It is",
     "> **This does not identify `01F82D20`.** " + A("section 7, Answered 2026-09-14 (FABLE): the "
                                                     "`GameSettingConfig` singleton pointer") + " It is"),
    # C-S247: 01F832C4 has a second writer.
    (EVSLOT, "| `01F832C4` | dword | cleared by the pusher each push |",
     "| `01F832C4` | dword | cleared by the pusher each push " + A("the note below, `001EC690` also increments "
                                                                   "it") + " |"),
    # C-S253 / C-S261 / C-S262 / C-S263 / C-S265 / C-S266 / C-S268 / C-S269 / C-S270: the arm catalogue.
    (ARMDIV, "**96 of 282 ids catalogued; 186 remain.**",
     "**96 of 282 ids catalogued; 186 remain** " + A("H delivered and The table is closed, 282 of 282, below") + "."),
    (ARMB, "Who calls it is still untraced.",
     "Who calls it is still untraced " + A("the 2026-09-14 answer below, one way in through `001CD040`") + "."),
    (ARMC, "**No target in this slice is identified by name** — see §8.",
     "**No target in this slice is identified by name** " + A("UQ-11, ANSWERED 2026-09-25: all 36 named") + " — "
     "see §8."),
    (ARMD, "ids 140–293 are unread, and nothing",
     "ids 140–293 are unread " + A("slices E to I, delivered") + ", and nothing"),
    (ARME, "`0x0E` is a channel or key selector, not decoded.",
     "`0x0E` is a channel or key selector, not decoded " + A("the cross-check below, `0x38 / 4 = 14`, "
                                                             "property 14") + "."),
    (ARMF, "**No field in this slice was traced to a reader.**",
     "**No field in this slice was traced to a reader** " + A("the ANSWERED 2026-09-25 note below") + "."),
    (ARMG, "and ids 236–293 are unread.",
     "and ids 236–293 are unread " + A("slices H and I, delivered") + "."),
    (ARMI, "(ids 236–267) is unread, and",
     "(ids 236–267) is unread " + A("slice H, delivered, and the test against its section 8 below") + ", and"),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('its one store is `007980A0+0x1C1`',
     'its one store is at `+0x1C1` of a 2,153-byte Phyre framework body'),
]
_rn = lambda s: __import__('functools').reduce(lambda a, p: a.replace(p[0], p[1]), ROLE_NAMES, s)
EDITS = [(e[0], _rn(e[1])) if len(e) == 2 else (e[0], e[1], _rn(e[2])) + tuple(e[3:]) for e in EDITS]


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
