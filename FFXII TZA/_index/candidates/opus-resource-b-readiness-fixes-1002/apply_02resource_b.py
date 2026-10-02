"""apply_02resource_b.py [--apply] - 02-Resource-And-Asset-Pipeline readiness map (cloud-reports/re-readiness/02-resource.md),
part B: section 3.1 from the `.ard` / `.nmb` / text-bank group to the handbook census (63 value items, C-V44 .. C-V40)
and section 3.2's stale "open / not read" claims, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the side the shipping image (or the shipped data) REFUTES and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* with the deciding instruction cited as entry+offset; a stale claim answered elsewhere
gets *(answered: see ...; 2026-10-02, OPUS)*. Items whose sides both hold, or that the bytes leave undecided, get no edit
(see verdicts-02b.md in the OPUS scratch). Part A's lines (apply_02resource_a.py) are not touched.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`<- corrected` comment, front-matter lines a trailing `# <- corrected` comment (their OLD includes the line end, so NEW
never contains OLD). Functions of other layers are named by ledger name or role in NEW text (pass-22 rule).
The one changed heading (sloc §2.1) carries OPUS in its correction tag.
Pages mix CRLF and LF: OLD is matched with every newline as CRLF or LF, and NEW takes the matched line endings.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import re
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "02-Resource-And-Asset-Pipeline/"
V = F + "VBF-Archive-And-Authored-Tables/"
S = V + "St2e-Carriers/"
P = F + "PS2-Image-Data-Formats/"
J = F + "Prefetch-And-Json-Data/"
README = F + "README.md"
REG = F + "authored-data-table-registry.md"
ROW = F + "CONTRACT-authored-table-row-lookup.md"
EV = F + "authored-reference-lifetime-evidence.md"
RSA = F + "resource-section-addressing.md"
TREE = F + "CONTRACT-resource-entry-tree.md"
EFX = F + "CONTRACT-efx-source-rebase.md"
TL = F + "a-typed-list-measured-once-and-built-in-one-allocation.md"
RQ = F + "the-resource-request-queue.md"
RQC = F + "CONTRACT-resource-request-queue.md"
ISR = F + "the-indexed-source-request-from-arm-to-terminal-pump.md"
OWNC = F + "CONTRACT-resource-input-ownership.md"
OWN = F + "the-resource-owner-from-copy-or-borrow-to-disposal.md"
EXT = F + "the-external-source-owner-and-borrowed-view-lifetime.md"
PRF = F + "the-nonempty-prf-registration-and-specialized-relocation.md"
ARDC = F + "CONTRACT-ard-area-binder.md"
AEC = F + "Authored-Expressions/CONTRACT-authored-expression-evaluation.md"
RND = F + "Authored-Expressions/how-an-authored-number-gets-its-randomness.md"
VBF = V + "vbf-archive-and-st2e-tables.md"
BIG = V + "how-the-bigfile-index-loads-and-is-verified.md"
BKT = V + "the-dat-and-bin-extension-buckets.md"
S2R = S + "README.md"
NMB = S + "area-nmb-index.md"
BTB = S + "battle-text-banks.md"
LDR = S + "how-the-ard-loader-binds-area-battle-data.md"
PJR = J + "README.md"
AH = J + "ah-asset-header-manifests.md"
PFM = J + "how-the-prefetch-manifests-are-read.md"
TA = J + "ta-texture-animation-lists.md"
FST = F + "Loose-Files-And-Size-Tables/file-size-tables-fst.md"
SF = F + "Standard-Formats/shipped-standard-formats.md"
PR = P + "README.md"
TIM2 = P + "tim2-images-and-the-seven-slot-registry.md"
LBB = P + "loader-bound-bin-families.md"
UBF = P + "unnamed-bin-families.md"
FIVE = P + "five-small-bin-tables.md"
BTM = P + "btm-exfont-bitmaps.md"
CL2 = P + "cl2-menu-colour-tables.md"
AMAP = P + "amap-menumap-area-table.md"
BINM = P + "binmenu-guest-face-and-map-effect-images.md"
CHSE = P + "chse-character-se-tables.md"
CMAP = P + "cmap-menumap-common-sublocation-directory.md"
GMAP = P + "gmap-menumap-guide-texts.md"
HCHK = P + "hchk-hctg-hdat-handbook-indexes.md"
HIMG = P + "himg-handbook-image-bundles.md"
LMAP = P + "lmap-menumap-location-graph.md"
LST = P + "lst-menuquest-list.md"
SLOC = P + "sloc-menumap-container.md"
WMAP = P + "wmap-menumap-world-map-graph.md"

C = "*(corrected 2026-10-02, OPUS: "
CC = "<- corrected 2026-10-02, OPUS: "
ARDR = "`AreaArd_LoadOrUnloadFieldResource`"
REBASE = "`AreaData_BindAndRebaseSectionDescriptor`"
ISSUE = ("the `.ard` request reads that table inline in the read issuer `002DF780` (`002DF780+0x3F` `mov rax, qword ptr "
         "[r15 + rbx*8 + 0x203f000]`, `002DF780+0x4C` `mov rdi, qword ptr [rax + r14*8]`), reached through "
         "`0046E030+0xE`; nothing on the `.ard` path calls `002DF980`")
LOCALES = ("the jump-table bodies of locales 8 and 11 end in `jmp` to the tail of locale 7's body (`002DF9A0+0x58D` and "
           "`002DF9A0+0x534` to `002DF9A0+0x4AA`), which stores the `ch` array into `0215F0A8` at `002DF9A0+0x4C6`")
SLOT7 = ("the binder `AreaArd_BindLoadedRootAndBattleSections` loads `+0x2C` at its `+0x79` and hands `base + offset` to "
         "the slot setter at its `+0x98`; the shipped `in` files hold a non-zero `+0x2C` in 166 of 166, 136 of them a "
         "non-empty table, 1,773 entries in all")
MOTION = ("`003DCA30+0x19` `mov dword ptr [r9], 0x1e` is its only store to the fourth argument; every match is stored "
          "to the fifth (`003DCA30+0x6A`, `003DCA30+0x12A`, `003DCA30+0x150`), and the tables are searched in the "
          "order `02B58188` (`003DCA30+0xF`, key and `+6` only), `02B58178` (`003DCA30+0x81`), `02B58180` "
          "(`003DCA30+0xCC`)")
AUG = ("the query-record filler reads the augment name from word `+2` (its `+0x1F0A` `movzx ecx, word ptr [rax + 2]`, "
       "bank `>> 11`, index `& 0x7FF`); word `+0` is a help id `13000 + n` with `n` the help-text index, not the row "
       "(row 103 carries 13041, the `us` `listhelp_ability.bin` text 41 \"Increases magick power when HP is full.\"; "
       "row 115 carries 13063)")
NMB4 = ("the assembler `00324510` passes the entry's first dword as the fourth argument (`00324510+0x119` "
        "`mov r9d, dword ptr [rbx]`), which is the byte count (part A, C-V2), advances the cursor by it, and stores the "
        "returned request id into the second (`00324510+0x133` `mov dword ptr [rbx + 4], eax`)")
SPLINE2 = ("`00431080+0xA1` `cmp al, 2` / `00431080+0xA3` `jbe` send a point count of two or fewer to the linear path, so "
           "three points already take the spline")
MOVIE = ("`002DF980` is the path getter `[0215F000][kind][index]`; the player passes kind `0x1C` (28, the movie kind) "
         "at its `+0x5C` `mov ecx, 0x1c` and a doubled index (`+0x61` `add edx, edx`), and the other ten callers pass "
         "other kinds")
CALLERS11 = "eleven direct call sites in eleven functions, no `jmp` or thunk caller"
FOURTEEN = ("six pack directories, three kind-9 files and five kind-7 singletons, whose 52 + 4 + 31 files make the 87; "
            "fourteen families")
SILH = ("`002C8EE0`'s two-pass loop asks for kind 7 ids `0x74` and `0x75` (`002C8EE0+0x38` `lea edx, [rdi + 0x74]`); "
        "path-table entry `0x75` is `in\\Bin_Menu\\Char_Silhouette.as7`, which ships in `in` and `ch` and is "
        "2,134,185 B in all twelve `.fst`")
BTMBUF = ("`00365810+0x1E` `dec ecx` and `00365810+0x2E` `movsxd rdi, ecx` index the band with `slot - 1`, and "
          "`00365810+0x4A` loads the pointer held in `022CBE00` before `00365810+0x56` / `00365810+0xA5` address "
          "`[ptr + 0x110 + rdi*8]`")
READY = ("`00364380` loads the pointer held in `022CBE00` at `+0x0`, shifts 1 by the request's `slot - 1` "
         "(`00364380+0x11` `shl eax, cl`) and ORs it into `[ptr + 0x240]` at `00364380+0x13`")
HDATN = ("the shipped monster catalogs hold `+0x14` = 4 in `de`, `it`, `kr`, `us`, 5 in `ch`, `cn`, `es`, `fr` and 11 in "
         "`in`, and each equals that locale's leading `hdat` file count")
TAG4 = ("the u32 at `+0x04` is 102 in every shipped `hctg`; the six per-family values are the whole u16 at `+0x08` "
        "(story `0x1900` = 6400 ... monster `0xF25` = 3877)")
NMBCH = ("three locale bodies reach the `ch` store: locales 8 and 11 jump into locale 7's tail (`002DF9A0+0x58D`, "
         "`002DF9A0+0x534` to `002DF9A0+0x4AA`), which writes `0215F0D0` at `002DF9A0+0x4B8`")

EDITS = [
    # ===================== 3.1: .ard, .nmb, text banks =====================
    # C-V44: the .ard read never calls 002DF980; the read issuer indexes the same table inline.
    (ARDC, "| path resolver | `002DF980` | **22 B** |",
     "| ~~path resolver~~ path getter of the same table, not on the `.ard` read " + C + ISSUE + ")* | `002DF980` | **22 B** |"),
    (LDR, "`0x0215F000`, filled by `FUN_002DF9A0` (2,831 B, a `switch` on locale id), and the resolver is",
     "`0x0215F000`, filled by `FUN_002DF9A0` (2,831 B, a `switch` on locale id), and ~~the resolver is~~ the 22-byte "
     "getter of that table is " + C + ISSUE + ")*"),
    # C-V46: the namespace of the sibling request is in edx; 003EA83E is mid-instruction.
    (ARDC, "instructions: `003EA840 mov ecx, 0x15` is the namespace (21), and `003EA845 lea esi, [r14 + r14]`",
     "instructions: ~~`003EA840 mov ecx, 0x15` is the namespace (21)~~ the namespace (21) is `mov ecx, 0x15` at the "
     "reader's `+0x43` for its size lookup and `lea edx, [rax + 0x15]` at its `+0x38` for the sibling request " + C +
     "the reader's `+0x20` `mov ecx, 0x15` feeds the `005C5230` test at its `+0x29`, not a request)*, and `003EA845 lea esi, [r14 + r14]`"),
    (LDR, "`field_index * 2 + 1` (`003EA83E`, via `FUN_0032eb40(0, 0x15, field_index*2+1)`).",
     "`field_index * 2 + 1` (~~`003EA83E`~~ `AreaArd_LoadOrUnloadFieldResource+0x32` `lea r8d, [rsi + 1]`, via `FUN_0032eb40(0, 0x15, "
     "field_index*2+1)`) " + C + "the old address falls inside the reader's `+0x1B` call; the request is its `+0x3B`)*."),
    # C-V47: 0020E620 encodes; with slot 1's depth 0 nothing recurses.
    (LDR, "`st2e` one (`FUN_003846F0`, 177 B) is its reader: `slot = resolve(desc)` (`00384704`–`00384709`),",
     "`st2e` one (`FUN_003846F0`, 177 B) is its reader: ~~`slot = resolve(desc)`~~ `slot = encode(desc)`, the image-"
     "relative encoding `RuntimePointer_EncodeImageAddress` makes (`00384704`–`00384709`) " + C + "the directory "
     "binder's `+0x14` calls the encoder, not the resolver)*,"),
    (LDR, "— the first `count` through a recursive call with the depth argument decremented (`0038475B`–",
     "— ~~the first `count` through a recursive call with the depth argument decremented (`0038475B`–~~ every "
     "entry in place, because this slot's depth argument is 0 " + C + "`BattleData_SetAreaArdSectionCategory+0x4F` "
     "`xor r8d, r8d` before its `+0x52` `jmp`; with depth 0 the directory binder's `+0x60` `test ecx, ecx` / `+0x62` "
     "`je` skip the recursion at its `+0x7B` and every entry takes the `+0x90` `add dword ptr [rbx], ebp`)* "
     "(recursion would be `0038475B`–"),
    # C-V48: the rebased fields are +0x0C/+0x10/+0x18/+0x1C plus +0x14 re-encoded; +0x00 is not touched.
    (LDR, "- **`AreaData_BindAndRebaseSectionDescriptor`'s descriptor fields** (`+0x00`, `+0x10`, `+0x14`,",
     "- **`AreaData_BindAndRebaseSectionDescriptor`'s descriptor fields** (~~`+0x00`~~ `+0x0C` " + C + REBASE +
     " stores the base into the slot at its `+0x4`, never into the descriptor's `+0x00`; its `+0x10` reads `+0x0C`, "
     "the table above)*, `+0x10`, `+0x14`,"),
    # C-V49: slot 7 is non-zero in all 166 `in` files.
    (LDR, "904–944 and 4000–4008, motion indices 60–2306 (1,161 distinct). The `.ard` slot is 0 in all 166",
     "904–944 and 4000–4008, motion indices 60–2306 (1,161 distinct). ~~The `.ard` slot is 0 in all 166~~ The `.ard` "
     "slot is bound in all 166 " + C + SLOT7 + ")*"),
    (LDR, "  `in` files, so in the shipped game only the script-side table is ever bound.",
     "  ~~`in` files, so in the shipped game only the script-side table is ever bound.~~ `in` files, so the area's "
     "table is consulted before `section_019`'s wherever it has rows."),
    # C-V50: the trailer record is {u32 key, u32 mask}; 0..13 are aliases, every shipped key passes through.
    (LDR, "> counted list of 8-byte `{selector, mask}` records at the trailer (`+0` count, `+4`…): the selector",
     "> counted list of 8-byte ~~`{selector, mask}`~~ `{u32 key, u32 mask}` records at the trailer (`+0` count, `+4`…) "
     + C + "`0035A3A0+0x43` loads the whole dword as the key and `0035A3A0+0x46` the mask; `002EB7A0` maps only keys "
     "0–13 (`002EB7A0+0x3` `ja` to `+0x31` `mov eax, ecx` passes any larger key through), and all 998 shipped keys are "
     "above 13, a letter `c`/`m`/`n`/`s`/`w` in the high word)*: the selector"),
    # C-V51: locales 7, 8 and 11 reach the `ch` .ard store.
    (LDR, "9 / 10 / default body) — and **exactly one body touches the `.ard` slot: locale 7** (`002DFDF6`),",
     "9 / 10 / default body) — and ~~**exactly one body touches the `.ard` slot: locale 7**~~ **three locales reach "
     "the `.ard` store: 7, 8 and 11** " + C + LOCALES + ")* (`002DFDF6`),"),
    (LDR, "loader has exactly two `.ard` arrays: `in` for every locale but one, `ch` for locale 7.",
     "loader has exactly two `.ard` arrays: ~~`in` for every locale but one, `ch` for locale 7.~~ `in` for every "
     "locale but three, `ch` for locales 7, 8 and 11 (as corrected above)."),
    # C-V52: the `ch` .nmb run is 321, one contiguous run.
    (NMB, "stride-8 runs of 321 (`in`) and 313 + 7 (`ch`)** — bounded by string identity rather than by",
     "stride-8 runs of 321 (`in`) and ~~313 + 7~~ 321 (`ch`)** " + C + "the `ch` array `01EAE0D0` holds 321 "
     "consecutive qwords, every one a pointer to a `ch\\...\\.nmb` path, with no break)* — bounded by string identity "
     "rather than by"),
    # C-V53: the initialiser stores 94 bases.
    (LDR, "extent as the distance to the next base in address order, over all **83** path-table bases recovered",
     "extent as the distance to the next base in address order, over all ~~**83**~~ **94** path-table bases "
     "recovered " + C + "`002DF9A0` makes 94 `lea`-then-store installs of 94 distinct values into the 41 slots; "
     "88 are image arrays and six point into the table's own BSS block; the 642-slot extent holds with all 94)*"),
    # C-V54 / C-V123: word +0 is a help id 13000 + n (n the help index); the name word is +2.
    (BTB, "directory offset `+0xEC`, `{u16 nameId, u16 0x5000 + row, u16 parameter, u16 0xFF}`) carries",
     "directory offset `+0xEC`, ~~`{u16 nameId, u16 0x5000 + row, u16 parameter, u16 0xFF}`~~ `{u16 helpId, u16 "
     "nameWord = 0x5000 + row, u16 parameter, u16 0xFF}`) " + C + AUG + ")* carries"),
    # C-V55: word +2 of rows 116..127 is 0x5074..0x507F.
    (BTB, "> text reference**: their word `+2` is `0x5070`–`0x507F` = 20,592–20,607 — in the same low-pool",
     "> text reference**: their word `+2` is ~~`0x5070`–`0x507F` = 20,592–20,607~~ `0x5074`–`0x507F` = "
     "20,596–20,607, bank 10 rows 116–127 " + C + "`0x5000 + row` in the shipped `us` augment table; the query-record "
     "filler reads it as a bank word, `>> 11` and `& 0x7FF`)* — in the same low-pool"),
    (BTB, "and their name ids `0x5070`–`0x507F` are low-pool group 20 rows 592–607.",
     "and their name ids ~~`0x5070`–`0x507F` are low-pool group 20 rows 592–607~~ `0x5074`–`0x507F` are bank 10 "
     "rows 116–127 " + C + "`0x5000 + row` in the shipped augment table; the query-record filler reads word `+2` as a "
     "bank word)*."),
    # C-V106: the assembler's pairs are {size, requestId}; the fourth argument is the size.
    (REG, "cursor, id)` for every positive id in the `{i32 id, i32 size}` pairs at `022C27B8` — recording",
     "cursor, id)` ~~for every positive id in the `{i32 id, i32 size}` pairs~~ for every positive size in the "
     "`{i32 size, i32 requestId}` pairs, that size being the fourth argument, " + C + NMB4 + ")* at `022C27B8` — recording"),
    (NMB, "`00324510`, from `MainLoop_UpdateAndRenderFrame` (`0022BAEF`), issues `0032E620(0x1a, i, cursor, id)`",
     "`00324510`, from `MainLoop_UpdateAndRenderFrame` (`0022BAEF`), issues ~~`0032E620(0x1a, i, cursor, id)`~~ "
     "`0032E620(0x1a, i, cursor, size)` " + C + NMB4 + ")*"),
    # C-V122: 003DCA30 stores 0x1E to the 4th argument and every match to the 5th.
    (LDR, "  at start-up. `003DCA30(modelKey, groupId, class, &primary, &secondary)` sets `primary = 0x1E` and",
     "  at start-up. ~~`003DCA30(modelKey, groupId, class, &primary, &secondary)` sets `primary = 0x1E`~~ "
     "`003DCA30(modelKey, groupId, class, &kind, &index)` sets `kind = 0x1E` (as corrected below) and"),
    (LDR, "  searches the **`.ard` table first, then `section_019`'s**, over 16-byte entries",
     "  searches ~~the **`.ard` table first, then `section_019`'s**~~ a third table first, then the `.ard` table, then "
     "`section_019`'s, over 16-byte entries"),
    (LDR, "  `{u32 modelKey; u16 class; u16 groupId; u16 motionIndex}`: a `(modelKey, groupId)` match yields",
     "  `{u32 modelKey; u16 class; u16 groupId; u16 motionIndex}`: ~~a `(modelKey, groupId)` match yields~~ a "
     "`(modelKey, groupId)` match in the first table, or a `(modelKey, groupId, class)` match in the other two, yields "
     "`index = motionIndex` " + C + MOTION + "; the prototype above is restated from `&primary, &secondary`)*"),
    (LDR, "  `secondary = motionIndex`, a `(modelKey, groupId, class)` match `primary = motionIndex`",
     "  ~~`secondary = motionIndex`, a `(modelKey, groupId, class)` match `primary = motionIndex`~~"),
    # ===================== 3.1: authored expressions =====================
    # C-V56: 0039B630 is the quadratic B-spline blend, not a matrix-vector transform.
    (RND, "`0039B630` (170 B) is a call-free 3x3 matrix-vector transform - `mulss`/`addss` row triples into `[r8]`/`[r8+4]`.",
     "`0039B630` (170 B) is ~~a call-free 3x3 matrix-vector transform~~ the call-free quadratic B-spline blend "
     "`0.5(1-t)² p0 + ((1-t)t + 0.5) p1 + 0.5t² p2` of three 3-vectors at `+0`, `+0x10` and `+0x20` " + C +
     "`0039B630+0x4` loads `1.0` and `0039B630+0x1B` forms `1 - t` from the `t` in `xmm0`; the three weights multiply "
     "the vectors' x, y and z and the sums are stored at `[r8]`, `[r8+4]`, `[r8+8]`, `0039B630+0x62` the first)* - "
     "`mulss`/`addss` row triples into `[r8]`/`[r8+4]`."),
    # C-V58: 00431430 calls f only in op 5; op 4 is (r9 + 1) * a; 139 B.
    (RND, "`00431430` (165 B) is the mode-keyed combiner",
     "`00431430` (~~165 B~~ 139 B " + C + "its last instruction ends at `00431430+0x8B`; the 24-byte case table after it "
     "is data)*) is the mode-keyed combiner"),
    (RND, "`(r9+1) * rbx`, or (modes 4/5 with `r8 != rbx`) `003A6E60(r8 - rbx)` + `rbx`",
     "`(r9+1) * rbx`, or ~~(modes 4/5 with `r8 != rbx`)~~ (mode 5 only, with `r8 != rbx`) `003A6E60(r8 - rbx)` + `rbx` " + C +
     "op 4 is `00431430+0x55` `lea eax, [r9 + 1]` / `+0x59` `imul eax, ebx` with no call, and with `r8 = 0` "
     "`00431430+0x6C` `sub ecx, 4` returns `rbx`; the only `003A6E60` call is op 5's at `00431430+0x7E`)*"),
    # C-V59 (with the point-count fallback): two points or fewer fall back to linear.
    (RND, "**1 quadratic B-spline** — with three points or fewer the linear path,",
     "**1 quadratic B-spline** — with ~~three points or fewer~~ two points or fewer the linear path " + C + SPLINE2 + ")*,"),
    (AEC, "  `y`; three points or fewer fall back to linear **[page]**.",
     "  `y`; ~~three points or fewer~~ two points or fewer fall back to linear " + C + SPLINE2 + "; the kinds 2 and 3 "
     "above are the operand's two-bit curve selector, `00431080+0x93`)* **[page]**."),
    # ===================== 3.1: typed list, prefetch, .ah, .ta, standard formats =====================
    # C-V27: the census spreads the 258 pack type-7s over eight units.
    (TL, "standalone-file type-7 items carry `+0x40 = 0xFFFF` (no second atlas); pack unit 01's 258 type-7s author",
     "standalone-file type-7 items carry `+0x40 = 0xFFFF` (no second atlas); ~~pack unit 01's 258 type-7s author~~ "
     "the 258 pack type-7s sit in eight units: unit 01's 150 author `+0x40 = 0x0001` (140) or `0xFFFF` (10), units 03 "
     "and 12 `0xFFFF`, units 05, 13 and 16 `0x0000`, units 14 and 15 `0x0002` / `0x0001` with the required id "
     "`partytop_4_c`; every authored second atlas resolves to `battle_4_c` " + C + "`members/atlas-name-census.tsv`, "
     "regenerated from the shipped VBF and byte-identical)*"),
    (TL, ">   `+0x40 = 0x0001` (`battle_4_c`, same as the required id).",
     ">   ~~`+0x40 = 0x0001` (`battle_4_c`, same as the required id).~~"),
    # C-V28: 49 distinct names, 21 never indexed.
    (TL, "> Supplementary: the arrays declare 48 distinct names but items reference only 28 — 20 names are authored yet",
     "> Supplementary: the arrays declare ~~48~~ 49 distinct names but items reference only 28 — ~~20~~ 21 names are "
     "authored yet " + C + "the census's distinct-name section: 49 rows, 28 `yes`, 21 `no`)*"),
    # C-V67 / C-V68: 002DF980 is the (kind, index) path getter; eleven callers.
    (SF, "(`008F8D75`, `001B8009`–`001B8015`) from a 0x1C-stride movie table (`002DF980`) and opens it through",
     "(`008F8D75`, `001B8009`–`001B8015`) from ~~a 0x1C-stride movie table (`002DF980`)~~ the path table "
     "`0215F000`'s kind-`0x1C` array through `002DF980` " + C + MOVIE + ")* and opens it through"),
    (SF, "locale-dependent). The movie table `002DF980` is read by a 1,636-byte Presentation body.",
     "locale-dependent). The ~~movie table~~ path getter `002DF980` " + C + MOVIE + ")* is read by a 1,636-byte "
     "Presentation body."),
    (SF, "`002DF980` — 22 B, 34 callers; the two-level index the 0x1C-stride movie table's readers",
     "`002DF980` — 22 B, ~~34 callers~~ 11 callers " + C + CALLERS11 + ")*; the two-level index ~~the 0x1C-stride "
     "movie table's readers~~ all `(kind, index)` path readers"),
    (LDR, "The movie table `002DF980` is\n",
     "The ~~movie table~~ path getter `002DF980` " + C + MOVIE + ")* is\n"),
    # C-V69: prefetchdata holds 9,351 files; 10,253 is the archive-wide .txt count.
    (PJR, "| `txt` | 10,253 | `prefetchdata/<lang>` — ~1,040 per language |",
     "| `txt` | ~~10,253~~ 9,341 (with 10 `.csv`, 9,351 files) " + C + "the archive index: 9,351 entries under "
     "`prefetchdata/`; 10,253 is every `.txt` in the archive)* | `prefetchdata/<lang>` — ~1,040 per language |"),
    (PJR, "**`prefetchdata` is a streaming hint system.** 10,253 files, roughly 1,040 per language.",
     "**`prefetchdata` is a streaming hint system.** ~~10,253 files~~ 9,351 files " + C + "the archive index; "
     "10,253 counts every `.txt`)*, roughly 1,040 per language."),
    # C-V71: 001E5790 is a call-free record writer; 01CEBDA0 is the float sign mask.
    (TA, "`001E5790` (530 B on `01CEBDA0` — the frame-clock read behind `001A9B70`)",
     "`001E5790` (530 B on `01CEBDA0` — ~~the frame-clock read behind `001A9B70`~~ a call-free record writer that "
     "negates two floats with the `.rdata` sign mask " + C + "`01CEBDA0` is four `0x80000000` and `001E5790+0xF7` "
     "`xorps`es with it)*)"),
    (TA, "`TA-1`'s answer lives here in embryo: `001E5790` is the clock source (`01CEBDA0` — the same",
     "`TA-1`'s answer lives here in embryo: ~~`001E5790` is the clock source (`01CEBDA0` — the same~~ " + C +
     "`001E5790` makes no call and `01CEBDA0` is the float sign mask its `+0xF7` `xorps` uses; the clock is the "
     "animation slot's time, `TA-1` answered 2026-09-25 above)* (the same"),
    # C-V74: the node's +0x120 points at the arena record's +0x120 cell, not at itself.
    (AH, "`+0x120` self-links, and `001A0BB0(alloc, node, 0)` enlists it.",
     "`+0x120` ~~self-links~~ holds the address of the arena record's own `+0x120` cell, the buffer pointer the reader "
     "scans " + C + "`0019EB60+0x34` `lea r14, [rax + 0x120]` on the arena `001BA860` returned, `0019EB60+0x49` zeroes "
     "it and `0019EB60+0x9F` stores it at node `+0x120`; the token reader takes `[node + 0x120]` at "
     "`0019E7B0+0x2F`)*, and `001A0BB0(alloc, node, 0)` enlists it."),
    # C-V107: twelve .fst files; 396 in eleven, -1 in UK.
    (AMAP, "| request size | `.fst` kind 7 id `0xA5` = 396 in all nine `FileSizeTable_*.fst` |",
     "| request size | `.fst` kind 7 id `0xA5` = 396 in ~~all nine~~ eleven of the twelve `FileSizeTable_*.fst`, -1 "
     "in `UK` " + C + "the install ships twelve tables, `ASIA` … `US`; each read at dword `7·5000 + 0xA5`)* |"),
    # ===================== 3.1: PS2-era formats =====================
    # C-V75: 1,439 .bin entries; 2,366 is MiB.
    (PR, "| `bin` | 1,437 | 2,366 MB |",
     "| `bin` | ~~1,437~~ 1,439 " + C + "the archive index; the census below counts the same 1,439)* | 2,366 MiB "
     "(2,481 MB) |"),
    # C-S39 (PR): .tm2 is TIM2.
    (PR, "| `tm2` | 447 | **likely TIM2**, the PS2 image format — candidate `standard` |",
     "| `tm2` | 447 | ~~**likely TIM2**~~ **TIM2**, the PS2 image format, magic `TIM2` in 447 of 447 *(answered: see "
     "[the TIM2 sheet](tim2-images-and-the-seven-slot-registry.md) §8, all 456 files opened; 2026-10-02, OPUS)* — "
     "candidate `standard` |"),
    # C-V76 + C-S39: fourteen families; summoneffectdata is not a named object.
    (PR, "thirteen families reachable only by kind/subtype request: the six `*pack_ys`/`fontpack_*` sentinel-filled "
         "offset directories, the kind-9 named objects (`behindcamera`, `pc_skillmotion`, `summoneffectdata`)",
     "~~thirteen~~ fourteen families " + C + FOURTEEN + ")* reachable only by kind/subtype request: the six "
     "`*pack_ys`/`fontpack_*` sentinel-filled offset directories, the kind-9 ~~named objects~~ files (`behindcamera` "
     "and `pc_skillmotion` named objects, `summoneffectdata` read into the fixed `.data` buffer `02AD9B60`, the "
     "loader-bound sheet §3)"),
    (LBB, "system: Thirteen .bin families reached only by kind/subtype request — pack directories, font packs, and six small tables\n",
     "system: Thirteen .bin families reached only by kind/subtype request — pack directories, font packs, and six small "
     "tables  # " + CC + "fourteen families (6 packs, 3 kind-9, 5 kind-7 singletons) make the 87 files\n"),
    (LBB, "> `FABLE-REQ-SWE2-DATA-LOADERS-FOR-UNNAMED-FILES`. These thirteen families are not in the",
     "> `FABLE-REQ-SWE2-DATA-LOADERS-FOR-UNNAMED-FILES`. These ~~thirteen~~ fourteen families " + C + FOURTEEN +
     ")* are not in the"),
    (LBB, "Kind 9 files arrive as **named resource objects** (`0036A190` allocs, `0036C660` registers the",
     "~~Kind 9 files arrive as **named resource objects**~~ Two of the three kind-9 files arrive as **named resource "
     "objects** " + C + "the summon-effect loader reads `summoneffectdata` into the fixed `.data` buffer "
     "`02AD9B60`, its `+0x5D` `lea r8`, as the row below says)* (`0036A190` allocs, `0036C660` registers the"),
    # C-V77: the clutpack binder fills four slots.
    (LBB, "`+0x390`/`+0x398`/`+0x3A0` populated on zero from `[+0x3C8]` self-relative offsets.",
     "~~`+0x390`/`+0x398`/`+0x3A0` populated~~ `+0x390`/`+0x398`/`+0x3A0`/`+0x3A8` populated " + C + "the fourth "
     "store is `00280AD0+0x95` `mov qword ptr [rdx + 0x3a8], rcx`)* on zero from `[+0x3C8]` self-relative offsets."),
    # C-V78: the tex2pack walk ends at +0x380; +0x388 is a separate raw store.
    (LBB, "Binder `00280740` → `00280670` walks slots `+0x338..+0x388` in step-8 lockstep with the offset",
     "Binder `00280740` → `00280670` walks slots ~~`+0x338..+0x388`~~ `+0x338..+0x380` " + C + "`00280670+0x5A` "
     "`cmp rbx, 0x388` / `+0x61` `jl` stop before `+0x388`, which `00280670+0x84` stores raw)* in step-8 lockstep "
     "with the offset"),
    # C-V82: id 0x75 is Char_Silhouette.as7, which ships.
    (LBB, "requests subtype `0x74` (this file) and `0x75` (**no file ships — the slot stays null**), sizes",
     "requests subtype `0x74` (this file) and `0x75` (~~**no file ships — the slot stays null**~~ "
     "`Char_Silhouette.as7` " + C + SILH + ")*), sizes"),
    # C-V80 / C-V81: the .btm band is addressed through the pointer in 022CBE00, slot - 1.
    (BTM, "| buffer slot | `[022CBE00 + 0x110 + slot*8]` — the `.btm` half of the 12 ids |",
     "| buffer slot | ~~`[022CBE00 + 0x110 + slot*8]`~~ `[[022CBE00] + 0x110 + (slot − 1)*8]` " + C + BTMBUF +
     ")* — the `.btm` half of the 12 ids |"),
    (BTM, "| ready bit | `[022CBE00 + 0x240]` bit `slot` — set on completion |",
     "| ready bit | ~~`[022CBE00 + 0x240]` bit `slot`~~ `[[022CBE00] + 0x240]` bit `slot − 1` " + C + READY +
     ")* — set on completion |"),
    # C-V84: 0xE2 Loca_gil, 0xE3 Loca_bhm, 0xE4 Loca_rbl.
    (CL2, "| kind-7 ids | `0xE2`–`0xE4` per the path arrays (`Loca_bhm`/`Loca_gil`/`Loca_rbl`) |",
     "| kind-7 ids | `0xE2`–`0xE4` per the path arrays (~~`Loca_bhm`/`Loca_gil`/`Loca_rbl`~~ `Loca_gil`/`Loca_bhm`/"
     "`Loca_rbl` in id order " + C + "kind-7 array `01EDD7E0` entries `0xE2`, `0xE3`, `0xE4`; RC-30 below)*) |"),
    # C-V87: the _name tables carry count + 1 offsets.
    (UBF, "      - **The two `_name` tables** are a `u32` count, then that many ascending offsets, each to a NUL-terminated",
     "      - **The two `_name` tables** are a `u32` count, then ~~that many~~ count + 1 ascending offsets, the last "
     "the file size " + C + "`basic_skill` 1,345 and `growth_rate` 128 rows; the first string sits at "
     "`4 + 4·(count + 1)` and `offsets[count]` equals the file size, `kr` and `cn`)*, each to a NUL-terminated"),
    # C-V88: sign sections 1 and 2.
    (FIVE, "| 1 | `0x0EC` | 24 | `{u16, u16}` | **`0x150`** |",
     "| 1 | `0x0EC` | 24 | ~~`{u16, u16}`~~ `{u24 labelTextId, u8 buttonIndex}` " + C + "`0029DA70+0xAA` takes "
     "byte 3 as the index and `0029DA70+0x100` masks the dword `0xFFFFFF`, the answer below)* | **`0x150`** |"),
    (FIVE, "| 2 | `0x150` | 19 | `{u16, u16}` | `0x1A0` |",
     "| 2 | `0x150` | 19 | ~~`{u16, u16}`~~ `u16[19]` offsets over 8-byte scene records " + C + "offsets `0x2C` … "
     "`0xBC` in the shipped `key_signal_data.bin`, the answer below)* | ~~`0x1A0`~~ `0x214`, the file end |"),
    # C-V89: the records start at +0x00 and fill the whole 672-byte file.
    (FIVE, "*Superseded 2026-09-29 (below): `dP<d` is not a tag but record 0's first four bytes, and the 668 bytes are 64 ten-byte records and a 32-byte tail.*",
     "*Superseded 2026-09-29 (below): `dP<d` is not a tag but record 0's first four bytes, and ~~the 668 bytes are~~ "
     "the file's 672 bytes, from `+0x00`, are 64 ten-byte records and a 32-byte tail.* " + C + "64 · 10 + 32 = 672 = "
     "`0x2A0`, the tail at `0x280`)*"),
    # C-V91: menuhandbook.bin / order.bin are requested as kind 7 0xC8 / 0xC9.
    (HCHK, "uses a different id space (kind-6 base `0x80`); the `menuquest.dat` bind uses `0x128` — the",
     "~~uses a different id space (kind-6 base `0x80`)~~ is requested as kind 7 ids `0xC8` / `0xC9` " + C +
     "`003158B0+0x25` `mov edx, 7` and `003158B0+0x33` `mov r8d, 0xc8`, `00572D80+0x51` / `00572D80+0x5E` for "
     "`0xC9`; the kind-6 path array also lists the two paths, at `0xF2` / `0xF3`)*; the `menuquest.dat` bind uses "
     "`0x128` — the"),
    # C-V39: hctg +0x14 varies per locale for the monster family.
    (HCHK, "count** (1 for story/world/person/tutorial, 2 for knowledge, 4 for monster — matching the",
     "count** (1 for story/world/person/tutorial, 2 for knowledge, ~~4 for monster~~ 4, 5 or 11 for monster by "
     "locale " + C + HDATN + ")* — matching the"),
    (HIMG, "story/world/person/tutorial, 2 for knowledge, 4 for monster — matching the shipped file names),",
     "story/world/person/tutorial, 2 for knowledge, ~~4 for monster~~ 4, 5 or 11 for monster by locale " + C +
     HDATN + ")* — matching the shipped file names),"),
    # C-V40: hctg +0x04 is 102; the family values are the +0x08 word.
    (HCHK, "+0x04  u32      familyTag  {6400, 6401, 3954, 6403, 6404, 3877} — per-family constant\n",
     "+0x04  u32      familyTag  {6400, 6401, 3954, 6403, 6404, 3877} — per-family constant   " + CC + TAG4 + "\n"),
    (HCHK, "                          {story 0x1900, world 0x1901, person 0xF72, knowledge 0x1903,\n",
     "                          {story 0x1900, world 0x1901, person 0xF72, knowledge 0x1903,   " + CC + "these are "
     "the whole u16 at +0x08, not its high 12 bits\n"),
    # C-V95: the six handles are 8 bytes apart.
    (HCHK, "| `+0xC8` … `+0xF0` | six family `hchk` buffers (48-byte stride, `{u16 count; rec[]}` at +8/+0x0C) |",
     "| `+0xC8` … `+0xF0` | six family `hchk` buffers (~~48-byte stride~~ 8-byte stride, 48 bytes in all " + C +
     "`00576F50+0xA5` `lea r14, [rbx + 0xc8]` and `00576F50+0xE0` `lea r14, [r14 + 8]` per family)*, "
     "`{u16 count; rec[]}` at +8/+0x0C) |"),
    # C-V96: +0xC9 also takes 1 (loaded); +0xD2 is the record's family byte.
    (HIMG, "+0xC9  u8 load phase (0 idle, 2 loading, 3 releasing)\n",
     "+0xC9  u8 load phase (0 idle, 2 loading, 3 releasing)   " + CC + "1 = loaded: 00575870+0x63 stores 1 when the "
     "load completes, and the readers require 1\n"),
    (HIMG, "+0xD2  u8 page mode                   +0xF0  resource buffer (the raw himg file)\n",
     "+0xD2  u8 page mode                   +0xF0  resource buffer (the raw himg file)   " + CC + "+0xD2 is the "
     "record's byte +0 (00575C30+0xA2), the family index into 0xD23740\n"),
    # C-V97: 00575710 is the handbook image pane's bind; 00576F50 is the handbook root's bind.
    (LST, "| buffer consumer | quest-list subsystem — the pane builder `00575710` resolves rows from the loaded quest data;",
     "| buffer consumer | quest-list subsystem — ~~the pane builder `00575710` resolves rows from the loaded quest "
     "data~~ " + C + "`00575710` is the handbook image pane's bind: it registers the pane's `+0xF0` buffer as a TIM2 "
     "at `00575710+0x5C` and keeps the handle at `+0xF8`, `00575710+0x55`; the `.lst` readers are RC-31's two)*;"),
    # C-V92: the per-kind table is 02F973C0.
    (BINM, "| `00238640` | indexes the per-kind record table `0x050E53C0 + kind*8` → `003845F0` |",
     "| `00238640` | indexes the per-kind record table ~~`0x050E53C0 + kind*8`~~ `0x02F973C0 + kind*8` " + C + "the "
     "19-byte binder's `+0x3` `lea rcx, [rip + ...]` resolves to `02F973C0`)* → `003845F0` |"),
    (BINM, "pixel buffer itself. The per-kind descriptor table `0x050E53C0` is **runtime-populated**",
     "pixel buffer itself. The per-kind descriptor table ~~`0x050E53C0`~~ `0x02F973C0` " + C + "as in the table "
     "above; it lies past `.data`'s raw end `0x01F7E400`, so BSS)* is **runtime-populated**"),
    # C-V93: +0x14 is rebased then re-encoded, not left absolute.
    (BINM, "| `003845F0` | record pointer fixup: `dword` offset fields at `rec+0xC/0x10/0x14/0x18/0x1C` relocated to absolute (plus a sub-offset table via `+0x14`) |",
     "| `003845F0` | record pointer fixup: `dword` offset fields at ~~`rec+0xC/0x10/0x14/0x18/0x1C` relocated to "
     "absolute~~ `rec+0xC/0x10/0x18/0x1C` relocated to absolute, and `+0x14` relocated then re-encoded image-relative "
     + C + REBASE + " adds the base at its `+0x62` and hands the sum to `RuntimePointer_EncodeImageAddress` at its "
     "`+0x6D`, storing the encoding at its `+0x72`)* (plus a sub-offset table via `+0x14`) |"),
    # C-V94: 002E60F0 is 491 B.
    (CHSE, "`002E60F0` (~62 B) — `dword[rcx]`-keyed table op (`002E60FA`).",
     "`002E60F0` (~~~62 B~~ 491 B " + C + "its last instruction ends at `002E60F0+0x1EB`; 62 B is the member "
     "`003A1290`)*) — `dword[rcx]`-keyed table op (`002E60FA`)."),
    # C-V98: 35 copies are 9 + 8 + 6 + 6 + 6, not 5 x 7.
    (GMAP, "corpus_validated: \"all 35 menumap_guide00..04.bin copies (5 units x 7 locales) close under the layout; 30 "
           "carry an embedded TIM2 ending exactly at EOF; guide00's 77 entries join menumap_common section 3 record by "
           "record 77/77 (shifted control 0/77); .fst sizes exist for kind 7 ids 0x496..0x49A only, 2026-09-29\"\n",
     "corpus_validated: \"all 35 menumap_guide00..04.bin copies (5 units x 7 locales) close under the layout; 30 "
     "carry an embedded TIM2 ending exactly at EOF; guide00's 77 entries join menumap_common section 3 record by "
     "record 77/77 (shifted control 0/77); .fst sizes exist for kind 7 ids 0x496..0x49A only, 2026-09-29\"  # " + CC +
     "the 35 are 9 + 8 + 6 + 6 + 6 by unit (G1 below), not 5 x 7\n"),
    # C-V100: menumap_sub files are 1.0 - 11.5 MB.
    (LMAP, "\"double buffer\" or 512 KB in a \"single buffer\". Those are PS2-era sizes: the TZA `menumap_sub00`–`47.bin` files are\n",
     "\"double buffer\" or 512 KB in a \"single buffer\". Those are PS2-era sizes: the TZA `menumap_sub00`–`47.bin` "
     "files are " + C + "1,049,520 – 11,544,192 B over the 436 shipped copies, the sloc sheet's corpus)*\n"),
    (LMAP, "4–11 MB, every one above both limits.",
     "~~4–11 MB~~ 1.0–11.5 MB, every one above both limits."),
    # C-V105: array C's +0 / +2 are the A ids in 545 of 545.
    (LMAP, "  the offset was wrong**: it is `+12` **and** `+14`, each an A id from the same record in **501 of",
     "  the offset was wrong**: it is ~~`+12` **and** `+14`~~ `+0` **and** `+2` at native offsets " + C + "§10.3: "
     "the shipped `us` file gives 545 of 545 for each; `+12` / `+14` was the shifted model)*, each an A id from the "
     "same record in ~~**501 of~~ **545 of"),
    # C-V101: the sloc header is 0x14 bytes.
    (SLOC, "### 2.1 Header — 16 bytes, then the directory",
     "### 2.1 Header — ~~16 bytes~~ 20 bytes (`0x14`), then the directory " + C + "the struct below and the "
     "directory at `+0x14`)*"),
    # C-V102: 2.41 GB over the 436 files.
    (SLOC, "| size | **1,049,520 B – 11,544,192 B** — 4.5 GB of `.bin` in total, the largest thing under `ps2data/image` |",
     "| size | **1,049,520 B – 11,544,192 B** — ~~4.5 GB of `.bin` in total~~ 2.41 GB over the 436 copies " + C +
     "the archive index; every `.bin` in the archive totals 2.48 GB)*, the largest thing under `ps2data/image` |"),
    # C-V103: 26 magics; st2e (73) is the largest, sloc second.
    (SLOC, "  census row** and that `sloc` is one of the seven signatures found in it. **The `.bin` signature",
     "  census row** and that `sloc` is one of the seven signatures found in it. " + C + "the full census of "
     "2026-09-19 in that README counts 26 magics over 178 of the 236 units, `st2e` the largest at 73 and `sloc` second "
     "at 52; the 28 below includes leading dwords that are not magics, such as `CCdd`)* **The `.bin` signature"),
    (SLOC, "  (`Tools/work/formats/bin-signature-census.tsv`), and `sloc` is the largest of them at 52 units.",
     "  (`Tools/work/formats/bin-signature-census.tsv`), and `sloc` is ~~the largest of them~~ the second largest, "
     "after `st2e`'s 73, at 52 units."),
    # ===================== 3.2: README and banners =====================
    # C-S1: slot 0x02EBF138 is bound from battle_pack.bin +0x3C.
    (README, "  arithmetic. **`action_data.bin` is the file behind registry slot `0x02EBF138`**: 543 records of 60",
     "  arithmetic. ~~**`action_data.bin` is the file behind registry slot `0x02EBF138`**~~ **registry slot "
     "`0x02EBF138` is bound from `battle_pack.bin`'s directory entry `+0x3C`** *(answered: see the VBF sheet's "
     "*Corrected 2026-10-01* note in its opening and §12; `action_data.bin` is a copy of that section; "
     "2026-10-02, OPUS)*: 543 records of 60"),
    # C-S13: the builder records the caller's bytes; the stall is in the requester 0032E870.
    (README, "  request queue every file load goes through: the builder that sizes a request from the file-size",
     "  request queue every file load goes through: ~~the builder that sizes a request from the file-size~~"),
    (README, "  table and stalls when no slot is free, the pump the frame drives through six states, 512 KB",
     "  ~~table and stalls when no slot is free,~~ the builder that records the byte count its caller passes (the "
     "caller takes it from the file-size table), the requester `0032E870` that pumps while no slot is free "
     "*(answered: see [the queue page](the-resource-request-queue.md) §2, \"The bytes come from the caller\" and "
     "\"`0032E870` is where the queue's only stall lives\"; 2026-10-02, OPUS)*, the pump the frame drives through six "
     "states, 512 KB"),
    # C-S54: the VBF layout is read.
    (README, "VBF/EBP container layout (use `ff12-vbf.exe` and `ff12-script.exe`).",
     "VBF/EBP container layout (use `ff12-vbf.exe` and `ff12-script.exe`) *(answered for VBF: see "
     "[the bigfile page](VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md) §3a; "
     "2026-10-02, OPUS)*."),
    # C-S1 (VBF, BTB): the AY-6 lead is closed.
    (VBF, "> **Downgraded:** `action_data.bin` → slot `0x02EBF138` is a **strongly supported lead**, resting on",
     "> **Downgraded:** `action_data.bin` → slot `0x02EBF138` is a **strongly supported lead** *(answered: see §12, "
     "AY-6 closed - the slot is bound from `battle_pack.bin` `+0x3C`; 2026-10-02, OPUS)*, resting on"),
    (BTB, "**action names**, indexed by `action_data.bin` row `+0x34` |",
     "**action names**, indexed by ~~`action_data.bin`~~ action-table row `+0x34` *(answered: see the row-`+0x34` "
     "entry above - the table is `battle_pack.bin` `+0x3C`, AY-6; 2026-10-02, OPUS)* |"),
    # C-S3: the superseded load scan and the ~46-pointer headline.
    (REG, "| 60 of 63 slots referenced at a regular 8-byte stride |",
     "| 60 of 63 slots referenced at a regular 8-byte stride *(answered: see *Result: OVERTURNED on two of the three* "
     "below and the 64-slot extent; 2026-10-02, OPUS)* |"),
    (REG, "should be read as *\"most authored content is reached through one array of ~46 pointers, which sits\n",
     "should be read as *\"most authored content is reached through one array of ~46 pointers, which sits "
     "*(answered: see AG-2's ANSWERED 2026-09-26 - every one of the 64 slots has an identity; 2026-10-02, OPUS)*\n"),
    # ===================== 3.2: request queue and ownership =====================
    # C-S6: no once-per-frame guarantee.
    (RQ, "Called once per frame by `0032E040` when a loader is present (`001EDE80()` or `0017D930()`) —",
     "Called ~~once per frame~~ by `0032E040` when a loader is present (`001EDE80()` or `0017D930()`) " + C +
     "the wrapper carries no once-per-frame guarantee: the script native and `0032E520(0)` below call it inside wait "
     "loops; [the contract](CONTRACT-resource-request-queue.md)'s `0032E040()` row)* —"),
    (RQ, "pump once per frame / drain until idle",
     "pump ~~once per frame~~ when a loader is present (no frame guarantee, the contract's `0032E040()` row) / drain "
     "until idle"),
    # C-S7: the read issuer's first route is a stream open served from the file cache or the archive, never a loose file.
    (RQ, "| issue a read (loose file first, then the archive) |",
     "| issue a read (~~loose file first~~ the stream open first, then the archive *(answered: see the Presentation "
     "and Audio neighbour line below - "
     "`001D6F20` is a stream open served from the RAM file cache or the VBF, never a loose file, 2026-09-27; "
     "2026-10-02, OPUS)*) |"),
    (RQ, "(243 B — loose file, then archive)",
     "(243 B — ~~loose file~~ stream open, then archive *(answered: as above; 2026-10-02, OPUS)*)"),
    (RQ, "loose-file open (`001D6FB0`, `002DF808`) or the archive read (`001D6D90`, `002DF838`) — and the",
     "~~loose-file open~~ stream-open read (`001D6FB0`, `002DF808`) *(answered: `001D6F20`'s stream comes from the "
     "file cache or the VBF, as corrected below; 2026-10-02, OPUS)* or the archive read (`001D6D90`, `002DF838`) — "
     "and the"),
    (RQ, "             state 1 -> 0046E030 -> 002DF780 -> loose file (001D6F20 ..) or archive (001D6D90)\n",
     "             state 1 -> 0046E030 -> 002DF780 -> loose file (001D6F20 ..) or archive (001D6D90)   " + CC +
     "001D6F20 is a stream open (file cache or VBF), never a loose file\n"),
    (FST, "and the read goes through the loose-file check (`0017D930`, `001D6EF0`, `001D6B40`, `001D6F20`)",
     "and the read goes through the ~~loose-file check~~ stream-open check *(answered: see the Presentation and "
     "Audio neighbour line below - `001D6F20` opens a stream from the file cache or the VBF, never a loose file; "
     "2026-10-02, OPUS)* (`0017D930`, `001D6EF0`, `001D6B40`, `001D6F20`)"),
    # C-S37 (FST).
    (FST, "  mode, and the completion callback are unread (**FZ-12**).",
     "  mode, and the completion callback are unread (**FZ-12**) *(answered: see [the queue page](../the-resource-"
     "request-queue.md) §2.3, the six-state pump, and part A's done / cancel callbacks; 2026-10-02, OPUS)*."),
    (FST, "| `bin` | 1,439 | `'sloc'`, `'st2e'`, `'gmap'`, `'hctg'`, `'FLAG'`, `'CCdd'` | several layouts; `st2e` is documented |",
     "| `bin` | 1,439 | `'sloc'`, `'st2e'`, `'gmap'`, `'hctg'`, `'FLAG'`, ~~`'CCdd'`~~ " + C + "`CCdd` is not a "
     "magic: the 18 `face_guest08`/`09` copies open with byte-doubled image data, `43 43 64 64 6c 6c …`; [the PS2 "
     "README](../PS2-Image-Data-Formats/README.md), 2026-09-19)* | several layouts; `st2e` is documented |"),
    (FST, "**Open:** none of the eight has a loader sheet, and `dat` and `bin` cannot get one row each - the",
     "**Open:** none of the eight has a loader sheet *(answered: see the *Re-derived 2026-09-18* note below - six of "
     "the eight have one; 2026-10-02, OPUS)*, and `dat` and `bin` cannot get one row each - the"),
    (FST, "The `001D6FB0` read-item constructor's alloc/enqueue triple `001A1220`/`001A0A90`/`001A0BB0`",
     "The `001D6FB0` read-item constructor's ~~alloc/enqueue~~ alloc/run triple " + C + "`001D6FB0+0xC6` `mov r8b, "
     "1` makes `001A0BB0` run the item at once, `001A0BB0+0x29` `test r8b, r8b` to its `+0x2E` call; the 2026-09-30 "
     "correction below)* `001A1220`/`001A0A90`/`001A0BB0`"),
    # C-S8: the Windows overlap copy is answered.
    (EXT, "The deployed Windows copy-overlap dependency from SECTION-07 is still unresolved. SECTION-08's",
     "The deployed Windows copy-overlap dependency from SECTION-07 is ~~still unresolved~~ *(answered: see [the mover]"
     "(the-source-block-mover-and-separate-consumer-refresh.md) OV-46 and [the PRF page]"
     "(the-nonempty-prf-registration-and-specialized-relocation.md) OV-43 - the image imports `memcpy` from "
     "`VCRUNTIME140.dll` (IAT `008C2A68`) and that `memcpy` is overlap-safe; 2026-10-02, OPUS)*. SECTION-08's"),
    (ISR, "The Windows overlap-copy question from SECTION-07 remains separate. The native adapter rejects",
     "The Windows overlap-copy question from SECTION-07 ~~remains separate~~ *(answered: see [the mover]"
     "(the-source-block-mover-and-separate-consumer-refresh.md) OV-46 - overlap-safe; 2026-10-02, OPUS)*. The native "
     "adapter rejects"),
    # C-S9: held state1 and delivery are answered.
    (ISR, "bit has been consumed and its state is not2. A separate dispatcher or transition must be proved;",
     "bit has been consumed and its state is not2. ~~A separate dispatcher or transition must be proved;~~ *(answered: "
     "see OV-34 in §9 - none exists; 2026-10-02, OPUS)*"),
    (ISR, "admitted in normal gameplay. Delivery uniqueness and record-reuse ordering need their own evidence.",
     "admitted in normal gameplay. ~~Delivery uniqueness and record-reuse ordering need their own evidence.~~ "
     "*(answered: see OV-36 in §9 - at-most-once delivery; 2026-10-02, OPUS)*"),
    (OWNC, "| State1, hold gate later clears, producer sweep | No submission by this sweep; another actual submission route/trigger must be established. |",
     "| State1, hold gate later clears, producer sweep | No submission by this sweep; ~~another actual submission "
     "route/trigger must be established.~~ none exists *(answered: see [the indexed-source page]"
     "(the-indexed-source-request-from-arm-to-terminal-pump.md) OV-34; 2026-10-02, OPUS)* |"),
    (OWNC, "   the eventual submission policy for held state1; callback single-delivery/reuse preconditions;",
     "   ~~the eventual submission policy for held state1; callback single-delivery/reuse preconditions;~~ "
     "*(answered: see [the indexed-source page](the-indexed-source-request-from-arm-to-terminal-pump.md) OV-34 and "
     "OV-36; 2026-10-02, OPUS)*"),
    (RQC, "not normal recovery. The complete game-level recovery and held-owner dispatcher remain unresolved.",
     "not normal recovery. The complete game-level recovery ~~and held-owner dispatcher remain unresolved~~ remains "
     "unresolved; the held-owner dispatcher does not exist *(answered: see [the indexed-source page]"
     "(the-indexed-source-request-from-arm-to-terminal-pump.md) OV-34; 2026-10-02, OPUS)*."),
    # C-S10: four owner families.
    (OWN, "replace the old unrestricted question of whether ANY external owner is known. Other owner families,",
     "replace the old unrestricted question of whether ANY external owner is known. ~~Other owner families,~~ "
     "*(answered: see OV-25 above - exactly four owner families; 2026-10-02, OPUS)*"),
    # C-S12: the configuration table has a start-up producer.
    (PRF, "the two `@FEF`-specific inputs have no shipped producer - ~~the configuration table",
     "~~the two `@FEF`-specific inputs have no shipped producer~~ of the two `@FEF`-specific inputs only the `@FEF` "
     "data has no shipped producer " + C + "the configuration table's populator `0040A230` runs at start-up, "
     "`RenderResourceRoot_InitializeSubcontainers+0x6B` calling `00409F80`, which calls it at `00409F80+0x4`)* - "
     "~~the configuration table"),
    # ===================== 3.2: arena, tree, section addressing, expressions =====================
    (EFX, "No harness exists; §13 names the experiment: plant a small arena, record encoded offsets, rebase to",
     "~~No harness exists;~~ *(answered: see *Consumed 2026-09-16 (OPUS) from EXP-084* above - 52 / 52 cases; "
     "2026-10-02, OPUS)* §13 names the experiment: plant a small arena, record encoded offsets, rebase to"),
    (TREE, "independent reconstruction parity or whole-game lifetime proof; the 4 GiB wrap is a fixture-only hazard unless the allocator's",
     "independent reconstruction parity or whole-game lifetime proof; ~~the 4 GiB wrap~~ the codec-domain overflow "
     "*(answered: see *Outside the codec domain*, corrected 2026-09-15 from \"4 GiB wrap\"; 2026-10-02, OPUS)* is a "
     "fixture-only hazard unless the allocator's"),
    (TREE, "(§4 already says it is not re-derived here), the 4 GiB narrowing inherited from",
     "~~(§4 already says it is not re-derived here)~~ *(answered: see §4, re-derived 2026-09-18; 2026-10-02, OPUS)*, "
     "the 4 GiB narrowing inherited from"),
    (TREE, "bytes — the rebalancing is ASTRA's reading, §4). Every link store goes through `0020E620` and every",
     "bytes — the rebalancing is ~~ASTRA's reading~~ byte-proven, §4 *(answered: re-derived 2026-09-18; 2026-10-02, "
     "OPUS)*). Every link store goes through `0020E620` and every"),
    (TREE, "one. The ordering key at `+0x18` is the quantity the arena orders by (ASTRA calls it a payload",
     "one. The ordering key at `+0x18` is the quantity the arena orders by " + C + "it is the payload byte length "
     "the mover copies: `0036A2A0+0x2B` `mov r13d, dword ptr [r8 + 0x18]` passes it at `0036A2A0+0x100` / "
     "`+0x107` to the copy; §4's `+0x18` bullet)* (ASTRA calls it a payload"),
    (TREE, "length; signed comparison proven, the quantity itself not).",
     "length; signed comparison proven, ~~the quantity itself not~~ the quantity too, as corrected above)."),
    (TREE, "| **what the `+0x18` key measures** | **not established** | none |",
     "| **what the `+0x18` key measures** | ~~**not established**~~ the allocated payload-byte extent the mover "
     "copies *(answered: see §4's `+0x18` bullet; `0036A2A0+0x2B`; 2026-10-02, OPUS)* | none |"),
    (TREE, "node's +18 ordering key remains as previously bounded, not silently solved by this new lifecycle.",
     "node's +18 ordering key ~~remains as previously bounded, not silently solved by this new lifecycle~~ is the "
     "payload-byte extent *(answered: see §4's `+0x18` bullet, SECTION-07; 2026-10-02, OPUS)*."),
    (RSA, "> `types_index.py` cannot validate a width it has never been told about, and the nine functions that",
     "> `types_index.py` cannot validate a width it has never been told about, and the ~~nine functions~~ eleven "
     "functions *(answered: see *There are 17 call sites in 11 functions, not nine* below; 2026-10-02, OPUS)* that"),
    (RSA, "DESCRIPTOR carries at `+0x48`. It is never a heap object, which is why no allocation site exists to",
     "DESCRIPTOR carries at `+0x48`. It is never ~~a heap object~~ its own heap object (the bank blob it sits in is "
     "heap-allocated by `0051F9F0`, *(answered: see the `RS-1` answer below; 2026-10-02, OPUS)*), which is why no "
     "allocation site exists to"),
    (RSA, "descriptor, not an immediate anywhere in `.text`. **The extent is authored data.** Declaring `0x40`",
     "descriptor, not an immediate anywhere in `.text`. ~~**The extent is authored data.**~~ *(answered: see the "
     "`RS-1` answer below - falsified by the writer, the geometry comes from `.text` immediates; 2026-10-02, OPUS)* "
     "Declaring `0x40`"),
    (RND, "> a single call varies. So the sequence a player gets is decided entirely by **whatever seeds these",
     "> a single call varies. So the sequence a player gets is decided entirely by ~~**whatever seeds these~~ "
     "**the boot seeder `00259180`** " + C + "`00259180+0x96` stores `0x458DC800` to `01EF93E8` and `00259180+0xA0` "
     "stores 1 to `022D9138`, called once at boot; the key-addresses table)*"),
    (RND, "> at runtime, which is not established**, and a reimplementation that seeded them differently would",
     "> ~~at runtime, which is not established**~~, and a reimplementation that seeded them differently would"),
    (RND, "      `00431080`, which is unread.",
     "      ~~`00431080`, which is unread.~~ `00431080`, which draws nothing *(answered: read 2026-09-18, §2's table; "
     "it calls only the resolver and the spline helpers, never `003A6E60`; 2026-10-02, OPUS)*."),
    (RND, "- **What the other eleven bits of `+0x0E` mean.** Only bits 4–7 are the operator.",
     "- **What the other ~~eleven~~ eight bits of `+0x0E` mean.** Only bits 4–7 are the operator *(answered in part: "
     "bits 0–1 and 2–3 select the A and B curves, `00431080+0x47` `shr ecx, 2` and `+0x4D` `and ecx, 3`, §2's table; "
     "2026-10-02, OPUS)*."),
    (AEC, "* **The other eleven bits of `+0x0E`** — only bits 4–7 are the operator **[page]**.",
     "* **The other ~~eleven~~ eight bits of `+0x0E`** — only bits 4–7 are the operator *(answered in part: bits 0–3 "
     "are the A and B curve selectors, `00431080+0x47` and `+0x4D`; 2026-10-02, OPUS)* **[page]**."),
    (RND, "      the zero-bound path keeps only ops 4 and 5 (`004313F3`–`004313FB`).",
     "      the zero-bound path ~~keeps only ops 4 and 5~~ tests ops 4 and 5 and only op 5 draws "
     "(`004313F3`–`004313FB`) " + C + "op 4 there returns `a` at `00431350+0xB1`; §3's *Only operator 5 survives "
     "it*)*."),
    (RND, "~~it is where the operand space\n  actually lives, and it takes a *context* argument this page passes through without inspecting.",
     "~~it is where the operand space~~\n  ~~actually lives, and it takes a *context* argument this page passes "
     "through without inspecting.~~ " + C + "the strike opened on the line above now closes on each line)*"),
    (EV, "from a table either. **So no in-image code can obtain a pointer to `01F83530` at all**",
     "from a table either. ~~**So no in-image code can obtain a pointer to `01F83530` at all**~~ " + C + "one in-image store reaches it: "
     "the texture-id table writer `00210570` bounds the id only from above with a signed compare (`00210570+0x5` "
     "`cmp cx, ax`, `+0x8` `jge`), so id `0xFFFB` (-5) stores at `01F83580 - 0x50` = `01F83530` "
     "(`00210570+0x18` `mov qword ptr [rcx + rax*8], rdx`); the 2026-09-25 scope correction above)*"),
    (EV, "8 under the observed identity map; do not assume that mapping in every state.",
     "8 under the observed identity map; ~~do not assume that mapping in every state.~~ *(answered: see Limits 4 - "
     "the map `022D89A8` is written only by its two identity fills, so source *n* selects arena *n* in every state; "
     "2026-10-02, OPUS)*"),
    (EV, "Logical source 6 is actual arena 6 under the observed identity map; the map\nmust not be assumed immutable in every state.",
     "Logical source 6 is actual arena 6 under the observed identity map; ~~the map~~\n~~must not be assumed "
     "immutable in every state.~~ *(answered: see Limits 4; 2026-10-02, OPUS)*"),
    (ROW, "begins as zero, and no instruction in the image writes it — nor on the `.data` dword at `01DFE0B4`.",
     "begins as zero, and ~~no instruction in the image writes it~~ one in-image store can write it " + C + "the "
     "texture-id table writer's `+0x18` reaches it for id `0xFFFB`, its `+0x5` compare being signed; undriven, not "
     "absent - §7's reconciliation)* — nor on the `.data` dword at `01DFE0B4`."),
    # ===================== 3.2: archive, st2e, carriers =====================
    (VBF, "is an unmapped byte (almost certainly `&`). **AY-8.**\n",
     "is an unmapped byte (almost certainly `&`). **AY-8.** *(answered: see AY-8 above, 2026-09-18 - the byte `0xA0` "
     "is `&`; 2026-10-02, OPUS)*\n"),
    (VBF, "`battle_pack.bin` (281 KB, same directory) is the obvious unopened candidate. **AY-9.**\n",
     "`battle_pack.bin` (281 KB, same directory) is the obvious unopened candidate. **AY-9.** *(answered: see §9 and "
     "§12 - the pack is opened and binds the action table; AY-9 is ANSWERED; 2026-10-02, OPUS)*\n"),
    (VBF, "those twelve bytes are an unread header on the directory (**PROPOSED-reposd2-9**).",
     "those twelve bytes are an unread header on the directory (**PROPOSED-reposd2-9**) *(answered: see UQ-74, "
     "2026-09-14 - a status word and a directory slot, not one header; 2026-10-02, OPUS)*."),
    (BIG, "  -> FUN_0059F4A0        ReadFile leaf, 12 callers  (Resource, Audio)\n",
     "  -> FUN_0059F4A0        ReadFile leaf, 12 callers  (Resource, Audio)   " + CC + "archive blocks arrive through "
     "CRT fread instead, 0019A860+0x71 (§5 table)\n"),
    (BIG, "a message or an exit. Which of the two `CreateFileA` sites opens what. The residual gap §8 already",
     "a message or an exit. ~~Which of the two `CreateFileA` sites opens what.~~ *(answered: see the §7 box - "
     "minidump files, 2026-09-27; 2026-10-02, OPUS)* The residual gap §8 already"),
    (BKT, "units, six token families no document names, an open tail. `.dat` is refused for a different,",
     "units, ~~six token families no document names~~ six token families since named *(answered: see the table "
     "below - all six bound 2026-09-29; 2026-10-02, OPUS)*, an open tail. `.dat` is refused for a different,"),
    (BKT, "- **Not settled:** `.bin`'s families. `sloc`+`st2e` are 58.6% of `.bin`, six `.bin` token families\n",
     "- **Not settled:** `.bin`'s families. `sloc`+`st2e` are 58.6% of `.bin`, six `.bin` token families *(answered: "
     "all six bound 2026-09-29, the table above; 2026-10-02, OPUS)*\n"),
    (S2R, "**Neither is explained; both are recorded rather than smoothed over.**",
     "**~~Neither is explained;~~ both are recorded rather than smoothed over.** *(answered: see [the loader sheet]"
     "(how-the-ard-loader-binds-area-battle-data.md) - the 85 `.ard`-less areas need no battle data, and `in` / `ch` "
     "are the two region variants of the path table; 2026-10-02, OPUS)*"),
    (S2R, "That is the shape of a directory, and it is a **lead, not a reading**: no loader has been consulted.",
     "That is the shape of a directory, and it is a **lead, not a reading**: ~~no loader has been consulted.~~ "
     "*(answered: see [the loader sheet](how-the-ard-loader-binds-area-battle-data.md), which reads the binder; "
     "2026-10-02, OPUS)*"),
    (S2R, "+0x08  u64  fpkPath   char* to the matching .fpk path - USUALLY NULL\n",
     "+0x08  u64  fpkPath   char* to the matching .fpk path - USUALLY NULL   " + CC + "null exactly where ardPath is "
     "null; all 215 .ard records carry an .fpk path\n"),
    (S2R, "(`…\\ttl_a\\area\\ttl_a.fpk`). It is null in 33 of the first 40 records.",
     "(`…\\ttl_a\\area\\ttl_a.fpk`). It is null in ~~33~~ 37 of the first 40 records " + C + "both shipped arrays, "
     "`01E0CFA0` and `01EDC280`: the 37 are exactly the records whose `.ard` path is null too, and 215 of 215 `.ard` "
     "records carry an `.fpk`)*."),
    (S2R, "- whether the 71-slot `battle_pack` directory is the same layout as EBP2's and PKFL's, or merely\n",
     "- whether the 71-slot `battle_pack` directory is the same layout as EBP2's and PKFL's, or merely *(answered: "
     "see the 2026-09-04 correction above - it is not; 2026-10-02, OPUS)*\n"),
    (LDR, "among the offset-shaped fields, **nothing reads it** (§3).",
     "among the offset-shaped fields, ~~**nothing reads it**~~ the loader does not read it *(answered: see CC-8 in §7 "
     "- `003EA650` reads it through the root accessor; 2026-10-02, OPUS)* (§3)."),
    (LDR, "areas* is not padding — **it is authored data the shipped engine ignores.** That is the same shape as",
     "areas* is not padding — ~~**it is authored data the shipped engine ignores.**~~ *(answered: see CC-8 - the "
     "trailer is read; 2026-10-02, OPUS)* That is the same shape as"),
    (LDR, "  > removes the `.fpk` half of §5's \"third instance of one shape\" — `trailerOff` and the 49 dead",
     "  > removes the `.fpk` half of §5's \"third instance of one shape\" — ~~`trailerOff` and~~ *(answered: "
     "`trailerOff` is read, CC-8; 2026-10-02, OPUS)* the 49 dead"),
    (LDR, "shipped copies are byte-identical, so the redundancy is packaging; *why those two trees* remains\nopen.",
     "shipped copies are byte-identical, so the redundancy is packaging; ~~*why those two trees* remains~~\n~~open.~~ "
     "*(answered: see CC-9 below - the two path-table region variants; 2026-10-02, OPUS)*"),
    (NMB, "overwrites the slot with the `ch` array.** So the default build reaches `in\\...` paths and exactly\none region reaches `ch\\...`",
     "overwrites the slot with the `ch` array.** So the default build reaches `in\\...` paths and ~~exactly~~\n~~one "
     "region reaches `ch\\...`~~ three regions reach `ch\\...` " + C + NMBCH + "; §8's locale table)*"),
    (NMB, "`.ard` in a separate 16-byte record array at 215 per tree.",
     "`.ard` ~~in a separate 16-byte record array at 215 per tree~~ in `g_pathTables[21]`, a flat `char*[]` at 8-byte "
     "stride with 215 `.ard` at even and 215 `.fpk` at odd indices " + C + "the `.ard` contract's AB-3)*."),
    (NMB, "- **The three 2000-entry arrays in the §3 table are lower bounds**, cut off by the profiler's walk",
     "- **The three 2000-entry arrays in the §3 table are lower bounds** *(answered: see §3 - the `entries` column "
     "is withdrawn, 2026-09-04; 2026-10-02, OPUS)*, cut off by the profiler's walk"),
    (ARDC, "the head, which is 24 NULLs**. Count the category-setter calls in both bodies and assert five and ten",
     "the head, which is 24 NULLs**. Count the category-setter calls in both bodies and assert five and ~~ten~~ "
     "fifteen " + C + "the binder makes 5 and the reader 15, the three groups of five AB-7 lists)*"),
    (BTB, "  10, 10`). How the engine composes `13000 + n` into `130000 + n` is not read; the correspondence",
     "  10, 10`). ~~How the engine composes `13000 + n` into `130000 + n` is not read;~~ *(answered: see §7 - nothing "
     "composes it, the row stores the second id; 2026-10-02, OPUS)* the correspondence"),
    (BTB, "call the input helpers `001E0B90` and `0017DE60` — the bank playback path consults input state.",
     "call ~~the input helpers `001E0B90` and~~ a keyboard-layout language selector (French 1, German 2, else 0, from "
     "`GetKeyboardLayout`) and the input helper `0017DE60` " + C + "the first is no input poll, the SWE2-EC7-71 update "
     "below)* — the bank playback path consults ~~input state~~ the layout language and input state."),
    # ===================== 3.2: prefetch, .ah, .ta, standard formats =====================
    (PJR, "reservation) or merely records it (a build-time note). `common.txt` additionally carries category",
     "reservation) or merely records it (a build-time note) *(answered: see [the manifest sheet]"
     "(how-the-prefetch-manifests-are-read.md) - the engine discards the `##Total_data_Size` line; 2026-10-02, "
     "OPUS)*. `common.txt` additionally carries category"),
    (PJR, "(`274,0,240,0`) — unexamined.",
     "(`274,0,240,0`) — ~~unexamined~~ *(answered: see [the manifest sheet](how-the-prefetch-manifests-are-read.md) - "
     "`%d,%d,%d,%d` quads with no per-record request; 2026-10-02, OPUS)*."),
    (PFM, "> One flat list of asset paths per scene, read at game start and at every map entry, to pull files",
     "> One flat list of asset paths per scene, read at game start and at every map entry, ~~to pull files~~ to "
     "resolve and mark each path *(answered: see §3's *CORRECTED 2026-09-21* - a prefetch token is never read; "
     "2026-10-02, OPUS)*"),
    (PFM, "layer** — not established here, and named in §7.",
     "layer** — ~~not established here, and named in §7~~ *(answered: see [the path resolver]"
     "(../VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md) - the two key builders, at lookup "
     "time; 2026-10-02, OPUS)*."),
    (PFM, "| `0x0018A330` | the scan routine the parser calls | ❌ entry only |",
     "| `0x0018A330` | the scan routine the parser calls | ~~❌ entry only~~ read *(answered: see [the `.ah` sheet]"
     "(ah-asset-header-manifests.md)'s interior citation of `0018A330`; 2026-10-02, OPUS)* |"),
    (PFM, "| `0x00597970` | the file-cache request —",
     "| `0x00597970` | ~~the file-cache request~~ the stream-reader constructor *(answered: see [the path resolver]"
     "(../VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md); 2026-10-02, OPUS)* —"),
    (PFM, "  non-zero the djb2 index route; what `5` stamps on the resolved entry is still unestablished.",
     "  non-zero the djb2 index route; ~~what `5` stamps on the resolved entry is still unestablished.~~ *(answered: "
     "see [the path resolver](../VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md) - selector 5 "
     "bumps a counter and stamps the entry, 2026-09-30; 2026-10-02, OPUS)*"),
    (PFM, "  archive's are not; the resolution layer was not read.",
     "  archive's are not; ~~the resolution layer was not read.~~ *(answered: see [the path resolver]"
     "(../VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md); 2026-10-02, OPUS)*"),
    (AH, "| `0x0018A330` | the token scanner both manifest families call | ❌ entry only |",
     "| `0x0018A330` | the token scanner both manifest families call | ~~❌ entry only~~ read *(answered: see the "
     "interior citation of `0018A330` below; 2026-10-02, OPUS)* |"),
    (AH, "**No `.ah` file was opened.** `gamedata/d3d11` is not in the local extraction and no `.vbf` exists on",
     "**No `.ah` file was opened.** *(answered: see the corpus table - all 2,564 opened 2026-09-13, §7; 2026-10-02, "
     "OPUS)* `gamedata/d3d11` is not in the local extraction and no `.vbf` exists on"),
    (AH, "- **The five monster and one npc assets missing a `chr_shadow` header** — counted, not explained.",
     "- **The five monster and ~~one npc~~ two npc assets missing a `chr_shadow` header** " + C + "the 2026-09-13 "
     "recount in §3)* — counted, not explained."),
    (AH, "- **Anything measured from a `.ah` file**, for the reason in §5.",
     "- **Anything measured from a `.ah` file**, for the reason in §5 *(answered: see the corpus table - all 2,564 "
     "measured 2026-09-13; 2026-10-02, OPUS)*."),
    (TA, "| `002F4520` | the rendering pass that supplies the frame number (call at `002F4A5D`) | ✗ `TA-1` |",
     "| `002F4520` | the rendering pass that supplies the frame number (call at `002F4A5D`) | ~~✗ `TA-1`~~ "
     "*(answered: `TA-1` answered 2026-09-25 below; 2026-10-02, OPUS)* |"),
    (TA, "## 6. Falsification pass\n\nNot yet run.",
     "## 6. Falsification pass\n\n~~Not yet run.~~ *(answered: see §9, Falsification pass 1 - 2026-09-13; "
     "2026-10-02, OPUS)*"),
    (TA, "all seven frames bind to null at run time unless the textures are loaded under those paths by some\nother route (`TA-2`).",
     "all seven frames bind to null at run time ~~unless the textures are loaded under those paths by some~~\n~~other "
     "route~~ (`TA-2`) *(answered: see UQ-71 - the frames stay null; 2026-10-02, OPUS)*."),
    (SF, "494 and 495. Which routine copies the pool files into the slot is not read (`FR-2`). `system.cnf`",
     "494 and 495. ~~Which routine copies the pool files into the slot is not read (`FR-2`).~~ *(answered: see FR-2 "
     "in §7 - there is no such routine, 2026-09-26; 2026-10-02, OPUS)* `system.cnf`"),
    (SF, "None — this sheet is about files. The readers of `.json` (the engine's JSON parser), `.tga` and",
     "~~None~~ *(answered: the body cites the player `001B7F30`, the parser `00801210`–`00806F20` and the save-slot "
     "name builders `SavePath_FormatSlotAssetName` / `SavePath_BuildSlotAssetName`; 2026-10-02, OPUS)* — this sheet is about files. The readers of `.json` "
     "(the engine's JSON parser), `.tga` and"),
    # ===================== 3.2: PS2-era formats =====================
    (TIM2, "| `0x0039BF50` | slot initialiser, called once per newly claimed slot | ❌ not read |",
     "| `0x0039BF50` | slot initialiser, called once per newly claimed slot | ~~❌ not read~~ read *(answered: see the "
     "SWE2-EC7-91 update below; 2026-10-02, OPUS)* |"),
    (TIM2, "- **What the decoder does with the other fields**, or what `FUN_0039BF50` initialises.",
     "- **What the decoder does with the other fields**, ~~or what `FUN_0039BF50` initialises~~ *(answered for "
     "`0039BF50`: see the SWE2-EC7-91 update below; 2026-10-02, OPUS)*."),
    (TIM2, "`02AEE868`. `FUN_0039BF50` is still unread.",
     "`02AEE868`. ~~`FUN_0039BF50` is still unread.~~ *(answered: see the SWE2-EC7-91 update below; 2026-10-02, OPUS)*"),
    (CMAP, "u16  pad;    /* +4 = 0 in all 77 */\n",
     "u16  pad;    /* +4 = 0 in all 77 */   /* " + CC + "read: the guide-text request adds this byte to 0x496 (gmap "
     "sheet G2) */\n"),
    (HIMG, "  passed to `00249210`; the record field `+2` added in state 1 (a file-index delta, but which\n",
     "  passed to `00249210`; the record field `+2` added in state 1 (a file-index delta, but which *(answered: see "
     "[the index sheet](hchk-hctg-hdat-handbook-indexes.md) - `00575D10` fills it from the record's `+0x06` "
     "`hdatFile`; 2026-10-02, OPUS)*\n"),
    (CHSE, "Audio-filed helper. What that helper does is not read here.",
     "Audio-filed helper. ~~What that helper does is not read here.~~ *(answered: see the line below - the helper is "
     "the SE block registration; 2026-10-02, OPUS)*"),
    # C-S52: section numbers.
    (WMAP, "> Every count is reproduced by the shipped generator header `menumap_world.h` (§5), and every",
     "> Every count is reproduced by the shipped generator header `menumap_world.h` (~~§5~~ §4 " + C + "the "
     "header-constant section is §4)*), and every"),
    (WMAP, "> name field resolves into `menu_mapname.bin`'s string-id table (§6).",
     "> name field resolves into `menu_mapname.bin`'s string-id table (~~§6~~ §5 " + C + "the 60000-range ids are "
     "§5)*)."),
    (WMAP, "every differing byte sits inside the area table's position/label fields; **no id or route byte ever differs** (§7) |",
     "every differing byte sits inside the area table's position/label fields; **no id or route byte ever differs** "
     "(~~§7~~ §6 " + C + "locale behaviour is §6)*) |"),
    (LMAP, "[wmap-menumap-world-map-graph.md](wmap-menumap-world-map-graph.md) §6 and",
     "[wmap-menumap-world-map-graph.md](wmap-menumap-world-map-graph.md) ~~§6~~ §5 " + C + "the join and the "
     "id-space map are its §5)* and"),
]


def _rx(s):
    return re.compile(re.escape(s).replace("\\\n", "\r?\n").replace("\n", "\r?\n"))


def _endings(m):
    return re.findall(r"\r?\n", m)


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel)
        if t is None:
            t = open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if _rx(new).search(t):
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hits = list(_rx(old).finditer(t))
        if len(hits) != 1:
            print("REFUSING", rel.split("/")[-1], len(hits), old[:50]); fails += 1; texts[rel] = t; continue
        m = hits[0]
        ends = _endings(m.group(0))
        parts = new.split("\n")
        if len(parts) - 1 == len(ends):
            n = "".join(p + (ends[i] if i < len(ends) else "") for i, p in enumerate(parts))
        else:
            n = new.replace("\n", ends[0] if ends else "\n")
        texts[rel] = t[:m.start()] + n + t[m.end():]
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
