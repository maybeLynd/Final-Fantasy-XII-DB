"""apply_16ui.py [--apply] - 16-UI readiness map (cloud-reports/re-readiness/16-ui.md), section 3.1 value items
CV-1..CV-112 that the shipping image decides, plus section 3.3 banner and stale items, settled on the pages (OPUS,
2026-10-02).

Each edit strikes the side the image REFUTES only and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* or
*(answered: see ...; 2026-10-02, OPUS)*. Items the image leaves as "both partly" or "undecidable statically" get no
edit (verdicts in the OPUS scratch file verdicts-16.md). Where a verdict is partial, only what the bytes show is said.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`<- corrected` comment instead of a strike (their OLD includes the line end, so NEW never contains OLD); the two
front-matter edits are trailing `# <- corrected` comments on single-line keys. No heading changes. Interior addresses
cited in NEW text are written as function entry + offset (A-drift rule); bare interior addresses that remain are the
pages' own text.
Section 3.3: the in-body PARTIAL banners and the README tags are restated to each page's own front-matter word; a few
"not read / open" lines get *(answered: ...)*. The count items of section 3.2 are not edited.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "16-UI/"
RM = F + "README.md"
CR = F + "CONTRACT-ui-request-router.md"
CT = F + "CONTRACT-text-control-codes-and-dyngeo-draw.md"
SEL = F + "the-selection-the-menu-publishes.md"
CW = F + "Widget-Object-Model/CONTRACT-widget-object.md"
SZ = F + "Widget-Object-Model/the-widget-constructor-and-object-sizes.md"
MP = F + "Widget-Object-Model/the-widget-message-protocol.md"
AN = F + "Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md"
TA = F + "Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md"
RR = F + "Request-Router/ui-request-router.md"
TL = F + "Text-And-Number-Rendering/the-text-control-code-language.md"
NF = F + "Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md"
FK = F + "Text-And-Number-Rendering/font-data-kerning-and-expansion.md"
DG = F + "Dynamic-Geometry-Instances/dyngeo-instance-family.md"
LP = F + "Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md"
MW = F + "Message-Windows/the-message-window-layout-readers.md"
BH = F + "Battle-Hud/the-battle-hud-layout-readers.md"
CF = F + "Config-Screen/the-config-screen-and-what-a-setting-change-runs.md"
MS = F + "Map-Screens/the-map-screens-and-their-shared-map-data.md"
QL = F + "Quest-List/the-quest-list-screen.md"
AT = F + "Menu-Screen-Atlas/the-menu-screen-atlas.md"
UP = F + "Unlabelled-Panes/the-unlabelled-procedures.md"
SD = F + "Shared-Dialogs/the-shared-dialog-widgets.md"
SH = F + "Shop-Screens/the-shop-screens.md"
LG = F + "License-Board-View/the-license-board-grid-build-and-its-change-sweep.md"
LW = F + "License-Board-View/the-license-board-screen-widgets.md"
GB = F + "Gambit-Screens/the-gambit-screens.md"
HB = F + "Handbook/the-handbook-screen.md"
HM = F + "Handbook/the-handbooks-monster-viewer.md"

FM = "the front matter says `status: %s`"
FACTORY = "`00244F50` takes the size in `ecx`, the handler in `rdx` and the init message in `r8`"


def readme_tag(old_tag, new_tag, rest):
    return (RM, old_tag + " " + rest,
            "~~" + old_tag + "~~ " + new_tag + " *(corrected 2026-10-02, OPUS: the page's own front matter says "
            "`status: " + new_tag.strip("*").split(",")[0] + "`)* " + rest)


EDITS = [
    # ---------------------------------------------------------------- Widget object model
    # CV-1 + CV-2: 00244DD0 sets bit 9 (00244DD0+0x77 bts edx, 9); the release clears bit 10 (002482E0+0xD4), which the
    #     teardown's keep path sets (00245020+0x77 bts eax, 0xa). 009151AC = 00915198 + 0x14, a descriptor half, no string.
    (CW, "Modes **0 and 3** schedule: `+0x40 |= bit9` (the deferred-destroy arm the\n"
         "  `and 0xFFFFFBFF` clear at release names), `+0x68` = the named record `009151AC`\n"
         "  (`\"map\\rbl_a\\rbl_a02\\global\"`) when",
     "Modes **0 and 3** schedule: `+0x40 |= bit9` ~~(the deferred-destroy arm the~~\n"
     "  ~~`and 0xFFFFFBFF` clear at release names)~~ *(corrected 2026-10-02, OPUS: bit 9 is not the bit the release "
     "clears — `and 0xFFFFFBFF` at `002482E0+0xD4` clears bit 10, which the teardown's keep path sets at "
     "`00245020+0x77` `bts eax, 0xa`; this arm's `bts edx, 9` is `00244DD0+0x77`)*, `+0x68` = ~~the named record "
     "`009151AC`~~\n"
     "  ~~(`\"map\\rbl_a\\rbl_a02\\global\"`)~~ `009151AC`, the default descriptor's backward half `00915198 + 0x14` "
     "*(corrected 2026-10-02, OPUS: `00244DD0+0x89` `lea rcx, [009151AC]`; the bytes there are a 20-byte descriptor "
     "half, `00 00 00 00 01 00 …`, not a string)* when"),
    (CW, "(`009151AC` `\"map\\rbl_a\\rbl_a02\\global\"` when `+0x40` bit 16, else `[+0x48]+0x14`)",
     "(`009151AC` ~~`\"map\\rbl_a\\rbl_a02\\global\"`~~ — the default descriptor's backward half `00915198 + 0x14`, "
     "not a string *(corrected 2026-10-02, OPUS: `00244DD0+0x89` `lea rcx, [009151AC]`)* — when `+0x40` bit 16, else "
     "`[+0x48]+0x14`)"),

    # CV-3: under 0208F560 != 0 the constructor forces bit 17 to 0 (002465F0+0x69..+0x7D), not to the flipped parity.
    (SZ, "matched pairs from `0025058D`–`00250914`, so widgets built inside such a bracket see the flipped value.",
     "matched pairs from `0025058D`–`00250914`, so widgets built inside such a bracket ~~see the flipped value~~ get "
     "bit 17 = 0 whatever the parity *(corrected 2026-10-02, OPUS: `002465F0+0x69`–`002465F0+0x7D` — when `0208F560` "
     "is non-zero, `xor` with `(0208ED5C & 1) << 17` clears the bit the merge above set; CONTRACT-widget-object.md, "
     "CHECKED AGAIN 2026-09-13)*."),

    # CV-4: bit 0 SET runs the nibble dispatch (00244DD0+0x4A test dl,1 / +0x4D jne); state 1 is written when it is clear.
    (AN, "the backward starter `00244DD0` sets **1** outright when `+0x40` bit 0 is set (`00244E1F`..`00244E23`)",
     "the backward starter `00244DD0` sets **1** outright when `+0x40` bit 0 is ~~set~~ clear (`00244E1F`..`00244E23`) "
     "*(corrected 2026-10-02, OPUS: `00244DD0+0x4A` `test dl, 1` / `00244DD0+0x4D` `jne` skip to the arms when bit 0 "
     "is set; the state-1 store at `00244DD0+0x4F` runs only when it is clear)*"),

    # CV-5: 00245020's keep path sets bit 10 (00245020+0x77 bts eax, 0xa), not bit 0x10.
    (TA, "clears bit 1 and sets bit `0x10`, and keeps the storage.",
     "clears bit 1 and sets ~~bit `0x10`~~ bit 10 (`0x400`), and keeps the storage *(corrected 2026-10-02, OPUS: "
     "`00245020+0x77` `bts eax, 0xa`)*."),

    # CV-6: the reconcile releases only bit-10 widgets (00248030+0x56 / +0x67); the rest get bit 2, {2} unless bit 18,
    #     and the parity restamp (00248030+0xAB, +0xBF, +0xD1..+0xE0), and their children are walked (+0xE3).
    (SZ, "the others are processed - detached through `002482E0` and, when `+0x40` bit 10 is set, walked into their "
         "children.",
     "the others are processed - ~~detached through `002482E0` and, when `+0x40` bit 10 is set, walked into their "
     "children.~~ released through `002482E0` only when `+0x40` bit 10 is set; the rest get bit 2, message 2 unless "
     "bit 18 is set, and bit 17 restamped to the parity, and their children are walked *(corrected 2026-10-02, OPUS: "
     "`00248030+0x56` `bt ecx, 0xa` → `00248030+0x67` `call 002482E0`; else `00248030+0xAB` `or ecx, 4`, "
     "`00248030+0xBF` `{2}`, `00248030+0xD1`–`00248030+0xE0` the restamp, `00248030+0xE3` the first child)*."),
    (SZ, "and the drain is the reconcile that removes widgets built under the other generation",
     "and the drain is the reconcile that ~~removes widgets built under the other generation~~ releases the deferred "
     "(bit-10) widgets of the other generation and re-stamps the rest *(corrected 2026-10-02, OPUS: as above)*"),

    # CV-7: 00249410 seals first (00249410+0x15) so the sealed test always passes; only the {16} path clears bit 0.
    (MP, "`or [rcx],2` sets the sealed bit; if it was **already**",
     "`or [rcx],2` sets the sealed bit; if ~~it was **already**~~ it is now *(corrected 2026-10-02, OPUS: the seal is "
     "set first, `00249410+0x15`, so the test at `00249410+0x1B` always passes)*"),
    (MP, "`{0x10,0,0,0}` arg block. Exit clears bit\n0 (`and [rbx],~1`).",
     "`{0x10,0,0,0}` arg block. ~~Exit clears bit~~ Only that vcall path clears bit\n0 (`and [rbx],~1`, at "
     "`00249410+0x6F`); the custom call returns with bit 0 still set *(corrected 2026-10-02, OPUS: `00249410+0x30` "
     "`call [rcx+0x10]` is followed by the epilogue)*."),

    # CV-8: 0208F570 counts 60 Hz frames: the UI pass adds 1..3 per pass and durations are converted ms -> frames.
    (MP, "start tick `dword[+0x94]`, the millisecond clock",
     "start tick `dword[+0x94]`, the ~~millisecond clock~~ frame clock *(corrected 2026-10-02, OPUS: the UI pass adds "
     "a step of 1 to 3 frames per pass — `00250540+0x89` `add [0208F570], r14d`, or `00250540+0x47` adding "
     "`00184950()`, clamped to 1..3 at `00798E90+0x14` — and `00244DD0+0xF2`–`00244DD0+0x104` convert a millisecond "
     "duration to 60 Hz frames before it meets the clock)*"),
    (MP, "(about 24.8 days at rate 1.0).",
     "(about ~~24.8 days~~ 414 days at rate 1.0, the clock counting 60 Hz frames *(corrected 2026-10-02, OPUS: see "
     "the clock correction above)*)."),

    # CV-9: 002481C0 stops at the first node lacking bit 0 or 3 (002481C0+0x16 / +0x1B je -> ret); it is not a search.
    (MP, "the `0208EBC0` chain is walked (`rax = [rax+0x10]`) for the first\n"
         "node whose `dword[+0x40]` carries both bits `0x1` and `0x8`; bit",
     "the `0208EBC0` chain is walked (`rax = [rax+0x10]`) ~~for the first~~ while each\n"
     "~~node whose~~ node's `dword[+0x40]` carries both bits `0x1` and `0x8`, and a node lacking either ends the walk "
     "with no message *(corrected 2026-10-02, OPUS: `002481C0+0x16`/`002481C0+0x1B` `je` to the `ret`)*; bit"),

    # CV-10: 10 has a framework sender (002481C0+0x34, the record's only reference); 16 is sent by the batch seal.
    (MP, "| **application only** | 0, 10, 13, 16, 26, 29–53, 61, 92, 95, 114, 119, 192, 285–289 |",
     "| **application only** | 0, ~~10,~~ 13, ~~16,~~ 26, 29–53, 61, 92, 95, 114, 119, 192, 285–289 *(corrected "
     "2026-10-02, OPUS: 10 has a framework sender — the focus notice, `002481C0+0x34` `lea rdx, [009150D8]`, the "
     "record's only reference — and 16 is a \"both\" id, sent by the batch seal at `00249410+0x46`–`00249410+0x6D`)* |"),

    # CV-11: 00244F50(size ecx, handler rdx, init r8) - 00244F50+0x14..+0x1A; the "command/tag/code" readings refuted.
    (MP, "calls: when `0209AC30`'s `+0x278` object is null it posts\n"
         "command `0xC8` with record `{0, movsxd(ecx), 0}` and code\n"
         "`002CF940` through `00244F50`; when the object exists and",
     "calls: when `0209AC30`'s `+0x278` object is null it ~~posts~~ builds\n"
     "~~command `0xC8` with record `{0, movsxd(ecx), 0}` and code~~ a `0xC8`-byte widget whose handler is\n"
     "`002CF940` through `00244F50`, with `{0, movsxd(ecx), 0}` as its init message *(corrected 2026-10-02, OPUS: "
     + FACTORY + " — `00244F50+0x14`–`00244F50+0x1A` keep them)*; when the object exists and"),
    (MP, "`0023DFC0` (95 B) is a `0x2E0`-tagged packet submit the widget record readers",
     "`0023DFC0` (95 B) is ~~a `0x2E0`-tagged packet submit~~ a `0x2E0`-byte widget build *(corrected 2026-10-02, "
     "OPUS: " + FACTORY + " — `0023DFC0+0x39` `mov ecx, 0x2e0`, `0023DFC0+0x28` `lea rdx, [0023E020]`; `0023E020` is "
     "the handler)* the widget record readers"),
    (MP, "continuation and `ecx = 0x2E0` as the tag (`0023DFE8`/`0023DFF9`), and posts",
     "~~continuation and `ecx = 0x2E0` as the tag~~ handler and `ecx = 0x2E0` as the size (`0023DFE8`/`0023DFF9`), "
     "and ~~posts~~ constructs *(corrected 2026-10-02, OPUS: as above)*"),
    (MP, "`002C41F0` posts command `0x7B0` with code `002C4460`",
     "`002C41F0` ~~posts command `0x7B0` with code `002C4460`~~ builds a `0x7B0`-byte widget with handler `002C4460` "
     "*(corrected 2026-10-02, OPUS: `002C41F0+0x14` `lea rdx, [002C4460]`, `002C41F0+0x1B` `mov ecx, 0x7b0`, then "
     "`jmp 00244F50`)*"),
    (MP, "is empty; `002C2F60` posts `0xAF8` with code `002C3560`",
     "is empty; `002C2F60` ~~posts `0xAF8` with code `002C3560`~~ builds a `0xAF8`-byte widget with handler `002C3560` "
     "*(corrected 2026-10-02, OPUS: `002C2F60+0x1B` `mov ecx, 0xaf8`, then `jmp 00244F50`)*"),
    (LP, "through `00244F50` (code `0x278`)",
     "through `00244F50` (~~code~~ size `0x278` *(corrected 2026-10-02, OPUS: `003BC450+0x43` `mov ecx, 0x278`; "
     + FACTORY + ")*)"),

    # CV-12: the factory's slot+1 store (00244F50+0xA4) is overwritten: memset (002465F0+0x36), 0xFF80 at +0xA1 (+0xF6).
    (CW, "index** into `+0xA2` and passes `pooled = 1`",
     "index** into `+0xA2` *(corrected 2026-10-02, OPUS: a dead store — the constructor's memset at `002465F0+0x36` "
     "and its word `0xFF80` at `+0xA1`, `002465F0+0xF6`, leave `+0xA2 = 0xFF`; the ✖ correction below)* and passes "
     "`pooled = 1`"),
    (CW, "taking it sets `[+0xA2] = 1` |",
     "~~taking it sets `[+0xA2] = 1`~~ taking it stores `slot + 1` at `00244F50+0xA4`, which the constructor "
     "overwrites: its memset (`002465F0+0x36`) and the word `0xFF80` at `+0xA1` (`002465F0+0xF6`) leave `+0xA2 = 0xFF` "
     "*(corrected 2026-10-02, OPUS: the ✖ correction of §3, re-read at the bytes)* |"),

    # CV-13: +0x40 bit 0x4000 is cleared (002465F0+0xE1) and re-set from the fifth argument (002465F0+0x102).
    (SZ, "with bit `0x20000` from a global and bit `0x4000` cleared |",
     "with bit `0x20000` from a global and bit `0x4000` cleared and then re-set from the fifth argument *(corrected "
     "2026-10-02, OPUS: `002465F0+0x102` `or [rdi+0x40], eax` with `eax = (arg5 & 1) << 14`; the pool slot and the "
     "in-place construct pass 1)* |"),

    # CV-14: 001EDEC0 is the half-rate phase predicate (1 unless 01F82E38 set and 01DFE0C0 clear, else (~x) & 1).
    (SZ, "selector resolve `001EDEC0`",
     "~~selector resolve~~ half-rate phase predicate `001EDEC0` *(corrected 2026-10-02, OPUS: `001EDEC0+0x1A` "
     "`not ecx` / `and ecx, 1`; it selects nothing)*"),
    (CW, "calls `001EDEC0`, the shared resolver `002D2DB0`/`00241D40`/`0057FE80` also reach.",
     "calls `001EDEC0`, ~~the shared resolver~~ the half-rate phase predicate *(corrected 2026-10-02, OPUS: "
     "`001EDEC0` returns 1 unless `01F82E38` is set and `01DFE0C0` clear, else `(~x) & 1` at `001EDEC0+0x1A`; it "
     "resolves nothing)* `002D2DB0`/`00241D40`/`0057FE80` also reach."),

    # CV-18: 289 goes from the pick list 0056B4D0 to its creator, the editor at [self+0xC8] (0056B4D0+0x4F..+0x79).
    (MP, "gambit list's destroy notice to its editor child, which sets the child's `+0x331` to 6",
     "gambit ~~list's destroy notice to its editor child, which sets the child's `+0x331` to 6~~ pick list "
     "`0056B4D0`'s destroy notice to the editor that created it, which sets its own `+0x331` to 6 *(corrected "
     "2026-10-02, OPUS: `0056B4D0+0x4F`–`0056B4D0+0x79` send `{0x121}` to `[self+0xC8]`, the editor, whose `+0xE8` "
     "`0056B350+0x7A` set to the list)*"),

    # CV-20: 002778C0 sends {30} through 002753F0 (002778C0+0x45E), which recurses over the children - a broadcast.
    (MP, "`rsi`, immediately after a `{31}` carrying a pointer.",
     "`rsi` and, through `002753F0` (`002778C0+0x45E`), to every descendant of it *(corrected 2026-10-02, OPUS: "
     "`002753F0+0x15`–`002753F0+0x2B` recurse over the children — a subtree broadcast)*, immediately after a `{31}` "
     "carrying a pointer."),

    # CV-21: 002470D0 pushes through 00244640 (002470D0+0x40), then switches focus through 00244830 (+0x52).
    (MP, "tail-calls `002470D0`, which pushes the widget onto the focus stack (`00244830`)",
     "tail-calls `002470D0`, which pushes the widget onto the focus stack ~~(`00244830`)~~ (`00244640`, at "
     "`002470D0+0x40`) and then switches focus to it (`00244830`, at `002470D0+0x52`) *(corrected 2026-10-02, OPUS: "
     "`00244830` sends `{9}`/`{8}` and stores `0208EBC0`; it pushes nothing)*"),

    # CV-22: 00246AD0's last instruction is 00246AD0+0x140 ret: 321 B.
    (AN, "All 330 bytes disassembled.",
     "All ~~330~~ 321 bytes disassembled *(corrected 2026-10-02, OPUS: the last instruction is `00246AD0+0x140` "
     "`ret`)*."),

    # CV-23: bit 14 = storage the object does not own (pool slot and in-place construct, 00245000+0x9).
    (CW, "i.e. **bit 14 means \"this object came out of the fixed pool\"** |",
     "i.e. ~~**bit 14 means \"this object came out of the fixed pool\"**~~ **bit 14 means \"storage this object does "
     "not own\"** — the fixed pool's slots and the in-place construct alike *(corrected 2026-10-02, OPUS: "
     "`00245000+0x9` passes 1 as the fifth argument too, and the release `002482E0+0x105`–`002482E0+0x109` then only "
     "clears bit 14 and zeroes `+0xA2` instead of freeing)* |"),

    # ---------------------------------------------------------------- Request router and the command menu
    # CV-24: Triangle (mask 0x1000) posts (2, 0) at 00253C70+0xF1..+0x108; the 0x21 posts follow cmp ebp, ebx (ebx = 1).
    (RR, "Triangle path's default parameter**, produced twice inside",
     "~~Triangle path's default parameter~~ default parameter of the pad-mask `1` and `2` paths**, produced twice "
     "inside *(corrected 2026-10-02, OPUS: Triangle, mask `0x1000`, posts request 2 with parameter 0 — "
     "`00253C70+0xF1` `cmp ebp, 0x1000` to `00253C70+0x108`; both `0x21` posts follow `cmp ebp, ebx` with "
     "`ebx = 1` from `00253C70+0xA4`, at `00253C70+0x17C` and `00253C70+0x291`)*"),

    # CV-26: 02092734 == 1 refuses everything; any route passing flag 1 to 00252B40 sets it.
    (CR, "| `00254B71`, before any policy read | a generic request is already open |",
     "| `00254B71`, before any policy read | ~~a generic request is already open~~ a request posted with flag 1 is "
     "open *(corrected 2026-10-02, OPUS: `00252B40` stores its second argument in `02092734`, and `00254B50+0x2A` "
     "refuses every id while it is 1; callers passing 1 include request 3 `0035D980+0xCA`, request 24's widget "
     "`0035D6B0+0x175`, `0027EFA0+0x35`, `0035C960+0xA9` and `003F4E70+0x19C`)* |"),

    # CV-27: the open arm's duration is 0xC8 ms, or 1 when bit 15 of the record's first dword is set.
    (RR, "duration scaled from the request parameter)",
     "duration ~~scaled from the request parameter~~ of 200 ms, or 1 ms when bit 15 of the request record's first "
     "dword is set *(corrected 2026-10-02, OPUS: `0027FB70+0x213` `mov ebp, 0xc8`, `0027FB70+0x224` `bt r15d, 0xf`, "
     "`0027FB70+0x229` `cmovb ebp, edi` with `edi = 1`; ×60/1000 to frames at `0027FB70+0x2E4`)*)"),

    # CV-29: the open table 00280090 sends 7-9, 13, 20 to the default and 16 to its own arm (0027FB70+0x45A).
    (RR, "In the generic widgets these ids reach only shared arms; 16",
     "In the generic widgets ~~these ids reach only shared arms~~ 7–9, 13 and 20 reach only the default of the open "
     "table at `0027FB70+0x520` (`0027FB70+0x49E`), and 16 its own arm (`0027FB70+0x45A` `mov dword ptr [rbx+0xcc], 2`, then "
     "the same default) *(corrected 2026-10-02, OPUS: the 21-entry table read from the image)*; 16"),

    # CV-30: [0209BE80]+0x10FB0 is a pointer slot; the 0x760-byte widget is built on the heap by 002D5030.
    (RR, "The router's own arm `0028E970` releases and rebuilds a `0x760`-byte widget at `0209BE80 + 0x10FB0`",
     "The router's own arm `0028E970` releases and rebuilds a `0x760`-byte widget ~~at `0209BE80 + 0x10FB0`~~ whose "
     "pointer it keeps at `[0209BE80] + 0x10FB0` *(corrected 2026-10-02, OPUS: `0028E970+0xF` reads the qword there, "
     "`0028E970+0x1B` tears the old widget down, and `0028E970+0x60` stores the new one, which `002D5030` builds "
     "through `00244F50` with `ecx = 0x760`)*"),
    (RR, "That arm releases the widget at `0209BE80 + 0x10FB0` and builds a new",
     "That arm releases the widget ~~at `0209BE80 + 0x10FB0`~~ whose pointer sits at `[0209BE80] + 0x10FB0` and "
     "builds a new"),
    (RR, "`0x760`-byte one there. Verb",
     "`0x760`-byte one ~~there~~ on the heap, storing its pointer back *(corrected 2026-10-02, OPUS: `0028E970+0x60`; "
     "`+0x10FB0` is a pointer slot of the `0x10FD0`-byte block)*. Verb"),

    # CV-31: the +0x2FE0 read sits in the per-frame message-2 arm (00276D30+0x270); {2} comes every pass.
    (SEL, "is the command-confirm path:",
     "is ~~the command-confirm path~~ the menu's per-frame message-2 arm (`00276D30+0x270`) *(corrected 2026-10-02, "
     "OPUS: message 2 is the generation reconcile, `00248030+0xBF`, which reaches every widget once "
     "`00250540+0x4D` has flipped the parity for the pass)*:"),

    # CV-32: 0027E050 installs six procedures (its lea sites).
    (SEL, "five installed procedures (owner re-status 2026-10-01, OPUS; documented_rule READY)\n",
     "five installed procedures (owner re-status 2026-10-01, OPUS; documented_rule READY)   # <- corrected 2026-10-02, "
     "OPUS - six installed procedures, not five: 0027E050's lea sites name 00276BE0, 0027D240, 0027CE70, 0027D5C0, "
     "0027E530 and 0027BC10\n"),

    # CV-33: 01E0C1D8/01E0C1DC are the screen width/height; 00272250 projects to screen coordinates.
    (SEL, "`00272180` + the `01E0C1D8`/`01E0C1DC` state cells — menu-mode read/write |",
     "`00272180` + ~~the `01E0C1D8`/`01E0C1DC` state cells — menu-mode read/write~~ the screen width and height "
     "`01E0C1D8`/`01E0C1DC` — a projection to screen coordinates *(corrected 2026-10-02, OPUS: "
     "`00272250+0xE`–`00272250+0x3B` compute `((v − 0x8000) >> 4)` plus half the width or height)* |"),

    # ---------------------------------------------------------------- Text engine
    # CV-34: the Final prefix overwrites m[0][0] with 00229DE0() (00214210+0x5C) and zeroes the rest of row 0.
    (CT, "    m = identity from 008C5F80 / 008C5F90 / 008C5FB0 / 008C5FD0\n",
     "    m = identity from 008C5F80 / 008C5F90 / 008C5FB0 / 008C5FD0   # <- corrected 2026-10-02, OPUS - then "
     "m[0][0] = 00229DE0() (height x 16/9 / width) and the rest of row 0 = 0 (00214210+0x5C, +0x62, +0x6B); 00229DE0 "
     "takes no argument (jmp 00183280)\n"),

    # CV-36: ShadowFinal 002143E0 never reaches 002142A0 (it ends in jmp [r10+0x20]).
    (DG, "- **`002142A0` is the single choke point** for all four text variants",
     "- **`002142A0` is the single choke point** for ~~all four~~ three of the four text variants *(corrected "
     "2026-10-02, OPUS: ShadowFinal `002143E0` never reaches it — its body ends in an indirect `jmp qword ptr "
     "[r10 + 0x20]` — while the Shadow body tail-jumps in at `00214540+0x4D` and Final through its tail)*"),

    # CV-37: two of the seven callers are single-shot (002B1FB0+0xCE, 002B5730+0xF3).
    (TL, "\"call me again\".** All seven call sites use the identical shape:",
     "\"call me again\".** ~~All seven call sites use the identical shape:~~ Five of the seven call sites use this shape; `002B1FB0` and "
     "`002B5730` call once and read only the advanced cursor *(corrected 2026-10-02, OPUS: `002B1FB0+0xCE`, "
     "`002B5730+0xF3`; no `test eax` follows)*:"),
    (TL, "and the identical `test/je` at all seven call sites | 1 |",
     "and the ~~identical `test/je` at all seven call sites~~ `test/je` at five of the seven call sites *(corrected "
     "2026-10-02, OPUS: `002B1FB0+0xCE` and `002B5730+0xF3` call once)* | 1 |"),
    (CT, "by each of its seven callers.",
     "by ~~each of its seven callers~~ five of its seven callers; `002B1FB0` and `002B5730` call it once *(corrected "
     "2026-10-02, OPUS: `002B1FB0+0xCE`, `002B5730+0xF3`; I-1)*."),

    # CV-38: an out-of-range or do-nothing selector returns 1 with the cursor on the selector byte (002AC5F0+0xA2A).
    (TL, "002AD029  ja    0x2acfc2                  ; outside 0x20..0x70 -> consume and continue\n",
     "002AD029  ja    0x2acfc2                  ; outside 0x20..0x70 -> consume and continue   <- corrected "
     "2026-10-02, OPUS - not consumed: the cursor already points at the selector byte (002AC5F0+0xA2A), so the caller "
     "prints it\n"),
    (TL, "| `0` `_` | `002ACFC2` | **consume and continue, no action** | | |",
     "| `0` `_` | `002ACFC2` | ~~**consume and continue, no action**~~ **printed**: return 1 with the cursor on the "
     "selector byte *(corrected 2026-10-02, OPUS: `002AC5F0+0xA2A` stores the cursor at the selector before the "
     "dispatch, and both selectors map to the exit `002AC5F0+0x9D2`)* | | |"),
    (CT, "    if s - 0x20 > 0x50: return 1                          # 002AD029  consume and continue\n",
     "    if s - 0x20 > 0x50: return 1                          # 002AD029  consume and continue   <- corrected "
     "2026-10-02, OPUS - not consumed: *cursor already points at the selector (002AC5F0+0xA2A), so the caller prints "
     "it\n"),

    # CV-39 (+0x94 half): 002B1F20 reads +0x94 as a signed word.
    (CT, "  +0x94  f32   the width justification subtracts from\n",
     "  +0x94  f32   the width justification subtracts from   <- corrected 2026-10-02, OPUS - a signed word, not f32: "
     "002B1F20+0x1C and 002B1F20+0x4A read it with movsx eax, word ptr [rcx+0x94]\n"),

    # CV-40: 00254A10 is 1 for {0,7,8,10,11} of the same dword, so the 26-unit branch never runs.
    (TL, "`0x07` 26 units when the option `00254A10` is clear and the frame mode `00229E40` is 7, otherwise",
     "`0x07` 26 units when the option `00254A10` is clear and ~~the frame mode~~ the cached locale value `00229E40` "
     "(`01E02814`) is 7 — a branch that never runs, since `00254A10` returns 1 for 7 (`00254A10+0xE` mask `0xD81`) "
     "*(corrected 2026-10-02, OPUS: `002AC5F0+0x5DA`–`002AC5F0+0x5ED`)* — otherwise"),

    # CV-41: 001DD110 returns the constant 008C5B38 whatever the object; the object supplies width/height only.
    (DG, "K is `16/9` (`008C5B38`) unless the `01F82D18` object supplies its own value",
     "K is `16/9` (`008C5B38`) ~~unless the `01F82D18` object supplies its own value~~ in every case: with the object "
     "present `00183280` calls `001DD110`, which loads the same constant *(corrected 2026-10-02, OPUS: `001DD110` is "
     "`movss xmm0, [008C5B38]` / `ret`; the object supplies the width and height through `00182EB0`)*"),

    # CV-42: 00215790 allocates count x 48 (00215790+0x16/+0x19); 002157C0 indexes idx x 48.
    (DG, "The record array at `+0x18` is 24-byte-stride,",
     "The record array at `+0x18` is ~~24-byte-stride~~ 48-byte-stride *(corrected 2026-10-02, OPUS: "
     "`00215790+0x16`/`00215790+0x19` allocate count × 48, and `002157C0+0x22`–`002157C0+0x3C` index `idx × 48`)*,"),

    # CV-43: slots 4 and 5 are shared by all four vtables; 6 by three (Final 00213B40); 10 has four bodies.
    (DG, "and the four shared slots 4, 5, 6\n      and 10 manage them.",
     "and ~~the four shared slots 4, 5, 6~~ slots 4 and 5 (shared by all four classes), 6 (shared by three; Final "
     "has `00213B40`)\n      ~~and 10~~ and 10 (four bodies) manage them *(corrected 2026-10-02, OPUS: read from the "
     "vtables `00906DE8`, `00906E50`, `00906EB8` and `00906F20`)*."),

    # CV-45: the ! arm has no parser (002AC5F0+0xBF5 inc qword [rdi]); the shared arm advances by 002AEB20's return.
    (CT, "Every arm ends `lea rdx, [rsp+0x40]` / `call <parser>` / `add qword ptr [rdi], rax`",
     "~~Every arm ends~~ Every parser-carrying arm ends `lea rdx, [rsp+0x40]` / `call <parser>` / "
     "`add qword ptr [rdi], rax` *(corrected 2026-10-02, OPUS: the `!` arm has no parser and advances by one, "
     "`002AC5F0+0xBF5` `inc qword ptr [rdi]`; the shared arm at `002AC5F0+0x1C01` advances by `002AEB20`'s return)*"),

    # CV-47: '/' sets +0xA0 = trunc(v/30) above 30 (002A8C50+0x5BE..+0x60D), 1 at most 30 (002A8C50+0x75E).
    (NF, "| `0x2F` | `/` | a magic-divide result; also sets `byte [state + 0xA0] = 1` |",
     "| `0x2F` | `/` | a magic-divide result; ~~also sets `byte [state + 0xA0] = 1`~~ a payload above 30 sets "
     "`+0x9C = 30` and `+0xA0 = trunc(v / 30)`, halved with a floor of 1 when `00248F20()` returns 1; a payload of at "
     "most 30 sets `+0xA0 = 1` *(corrected 2026-10-02, OPUS: `002A8C50+0x5BE`–`002A8C50+0x60D` and "
     "`002A8C50+0x75E`)* |"),

    # CV-48: the index is masked to 0x7F before 0039BA00's own & 0x1FF (003FFAB0+0x1A).
    (NF, "`out` is the FIRST BYTE of entry `tag[2] & 0x1FF` of the unnamed 5-byte-stride table",
     "`out` is the FIRST BYTE of entry ~~`tag[2] & 0x1FF`~~ `tag[2] & 0x7F` *(corrected 2026-10-02, OPUS: "
     "`003FFAB0+0x1A` `and r8b, 0x7f` masks the index before `0039BA00`'s own `and eax, 0x1ff` at `0039BA00+0xA`, so "
     "only entries 0–127 are reached)* of the unnamed 5-byte-stride table"),

    # CV-50: 002A9F00 copies 0xD0 bytes (thirteen movups loads, 002A9F00+0x29..+0xC3).
    (NF, "The function also opens by copying **`0x100` bytes of render state** to its stack frame in unrolled",
     "The function also opens by copying **~~`0x100`~~ `0xD0` (208) bytes of render state** *(corrected 2026-10-02, "
     "OPUS: thirteen 16-byte `movups` loads, `002A9F00+0x29`–`002A9F00+0xC3`)* to its stack frame in unrolled"),

    # CV-53: the pointers sit at -0x48, -0x80 and -0x78; the qword at -0x50 is zero.
    (NF, "that, at `-0x50` and `-0x80`, are **function pointers** — `002AAE40`, `002A8C50`,",
     "that, at ~~`-0x50` and `-0x80`~~ `-0x48`, `-0x80` and `-0x78` in the order listed *(corrected 2026-10-02, OPUS: "
     "the qwords at `00916518`, `009164E0` and `009164E8`; the one at `-0x50` is zero)*, are **function pointers** — "
     "`002AAE40`, `002A8C50`,"),

    # CV-54: in selector order 0x25/0x26/0x27 the arms are left/right/centre (002B1F20+0x7A, +0x4A, +0x1C).
    (TL, "returns `(word[+0x94] - xmm1)/2 + byte[+0x99]` — the left/center/right",
     "returns `(word[+0x94] - xmm1)/2 + byte[+0x99]` — the ~~left/center/right~~ left/right/centre *(corrected "
     "2026-10-02, OPUS: in selector order `0x25`, `0x26`, `0x27` — `002B1F20+0x7A` the margin alone, "
     "`002B1F20+0x4A` the width subtracted, `002B1F20+0x1C` half of it)*"),

    # CV-57: 001FDB90 ends at 001FDB90+0x7E ret; the second walk and the value store are 001FDC10's.
    (FK, "`001FDC02`), and the second arm repeats the walk off `001FC420`",
     "`001FDC02`) and returns (`001FDB90+0x7E` `ret`); ~~and the second arm repeats the walk off `001FC420`~~ the next "
     "function, `001FDC10`, repeats the walk off `001FC420` *(corrected 2026-10-02, OPUS: the two sites cited next "
     "are `001FDC10+0x1D` and `001FDC10+0x56`, past `001FDB90`'s last instruction)*"),

    # CV-58: 001FDDD0 is reached: 002AC2F0+0x23F -> 0017F8E0 -> 001E9780 -> 001FDDD0, gated on +0x20 != -1.
    (FK, "(structurally unreachable — see §3). Plus `[r14]` flag bits —",
     "(~~structurally unreachable~~ reachable: `002AC2F0+0x23F` calls `0017F8E0` → `001E9780` → `001FDDD0` when the "
     "record's `+0x20` word is not −1, `002AC2F0+0x237` *(corrected 2026-10-02, OPUS)* — see §3). Plus `[r14]` flag "
     "bits —"),

    # ---------------------------------------------------------------- Layout parameters
    # CV-59: 002A6190 reads three keys itself (layout-key-readers.tsv rows, checked at the bytes).
    (MW, "| reads no key directly; its helpers",
     "| ~~reads no key directly~~ reads three keys itself — `MessageWinMaskBottom` (`002A6190+0x234`), "
     "`MsgWinSignalOffsetY` (`002A6190+0x400`) and `MessageWinMaskTop` (`002A6190+0x738`) *(corrected 2026-10-02, "
     "OPUS: the `layout-key-readers.tsv` rows, each read at the bytes)*; its helpers"),

    # CV-60 (object): 0029E770 writes [0209C498]+0xC0/+0xC2.
    (LP, "writes a word pair `+0xC0/+0xC2` on the `[0209C4A0]` pane-state block — the inline mutation every pane "
         "updater performs.",
     "writes a word pair `+0xC0/+0xC2` on ~~the `[0209C4A0]` pane-state block — the inline mutation every pane updater "
     "performs.~~ `[0209C498]`, the key-signal HUD object *(corrected 2026-10-02, OPUS: `0029E770` loads `[0209C498]`, "
     "as the falsification note above says; its four callers are `002BA700`, `002D5EB0`, `0055E9E0` and "
     "`005789D0`)*."),

    # CV-61: BaseX goes to +0xC0 (0029E110+0x151); the +0x160 lea only forms an argument.
    (BH, "`BaseX` `movzx` word → the `+0x160` record (`0029E251`)",
     "`BaseX` `movzx` word → ~~the `+0x160` record~~ `+0xC0` *(corrected 2026-10-02, OPUS: `0029E110+0x151` "
     "`mov word ptr [rbx+0xc0], ax`; the `lea rcx, [rbx+0x160]` between them only forms an argument)* (`0029E251`)"),

    # CV-62: 002C99A0's r8d is a 0/1 flag (002C99A0+0x17), not a duration.
    (LP, "`002C9490` (band build) or `002C99A0` / `002CD7F0` (band animation), each helper binding one",
     "`002C9490` (band build) or `002C99A0` / `002CD7F0` (band animation) *(corrected 2026-10-02, OPUS: not for "
     "`002C99A0` — its `r8d` is a 0/1 flag, `002C99A0+0x17` `cmp ebx, 1` gating a second call to `002CD800`, and its "
     "callers pass 0 or 1, e.g. `00280D20+0x58` `mov r8d, 1`)*, each helper binding one"),

    # CV-63: 002CE2F0 ends at 002CE2F0+0x77; 002CE370 is the next function, the handler 00244F50 takes in rdx.
    (LP, "and `rdx` = the literal\nblock at `002CE370` (the bytes immediately after the body, `002CE33D`",
     "and `rdx` = ~~the literal~~ the handler\n~~block at~~ `002CE370` ~~(the bytes immediately after the body,~~ (the "
     "next function — `002CE2F0` ends at its `ret`, `002CE2F0+0x77` *(corrected 2026-10-02, OPUS: " + FACTORY + ")*, "
     "`002CE33D`"),

    # CV-64: 0x88888889 with sar 5 divides by 60 (002D4A40+0xC5..+0xDA).
    (LP, "`(result * 0x3E8)` is magic-divided by 55 (`0x88888889`/`>>5`+sign) into",
     "`(result * 0x3E8)` is magic-divided by ~~55~~ 60 (`0x88888889`/`>>5`+sign; with `>>4` the same reciprocal "
     "divides by 30) *(corrected 2026-10-02, OPUS: `002D4A40+0xC5`–`002D4A40+0xDA`)* into"),

    # CV-65: 003BD950 is a row probe (003BD950+0x36..+0x51), not an allocator.
    (LP, "aligned up to 4, `003BD950` allocates it into `+0xF0`,",
     "aligned up to 4, ~~`003BD950` allocates it into `+0xF0`,~~ `003BD950`, a row probe and not an allocator, runs on it *(corrected "
     "2026-10-02, OPUS: `003BD950` walks the `[rcx]`-counted 8-byte rows backward, comparing `00265270()` with each "
     "row's word and testing its flag through `0032A8A0`, `003BD950+0x36`–`003BD950+0x51`)*,"),

    # CV-66: 001CA600's last instruction is 001CA600+0x1FFE ret: 8,191 B.
    (LP, "The loader is `001CA600` (8,186 bytes),",
     "The loader is `001CA600` (~~8,186 bytes~~ 8,191 bytes *(corrected 2026-10-02, OPUS: its last instruction is "
     "`001CA600+0x1FFE` `ret`)*),"),

    # CV-68: the lerp pairs are per gauge (002C5F90+0xB8/+0xBE enemy, +0x26/+0x2C other).
    (BH, "| `mov eax, [01E0CEF4]`; `sub eax, [01E0CF24]`, `cvtdq2ps xmm1, xmm1` |",
     "| ~~`mov eax, [01E0CEF4]`; `sub eax, [01E0CF24]`~~ two lerps, one per gauge: `002C5F90+0xB8`/`002C5F90+0xBE` "
     "`mov eax, [01E0CEF4]` / `sub eax, [01E0CEE4]` (enemy Max − Min) and `002C5F90+0x26`/`002C5F90+0x2C` "
     "`mov eax, [01E0CF34]` / `sub eax, [01E0CF24]` (other Max − Min) *(corrected 2026-10-02, OPUS: the row joined one "
     "gauge's Max with the other's Min)*, `cvtdq2ps xmm1, xmm1` |"),

    # ---------------------------------------------------------------- Screens
    # CV-70: 0023BD40 is 2,091 B (last instruction 0023BD40+0x82A ret).
    (CF, "`0023BD40` (~350 B) — a config-screen row handler under a stack cookie.",
     "`0023BD40` ~~(~350 B)~~ (2,091 B *(corrected 2026-10-02, OPUS: its last instruction is `0023BD40+0x82A` "
     "`ret`)*) — a config-screen row handler under a stack cookie."),

    # CV-71: the static 00914710 table is stepped by 0x14 (0023BD40+0x308).
    (CF, "+ i×0x20` uses the same `0x20` stride as §4's static",
     "+ i×0x20` ~~uses the same `0x20` stride as §4's static~~ uses a `0x20` stride, not the `0x14` stride of §4's static "
     "*(corrected 2026-10-02, OPUS: `0023BD40+0x308` `add r12, 0x14` steps that table, whose first dwords read 0, 1, 2 "
     "at 20-byte spacing)*"),

    # CV-72: 0209EC30 / 0209EA28 have no references; the code loads 0209AC30 (002CE7A0+0xD) and 0208EA28 (00280DE0+0xBD).
    (CF, "take `[[0209EC30]+0x30]`,",
     "take ~~`[[0209EC30]+0x30]`~~ `[[0209AC30]+0x30]` *(corrected 2026-10-02, OPUS: `002CE7A0+0xD` loads "
     "`[0209AC30]`; nothing references `0209EC30`)*,"),
    (CF, "then `00246AD0(0209EA28-obj, self)`",
     "then ~~`00246AD0(0209EA28-obj, self)`~~ `00246AD0(0208EA28-obj, self)` *(corrected 2026-10-02, OPUS: "
     "`00280DE0+0xBD` loads `[0208EA28]`; nothing references `0209EA28`)*"),

    # CV-73 (arm count): the 282-entry table holds 226 distinct arms plus a default shared by 56 ids.
    (CF, "Whatever else lives in the other 266 arms,",
     "Whatever else lives in the other 266 ~~arms~~ ids *(corrected 2026-10-02, OPUS: the 282-entry table holds 226 "
     "distinct arms and a default, `001D1660+0x359A`, that 56 ids share)*,"),

    # CV-76: 00241D40 is the widget handler 002465F0 takes in r8 (00241BF0+0x7C).
    (CF, "&out)` runs the table-driven init with the `00241D40` descriptor",
     "&out)` ~~runs the table-driven init with the `00241D40` descriptor~~ constructs a `0x3D0`-byte widget whose "
     "handler is `00241D40` *(corrected 2026-10-02, OPUS: `002465F0` takes the handler in `r8` — `00241BF0+0x7C` "
     "`lea r8, [00241D40]`)*"),

    # CV-79: the four dwords are layout keys written through the slot pointers 001AF470 installs.
    (SH, "values are the `.data` dwords `01E0C3CC`, `01E0C3D0`, `01E0C3BC`, `01E0C3E8`, which no instruction writes).",
     "values are the `.data` dwords `01E0C3CC`, `01E0C3D0`, `01E0C3BC`, `01E0C3E8`, ~~which no instruction writes~~ "
     "the layout keys `DeftopBlackBandH`, `DefUnderBlackBandH`, `PartyBlackBandGradH` and `BlackBandAnimTime`, "
     "written through the slot pointers `001AF470` installs, e.g. `001AF470+0x214` `lea rax, [01E0C3D0]` *(corrected "
     "2026-10-02, OPUS: `layout-key-slots.tsv`)*)."),

    # CV-80: 005666D4 (00566680+0x54) is the id-18 arm; the id-12 arm (00566680+0x114) never branches into it.
    (SD, "the five sort modes; each walks the parent's `[+0xC0]+0x180`-indexed option table at `0x1E` stride 8 (`005666D4`–`005666F3`) via "
         "`00567690`",
     "the five sort modes; ~~each walks the parent's `[+0xC0]+0x180`-indexed option table at `0x1E` stride 8 (`005666D4`–`005666F3`) via "
     "`00567690`~~ *(corrected 2026-10-02, OPUS: that walk opens the id-18 arm — the dispatch sends 18 to "
     "`00566680+0x54` — and the id-12 arm `00566680+0x114` never branches into `00566680+0x54`–`00566680+0x73`)*"),

    # CV-82: 003C2200 tails into 003C26C0, which fills the matching slot (003C26C0+0x5C..+0x7F).
    (MS, "releases the slot (`003C2200`) and destroys the page.",
     "~~releases the slot (`003C2200`)~~ fills the slot through `003C2200`, a tail into `003C26C0` that parses the "
     "loaded block into the matching slot (`003C26C0+0x5C`–`003C26C0+0x7F`) *(corrected 2026-10-02, OPUS: the §2.6 "
     "correction below)*, and destroys the page."),
    (MS, "**16** (resource batch complete) releases the slot through `003C2200` and rebuilds",
     "**16** (resource batch complete) ~~releases the slot through `003C2200`~~ fills the slot through `003C2200` "
     "*(corrected 2026-10-02, OPUS: `003C2200` tails into `003C26C0`, a populate — §2.6's correction)* and rebuilds"),

    # CV-83: 002C9430 returns a black-band extent (002C9430+0x10/+0x19 pick the band object).
    (MS, "— `002C9430(0)`/`(1)` read both pads;",
     "— `002C9430(0)`/`(1)` ~~read both pads~~ return the top and bottom black-band extents *(corrected 2026-10-02, "
     "OPUS: `002C9430+0x10`/`002C9430+0x19` pick `[0209AC30]+0x2B8` or `+0x2C8`, and `002C9430+0x2D`–"
     "`002C9430+0x4F` return its extent; no controller read)*;"),
    (MS, "`002C9430` ×2 (both pads) |",
     "`002C9430` ×2 (~~both pads~~ the two band extents *(corrected 2026-10-02, OPUS)*) |"),
    (MS, "pad/direction bytes and `002C9430` pads, scrolls",
     "pad/direction bytes and ~~`002C9430` pads~~ the `002C9430` band extents *(corrected 2026-10-02, OPUS)*, "
     "scrolls"),

    # CV-85: 003BD9F0 requires bits 8 AND 9 set (003BD9F0+0x3F, +0x4C/+0x50).
    (QL, "`dword[+0xD0]` requires bit8 set and bit9 clear else 0;",
     "`dword[+0xD0]` requires bit8 ~~set and bit9 clear~~ and bit9 both set *(corrected 2026-10-02, OPUS: "
     "`003BD9F0+0x3F` `bt eax, 8`, `003BD9F0+0x4C` `bt eax, 9` / `003BD9F0+0x50` `jae` to the 0 return)* else 0;"),

    # CV-86: 0037F050 compares 02AED490 with zero (0037F050+0x2).
    (MS, "| 13 B compare on the `0208EA20` region |",
     "| 13 B compare ~~on the `0208EA20` region~~ of `02AED490` with zero *(corrected 2026-10-02, OPUS: "
     "`0037F050+0x2` `cmp qword ptr [02AED490], rax`)* |"),

    # CV-87: 0x120000 + 0x1B4310 = 002D4310.
    (MS, "six-arm jump table at `02ED4310` (`00120000` +",
     "six-arm jump table at ~~`02ED4310`~~ `002D4310` *(corrected 2026-10-02, OPUS: the operand at `002D3BA0`'s "
     "`mov ecx, [r8 + rax*4 + 0x1b4310]`)* (`00120000` +"),

    # CV-88: the case table 002BC24C starts past 002BAF80's last instruction (002BAF80+0x12C9 ret).
    (MS, "true of `002B7B80` by accident, false of `002BAF80`, whose\n"
         "case table sits inside its declared extent, so that assertion",
     "true of `002B7B80` by accident, ~~false of `002BAF80`, whose~~ and true of `002BAF80` too, whose\n"
     "case table ~~sits inside its declared extent~~ starts two bytes past its last instruction, `002BAF80+0x12C9` "
     "`ret` (corrected 2026-10-02, OPUS), so that assertion"),

    # CV-91: 005528C0 only reads 02CA8F38; the writers are 00550400 and 00552230.
    (MS, "— installs the panes, owns `02CA8F38` |",
     "— installs the panes, ~~owns `02CA8F38`~~ reads `02CA8F38`, which only the installer `00550400` "
     "(`00550400+0x55`) and `00552230` (`00552230+0x5`) write *(corrected 2026-10-02, OPUS)* |"),

    # CV-92: pop at self + 0xD4 + 6(n-1) (00575870+0xB5..+0xBD, 0x6A in words); push at +0xD4, +0xD6+6n, +0xD8+6n.
    (QL, "(`00575A50` on `self + 0x6A + 6*(+0xD3 - 1)`)",
     "(`00575A50` on ~~`self + 0x6A + 6*(+0xD3 - 1)`~~ `self + 0xD4 + 6*(+0xD3 - 1)` *(corrected 2026-10-02, OPUS: "
     "`00575870+0xB5`–`00575870+0xBD` form `2 × (0x6A + 3n)`, so `0x6A` is in words)*)"),
    (QL, "onto a 3-deep stack at `+0xD4`/`+0xD6`/`+0x48` counted by `+0xD3`",
     "onto a 3-deep stack at ~~`+0xD4`/`+0xD6`/`+0x48`~~ `+0xD4` (the kind byte, at a fixed offset), `+0xD6 + 6n` and "
     "`+0xD8 + 6n` *(corrected 2026-10-02, OPUS: `00575A50+0x86`–`00575A50+0xB6`; the third word's index is "
     "`(n + 0x24) × 6`)* counted by `+0xD3`"),

    # CV-93: bit 0x40 is set by 005776D0 (005776D0+0x20..+0x28), called only from 0056F2A0.
    (QL, "(bit `0x40`, set by the opening path, plus the three arm bits)",
     "(bit `0x40`, set ~~by the opening path~~ by `005776D0`, whose only caller is `0056F2A0` *(corrected 2026-10-02, "
     "OPUS: `005776D0+0x20`–`005776D0+0x28` `and eax, 0xFFFFFC7F` / `or eax, 0x40`, which also clears the three arm "
     "bits)*, plus the three arm bits)"),

    # CV-94: while collecting, 0055B310 never updates the previous nibble, so a 33rd change is found again later.
    (RM, "collects **exactly 32**\n  changed squares, silently dropping the 33rd.",
     "collects **exactly 32**\n  changed squares~~, silently dropping the 33rd~~; a 33rd is deferred, not lost — while "
     "collecting, the sweep leaves every square's previous nibble as it was, so a later sweep finds it again "
     "*(corrected 2026-10-02, OPUS: `0055B310+0x70`–`0055B310+0x78` stop at 32, and the previous-nibble update "
     "`0055B310+0x88`–`0055B310+0x96` runs only when not collecting)*."),

    # CV-99: 02EBF190 and 0209AC30 hold pointers (00323600+0x19, 00283E40+0x26).
    (LG, "stats block `02EBF190 + 8 + slot * 0x1C8`,",
     "stats block ~~`02EBF190 + 8 + slot * 0x1C8`~~ `[02EBF190] + 8 + slot * 0x1C8` *(corrected 2026-10-02, OPUS: "
     "`02EBF190` holds a pointer — `00323600+0x19` `mov rax, [02EBF190]`, then `00323600+0x20` `add rax, 8`)*,"),
    (LG, "indexes `qword[0209AC30 + idx*8 + 0xAC8]`",
     "indexes ~~`qword[0209AC30 + idx*8 + 0xAC8]`~~ `qword[[0209AC30] + idx*8 + 0xAC8]` *(corrected 2026-10-02, OPUS: "
     "`00283E40+0x26` loads the pointer `[0209AC30]`, `00283E40+0x43` indexes it)*"),

    # CV-100: 0055A180 tests +0x570 & 2 (0055A180+0x6), bit 1.
    (LG, "`+0x570` bit 2 set tail-enters `0055A1F0(this)`",
     "`+0x570` ~~bit 2~~ bit 1 (`& 2`) set tail-enters `0055A1F0(this)` *(corrected 2026-10-02, OPUS: `0055A180+0x6` "
     "`test byte ptr [rcx+0x570], 2`)*"),

    # CV-101: 0055B2B0's columns are +0x559 (0055B2B0+0x1A).
    (LW, "loop over `+0x55A` rows/`+0x554` cols, no calls |",
     "loop over `+0x55A` rows/~~`+0x554`~~ `+0x559` cols *(corrected 2026-10-02, OPUS: `0055B2B0+0x1A` "
     "`movsx edx, byte ptr [rcx+0x559]`)*, no calls |"),

    # CV-102: 0055DD70 calls 0055BFF0 (0055DD70+0x19) and returns at 0055DD70+0x12C.
    (LW, "| sweep wrapper — tail `0055BFF0` |",
     "| sweep ~~wrapper~~ driver — ~~tail `0055BFF0`~~ sets `+0x570` bit 0, calls `0055BFF0` (`0055DD70+0x19`) and "
     "walks the result before its own `ret` (`0055DD70+0x12C`) *(corrected 2026-10-02, OPUS)* |"),

    # CV-107: the editor builds the list (0056B350+0x7A stores it at the editor's +0xE8); 289 goes child -> creator.
    (GB, "calls the `+0xC8` editor child's first vtable slot (`0056B516`–`0056B549`) — the parent→child destroy "
         "notification |",
     "calls the `+0xC8` ~~editor child's~~ editor's — its creator's — first vtable slot (`0056B516`–`0056B549`) — the "
     "~~parent→child~~ child→creator destroy notification *(corrected 2026-10-02, OPUS: the editor's `00567D80` "
     "builds this list through `0056B350`, which stores it at the editor's `+0xE8`, `0056B350+0x7A`)* |"),

    # CV-109: 00572D80 is a resource requester (batch open, request, tail-jump to the seal).
    (HB, "| post-build cleanup — `00249580` |",
     "| ~~post-build cleanup — `00249580`~~ a resource requester: opens a batch (`00249580`), requests through "
     "`002491B0`/`00249210` (`00572D80+0x45`, `00572D80+0x6B`) and tail-jumps to the seal `00249410` "
     "(`00572D80+0x88`) *(corrected 2026-10-02, OPUS)* |"),

    # CV-110: 002527B0 stores its third argument into one of three banks at [020927C0] (002527B0+0x7..+0x69).
    (HB, "`002527B0`/`002CD7D0`/`002CD800`/`002CD880` resource release,",
     "~~`002527B0`/~~`002CD7D0`/`002CD800`/`002CD880` resource release *(corrected 2026-10-02, OPUS: `002527B0` is "
     "no release — it stores a value into one of three banks at `[020927C0]`, `002527B0+0x7`–`002527B0+0x69`)*,"),
    (LG, "and `002527B0(6, 4, armed)` re-lays the pane",
     "and `002527B0(6, 4, armed)` ~~re-lays the pane~~ stores `armed` into word 4 of bank 6 *(corrected 2026-10-02, "
     "OPUS: `002527B0` writes its third argument into one of three banks at `[020927C0]` — bank 6's words at `+0x30`, "
     "`002527B0+0x69`; it lays nothing out)*"),

    # CV-112: 0215FD40 lies past the file data with no direct writer; reads 002EEED0 and 002EF050+0x45 only.
    (HM, "advanced by a fixed\nstep (`0215FD40`) and wrapped",
     "advanced by a ~~fixed~~\nstep (`0215FD40`) *(corrected 2026-10-02, OPUS: not a constant — `0215FD40` lies past "
     "the image's file data and has no direct writer; its only references are the reads `002EEED0` and "
     "`002EF050+0x45`)* and wrapped"),

    # ---------------------------------------------------------------- Section 3.3: banners (CS-1 to CS-9)
    (RR, "**Status is PARTIAL:** the mechanism is fully documented",
     "~~**Status is PARTIAL:**~~ **Status is DOCUMENTED** *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" +
     ", owner re-status 2026-10-01)*: the mechanism is fully documented"),
    (NF, "**This document is `PARTIAL` and is the first system recovered from",
     "**This document is ~~`PARTIAL`~~ `DOCUMENTED` *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ")* and is "
     "the first system recovered from"),
    (MW, "**Status:** PARTIAL — this page documents where each `uisize.json` key of the message families lands",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ")* — this page "
     "documents where each `uisize.json` key of the message families lands"),
    (BH, "**Status:** PARTIAL — this page documents where each `uisize.json` key of the battle-HUD families",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ", owner re-status "
     "2026-10-01)* — this page documents where each `uisize.json` key of the battle-HUD families"),
    (MS, "**PARTIAL.** Read: which code is which screen,",
     "~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ")* Read: which code is "
     "which screen,"),
    (QL, "**PARTIAL.** Read: the procedure tree,",
     "~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: " + FM % "AUDITED" + ")* Read: the procedure tree,"),
    (AT, "**PARTIAL.** This is an atlas, not a reading.",
     "~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ")* This is an atlas, not "
     "a reading."),
    (UP, "**Status:** PARTIAL — the 25 atlas rows",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ", GI-6 answered "
     "2026-09-29)* — the 25 atlas rows"),
    (SD, "**Status:** PARTIAL — the four procedures'",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ", GI-4 answered "
     "2026-09-29)* — the four procedures'"),
    (HB, "**Status:** PARTIAL — both dispatch tables",
     "**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: " + FM % "DOCUMENTED" + ", GI-2 answered "
     "2026-09-29)* — both dispatch tables"),
    # CS-14: front matter falsification_passes against the body's pass section.
    (CR, "falsification_passes: 0\n",
     "falsification_passes: 0   # <- corrected 2026-10-02, OPUS - the body records Falsification pass 1 "
     "(2026-09-29, OPUS)\n"),

    # ---------------------------------------------------------------- Section 3.3: README tags (CS-3/4/5/7/11/12)
    readme_tag("**DOCUMENTED, tier 1.**", "**AUDITED, tier 1.**", "The bestiary's 3D monster"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "The board's runtime grid"),
    readme_tag("**DOCUMENTED, tier 1.**", "**AUDITED, tier 1.**", "Eight `DynGeo*` classes"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "Track map, location map and world map"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "The 80 menu widget procedures"),
    readme_tag("**DOCUMENTED, tier 1.**", "**AUDITED, tier 1.**", "`.ker` kerning pairs"),
    readme_tag("**PARTIAL, tier 1.**", "**AUDITED, tier 1.**", "`002AC5F0`, **the largest"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "One constructor builds every widget"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "The MsgWin layout-key readers"),
    readme_tag("**PARTIAL, tier 1.**", "**DOCUMENTED, tier 1.**", "The battle-HUD layout-key readers"),
    readme_tag("**DOCUMENTED, tier 1.**", "**AUDITED, tier 1.**", "231 layout parameters"),

    # ---------------------------------------------------------------- Section 3.3: stale "not read / open" lines
    # CS-18: the release frees a pool slot (002482E0+0x105..+0x109 clear bit 14 and zero +0xA2).
    (CW, "if any: nothing read shows a slot being released.",
     "if any: ~~nothing read shows a slot being released.~~ *(answered: the release frees it — `002482E0+0x105`–"
     "`002482E0+0x109` clear bit 14 and zero `+0xA2`, the byte the factory's free test reads; 2026-10-02, OPUS)*"),
    # CS-36: every arm is read (the arm table; 2026-09-14 and 2026-09-18).
    (TL, "**Their addresses are read; what all but four of them do is not.**",
     "**Their addresses are read; ~~what all but four of them do is not.~~** *(answered: see the arm table and the "
     "2026-09-14 and 2026-09-18 notes on this page; 2026-10-02, OPUS)*"),
    # CS-41: KE-1 closed 2026-09-27.
    (FK, "in practice.) What a `.fex` key names is not established (§7).",
     "in practice.) ~~What a `.fex` key names is not established (§7).~~ *(answered: see §7 — KE-1 closed 2026-09-27; 2026-10-02, "
     "OPUS)*"),
    # CS-44: Y-3 read from the code 2026-09-12.
    (LP, "(inferred from the file pair, not read from code — see **Y-3**):",
     "(~~inferred from the file pair, not read from code~~ *(answered: read from the code, Y-3 below, 2026-09-12; "
     "2026-10-02, OPUS)* — see **Y-3**):"),
    # CS-46: Y-2 answered 2026-09-20 (members/uisize-y2-join.tsv).
    (LP, "so **231 / 266 / 229 could not be recounted**.",
     "so ~~**231 / 266 / 229 could not be recounted**.~~ *(answered: recounted by the Y-2 join, "
     "`members/uisize-y2-join.tsv`, 2026-09-20; 2026-10-02, OPUS)*"),
    # CS-52: 0016D6A0 is the folded ret 0 stub.
    (CF, "0017DD39   call 0016D6A0()                 ; unread\n",
     "0017DD39   call 0016D6A0()                 ; unread   <- corrected 2026-10-02, OPUS - 0016D6A0 is ret 0, the stub "
     "/OPT:ICF folded empty functions onto\n"),
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
