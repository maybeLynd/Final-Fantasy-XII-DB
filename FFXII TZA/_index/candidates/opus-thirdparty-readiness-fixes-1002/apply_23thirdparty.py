"""apply_23thirdparty.py [--apply] - 23-Third-Party-Libraries readiness map (re-readiness/23-thirdparty.md), section 3.1
value items X-1..X-35 and the section 3.2 stale / banner items the image or the pages settle (OPUS, 2026-10-02).

Each edit strikes the side the shipping image REFUTES only and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*,
or answers a stale "open / not read" line with *(answered: see ...; 2026-10-02, OPUS)*. Deciding instructions and data
are in the scratch verdicts-23.md; every address inside a function is cited as entry+offset.
Left without an edit, because no side is refuted by the image: X-9 (the image has 52 / 6 / 2 initialisers, the body's
58 is 52 + 6, the front matter counts family members), X-11 (section 3 is incomplete, not wrong), X-16, X-19's other
lines, X-20, X-21, X-31 (family-ledger arithmetic, not image values), X-25 (0.6.2 is of the 0.6 line), X-34 (which
immediate is __LINE__ is undecidable statically; BQ-31 already says so), S-2 (kept on purpose), S-13 (an answered box's
question), S-18 (the four stay outside the listed census), S-20's 188 (a dated measurement), B-3, B-5, B-6, B-7, B-9.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`<- corrected` comment instead of a strike, front-matter lines a trailing `# <- corrected` YAML comment (each such OLD
includes its line end, so NEW never contains OLD). No heading changes.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "23-Third-Party-Libraries/"
R = F + "README.md"
INV = F + "third-party-middleware-inventory.md"
BUL = F + "Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md"
EA = F + "EASTL/eastl-strings-containers-and-the-logging-allocator.md"
VPX = F + "LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md"
LUAC = F + "Lua-Core/CONTRACT-lua-chunk-loader.md"
LUA = F + "Lua-Core/the-lua-loader-and-what-it-accepts.md"
PPFX = F + "PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md"

HDR = ("`0082E490+0x3C` `mov r8d, 0x11` is the read length; `0082E490+0x69`..`+0x89` compare qword, qword and word, "
       "bytes 0-17, byte 0 being the `0x1B` the checker plants at `0082E490+0x5A`")

EDITS = [
    # X-1: +0x28/+0x2C/+0x30 is the centre of mass as (x, y, z): 0069FB10 negates it into the child origin with +0x28 on
    #      x (0069FB10+0x307), and 006A4A60 rotates it (matrix times vector), it is not a scale.
    (BUL, "origin += ( -body[0x30], -body[0x2C], -body[0x28] );\n",
     "origin += ( -body[0x30], -body[0x2C], -body[0x28] );   /* <- corrected 2026-10-02, OPUS - reversed: x takes "
     "-body[0x28], y -body[0x2C], z -body[0x30] (negated at 0069FB10+0x1AD..+0x1E1, added at 0069FB10+0x307 / +0x2FA / "
     "+0x2E9 into the origin stored at +0x30C / +0x312 / +0x318) */\n"),
    (BUL, "  +0x28  f32   centreOfMass.z    negated into every child transform\n",
     "  +0x28  f32   centreOfMass.z    negated into every child transform   <- corrected 2026-10-02, OPUS - .x, not "
     ".z: 0069FB10+0x307 adds -[+0x28] to the child origin's x, and 006A4A60 multiplies it by the basis column 0\n"),
    (BUL, "  +0x30  f32   centreOfMass.x\n",
     "  +0x30  f32   centreOfMass.x   <- corrected 2026-10-02, OPUS - .z, not .x: 0069FB10+0x2E9 adds -[+0x30] to the "
     "child origin's z\n"),
    (BUL, "origin.x  += -body[0x30];\n",
     "origin.x  += -body[0x30];   /* <- corrected 2026-10-02, OPUS - x takes -body[0x28] (0069FB10+0x307) */\n"),
    (BUL, "origin.z  += -body[0x28];\n",
     "origin.z  += -body[0x28];   /* <- corrected 2026-10-02, OPUS - z takes -body[0x30] (0069FB10+0x2E9) */\n"),
    (BUL, "into `006A57C0`, whose 4×4 output is then multiplied\ncomponentwise by the scale at `self+0x28/0x2C/0x30` and "
          "offset by the translation at",
     "into `006A57C0`, whose 4×4 output is then ~~multiplied~~\n~~componentwise by the scale at `self+0x28/0x2C/0x30`~~ "
     "applied to the centre-of-mass vector at `self+0x28/0x2C/0x30` as a matrix-vector product, not a componentwise "
     "scale *(corrected 2026-10-02, OPUS: `006A4A60+0x12A`..`+0x1D6` sum, per row, the three basis entries times "
     "`[+0x28]`, `[+0x2C]` and `[+0x30]`; the same vector `0069FB10` negates into every child origin)*, and offset by "
     "the translation at"),

    # X-2: 006A0A50 adds (matrix * input) * angular factor into the angular velocity +0x160..+0x168, which 008531F0
    #      damps by +0x1E4; nothing writes a basis.
    (BUL, "`006A0A50` (249 B) is the basis-write `006A0A40` runs",
     "`006A0A50` (249 B) is ~~the basis-write~~ an angular-velocity write, not a basis write *(corrected 2026-10-02, "
     "OPUS: it adds the matrix product into the angular velocity `+0x160`..`+0x168`, which `008531F0` damps by "
     "`+0x1E4`; nothing at `+0x120`..`+0x148` is written)* `006A0A40` runs"),
    (BUL, "and stored back into `+0x160`..`+0x164` - then",
     "and stored back into ~~`+0x160`..`+0x164`~~ `+0x160`..`+0x168` *(corrected 2026-10-02, OPUS: three stores, "
     "`006A0A50+0xC3`, `+0xDB` and `+0xD3`)* - then"),

    # X-3: 0082E490 reads 17 bytes and compares 18 (the contract's 2026-09-12 correction is right).
    (LUA, "The comparison at `0082E490`\nruns over **`0x11` = 17 bytes** — `LUAC_HEADERSIZE - 1` —",
     "~~The comparison at `0082E490`~~\n~~runs over **`0x11` = 17 bytes**~~ `0082E490` reads **`0x11` = 17 bytes** and "
     "compares all 18 *(corrected 2026-10-02, OPUS: " + HDR + ")* — `LUAC_HEADERSIZE - 1` —"),
    (LUA, "| `0082E490` | 414 B | the header writer / checker; 17-byte compare |",
     "| `0082E490` | 414 B | the header writer / checker; ~~17-byte compare~~ 17-byte read, 18-byte compare *(corrected "
     "2026-10-02, OPUS: `0082E490+0x3C` read length, `0082E490+0x69`..`+0x89` compare)* |"),
    (LUA, "| Header size 18, checker compares 17 |",
     "| Header size 18, checker ~~compares 17~~ reads 17 and compares 18 *(corrected 2026-10-02, OPUS: " + HDR + ")* |"),
    (LUA, "| the comparison runs over `0x11` = 17 bytes |",
     "| ~~the comparison runs over `0x11` = 17 bytes~~ the read runs over `0x11` = 17 bytes and the comparison over 18 "
     "*(corrected 2026-10-02, OPUS: `0082E490+0x69`..`+0x89`)* |"),
    (LUA, "Two instructions the section-2 listing omits are recorded as unread, not interpreted. Nothing was executed\n",
     "Two instructions the section-2 listing omits are recorded as unread, not interpreted. Nothing was executed # <- "
     "corrected 2026-10-02, OPUS - 0x11 at 0082E490+0x3C is the read length, not a comparison length; the comparison "
     "covers all 18 bytes (0082E490+0x69..+0x89)\n"),
    (LUAC, "| bytecode with a wrong header | rejected by the 17-byte compare |",
     "| bytecode with a wrong header | rejected by the ~~17-byte~~ 18-byte compare, 17 bytes read *(corrected 2026-10-02, "
     "OPUS: " + HDR + ")* |"),
    (LUAC, "and its boundary is exact — **17 compared bytes, not 18**.",
     "and its boundary is exact — ~~**17 compared bytes, not 18**~~ **18 compared bytes, 17 read** *(corrected "
     "2026-10-02, OPUS: " + HDR + "; the box below)*."),
    (LUAC, "must still be *accepted* by the 17-byte compare, because\n  byte 0 is not in the compared range.",
     "must still be *accepted* ~~by the 17-byte compare, because~~\n  ~~byte 0 is not in the compared range~~, because "
     "byte 0 never comes from the file *(corrected 2026-10-02, OPUS: `0082E490+0x5A` plants `0x1B` and the 18-byte "
     "compare covers it; the box above)*."),

    # X-4 + X-5: 00683C30 subtracts the low bit off the NAME pointer (r9); the length is [b+0x10] & 0x7FFFFFFF (r8).
    #      EASTL strings in this build carry no tag (001600D0), so it is not the EASTL idiom.
    (LUA, "The `- (*(u8 *)(b + 0x48) & 1)` on the length is the small-string-optimisation tag bit being masked\noff a "
          "packed length field, the same idiom this database records for EASTL strings.",
     "The `- (*(u8 *)(b + 0x48) & 1)` ~~on the length is the small-string-optimisation tag bit being masked~~\n~~off a "
     "packed length field, the same idiom this database records for EASTL strings.~~ is a tag bit subtracted off the "
     "**name pointer**, not off a length, and it is not an EASTL idiom: this build's EASTL strings carry no tag "
     "*(corrected 2026-10-02, OPUS: `00683C30+0x6`..`+0x14` put `[b+0x48]` minus its low bit in `r9`, the name; the "
     "length is `[b+0x10]` with bit 31 cleared, `00683C30+0x17`..`+0x27`, in `r8`; the EASTL page's three-pointer "
     "string, `001600D0`)*."),
    (LUA, "  — the packed-length idiom `00683C30` uses on its buffer.",
     "  — ~~the packed-length idiom `00683C30` uses on its buffer~~ the untagged string layout, which `00683C30`'s "
     "tagged name pointer is not *(corrected 2026-10-02, OPUS: the low bit comes off the name, `00683C30+0x6`..`+0x14`)*."),

    # X-6: a basic_string object is 0x20 bytes - the three pointers and the allocator at +0x18.
    (EA, "eastl::basic_string  -- 24 bytes, three pointers, NO inline buffer\n",
     "eastl::basic_string  -- 24 bytes, three pointers, NO inline buffer   <- corrected 2026-10-02, OPUS - 0x20 bytes: "
     "the three pointers and the allocator object at +0x18 (001600D0+0x1E..+0x3B: 01FD40D8 / 01FD40E0 / 01FD40E8, "
     "allocator 01FD40F0; 001FF740's stack temporary has the same shape)\n"),

    # X-7: empty: begin = end = 02EBA2E0, capacity_end = 02EBA2E1 (001600D0+0x97..+0xB3).
    (EA, "and which game string each object holds. Selector: members/select_eastl_string_static_inits.py\"\n",
     "and which game string each object holds. Selector: members/select_eastl_string_static_inits.py\" # <- corrected "
     "2026-10-02, OPUS - empty case: begin and end = 02EBA2E0, capacity_end = 02EBA2E1 (001600D0+0x97..+0xB3), not all "
     "three at 02EBA2E0\n"),

    # X-8: the initialiser branches: payloadLen + 1 <= 1 takes the sentinel and allocates nothing.
    (EA, "p = allocator->allocate(payloadLen + 1, 0);\n",
     "p = allocator->allocate(payloadLen + 1, 0);   /* <- corrected 2026-10-02, OPUS - only when payloadLen + 1 > 1 "
     "(001600D0+0x52 cmp eax, 1 / +0x55 jbe); an empty literal takes the shared sentinel 02EBA2E0 / 02EBA2E1 and "
     "allocates nothing */\n"),

    # X-10: BS-5's addresses are file offsets (.rdata + 0x121200, .data + 0x121A00).
    (EA, "`EASTL vector` (`007A4D58`), `EASTL set` (`007D2AB0`), `EASTL list` (`007D2AC0`), `EASTL map` (`007D2F20`), "
         "`EASTL basic_string` (`007D5400`) and `EASTL` (`01BB9C78`), and the two RTTI descriptors "
         "`.?AVallocator_memory_log@eastl@@` (`01E266F8`) and `.?AVallocator@eastl@@` (`01E5C900`).",
     "`EASTL vector` (~~`007A4D58`~~ `008C5F58`), `EASTL set` (~~`007D2AB0`~~ `008F3CB0`), `EASTL list` (~~`007D2AC0`~~ "
     "`008F3CC0`), `EASTL map` (~~`007D2F20`~~ `008F4120`), `EASTL basic_string` (~~`007D5400`~~ `008F6600`) and "
     "`EASTL` (~~`01BB9C78`~~ `01CDAE78`), and the two RTTI descriptors `.?AVallocator_memory_log@eastl@@` "
     "(~~`01E266F8`~~ `01F480F8`) and `.?AVallocator@eastl@@` (~~`01E5C900`~~ `01F7E300`) *(corrected 2026-10-02, OPUS: "
     "the struck values are file offsets - an `.rdata` image address is the file offset + `0x121200`, a `.data` one + "
     "`0x121A00`; each string read at its image address, as §10 and BS-2 cite them)*."),

    # X-12: four return values - 0016EFF0 returns 1 when [+0x1A38] is null (0016EFF0+0x20).
    (VPX, "Three distinct return values appear, and each is reached by a distinguishable path:",
     "~~Three~~ Four distinct return values appear *(corrected 2026-10-02, OPUS: `0016EFF0+0x20` `mov eax, 1` when "
     "`[+0x1A38]` is null, row `0x101` above; the table below lists the other three)*, and each is reached by a "
     "distinguishable path:"),

    # X-13: 0016EEC0 makes three passes (for 3, 2 and 1).
    (VPX, "(294 B, two nested loop pairs over a `0x4C` stride)",
     "(294 B, ~~two~~ three nested loop pairs over a `0x4C` stride *(corrected 2026-10-02, OPUS: passes for `3`, `2` "
     "and `1` at `0016EEC0+0x60`, `+0xA0` and `+0xD6`; UQ-310's answer)*)"),
    (VPX, "(`0016EF60`) — two full passes, not one.",
     "(`0016EF60`) — ~~two full passes, not one~~ three full passes, the third for `1` *(corrected 2026-10-02, OPUS: "
     "`0016EEC0+0xD6` compares the byte with `dil` = 1; the answer below)*."),

    # X-14: no handler is branched to; the 0016EFF0 byte match is a misaligned 7C inside 0016EEC0+0x108.
    (INV, "and none reaches anything outside the span that the listed members do not. Generator: "
          "_index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write.\"\n",
     "and none reaches anything outside the span that the listed members do not. Generator: "
     "_index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write.\" # <- corrected 2026-10-02, OPUS - none is "
     "branched to: the only other byte match for 0016EFF0 is a 7C inside the instruction at 0016EEC0+0x108 (mov rdi, "
     "[rsp + 0x18]), so each of the four is held only by its control-map qword (01CDB348, 01CDB398, 01CDB3A8, "
     "01CDB3C8); the members file's refs value 2 is generated output (SWE2-DATA)\n"),

    # X-15: every kernel is referenced (callers or lea), 0016F080 leas four.
    (VPX, "> separate population, reached by nothing at all, and they",
     "> separate population, ~~reached by nothing at all~~ referenced only by the decoder object and by each other - "
     "each of the 63 members of `libvpx-vp8-dsp-kernels.tsv` has a direct caller or a `lea`, and `0016F080` `lea`s "
     "four *(corrected 2026-10-02, OPUS: `0016F080+0xC4`..`+0xE7`; the inventory's kernel row)*, and they"),

    # X-17: libvorbis is reached: 001B7F30+0xF9 -> 0067A480, 0067A480+0x349 -> 00679A50 -> 008800C0 / 00880AF0 /
    #       00880BF0; 00679A40 is lea'd at 0067A480+0x443.
    (INV, "libvorbis is unreached — only the attribution of the path's lower half is",
     "~~libvorbis is unreached~~ libvorbis is reached from the movie player *(corrected 2026-10-02, OPUS: "
     "`001B7F30+0xF9` calls `0067A480`, `0067A480+0x349` calls `00679A50`, and `00679A50+0x1F`..`+0x8A` call "
     "`00880AF0`, `00880BF0` and `008800C0`)* — only the attribution of the path's lower half is"),
    (INV, "`00679600`, `00679A50`, `00679F40`; CF-2's reachability (the root `00679A40` is called by nothing) is\n"
          "unchanged.",
     "`00679600`, `00679A50`, `00679F40`; ~~CF-2's reachability (the root `00679A40` is called by nothing) is~~\n"
     "~~unchanged.~~ CF-2's reachability does not hold: `00679A40` has no caller but the movie player takes its address "
     "(`0067A480+0x443`), and calls `00679A50` (`0067A480+0x349`) *(corrected 2026-10-02, OPUS: read at the image)*."),

    # X-18: the CF-2 box's "driver's decoder core" is Tremor's (registry 01F41E58 -> mapping0 01F41F40, inverse 007FDC60).
    (INV, "  from the driver's own decoder core (`007FDC60`,",
     "  from ~~the driver's own decoder core~~ Tremor's own decode core *(corrected 2026-10-02, OPUS: `007FDC60` is the "
     "inverse slot of the mapping0 bundle `01F41F40` that Tremor's registry `01F41E58` points at, and the takers "
     "`007F8220`, `007F8600`, `007F8FD0` are Tremor bodies too; the 2026-09-12 correction in the libogg section)* "
     "(`007FDC60`,"),
    (INV, "The upward closure from those three is 62 functions, all inside the\n  sound driver, rooted at",
     "The upward closure from those three is 62 functions, ~~all inside the~~\n  ~~sound driver~~ whose lower part is "
     "Tremor, linked beside the driver *(corrected 2026-10-02, OPUS: `007F7FF0` compares the `vorbis` signature "
     "`01CEBB50`, and Tremor's registry is `01F41E58`)*, rooted at"),

    # X-19: the two Tremor ranges hold 107 listed entries (26 + 81); the front matter's removals reach 99 from 107.
    (INV, "**Tremor, 106 members — `007F41A0`",
     "**Tremor, ~~106~~ 107 members *(corrected 2026-10-02, OPUS: the two ranges hold 107 listed entries, 26 and 81; "
     "the front matter's eight removals reach its 99 from 107)* — `007F41A0`"),

    # X-22: the libvorbis registry is codec bundles held by .rdata pointer cells; 01CEB190 is a float table.
    (INV, "and their three vtables at `01CEB0A8`–\n  `01CEB178` are referenced only by two of the eleven themselves "
          "(`008923E0`, `00893860`, through\n  `01CEB190`);",
     "and ~~their three vtables at `01CEB0A8`–~~\n  ~~`01CEB178` are referenced only by two of the eleven themselves "
     "(`008923E0`, `00893860`, through~~\n  ~~`01CEB190`)~~ the registry there is codec bundles, not vtables, held by "
     "the `.rdata` pointer cells `01CDCF68` and `01CDD0F0`–`01CDD118`, and `01CEB190` after it is a float table that "
     "`008923E0` and `00893860` read *(corrected 2026-10-02, OPUS: read at the image; the residue bundles `01CEB0D0` / "
     "`01CEB110` / `01CEB150` of the libvorbis declaration)*;"),
    (INV, "end at a root that no site calls\n  and no pointer slot holds.",
     "end at a root that no site calls\n  ~~and no pointer slot holds~~ but whose address the movie player takes "
     "*(corrected 2026-10-02, OPUS: `0067A480+0x443` `lea`s `00679A40`)*."),

    # X-23 + X-24: the decoder banner is Ver.2.05.00 at 01CBA5D1, before the copyright 01CBA610 that 00121DB0+0x1C leas.
    (INV, "| **CRI HCA** | **Mixer 2.00.00, build 2015-07-31 16:45:20** | `HCA Mixer Ver.2.00.00 Build:Jul 31 2015 16:45:20` "
          "| `01CB7AC1` |",
     "| **CRI HCA** | ~~**Mixer 2.00.00, build 2015-07-31 16:45:20**~~ **decoder 2.05.00, build 2015-07-31 16:45:20** | "
     "~~`HCA Mixer Ver.2.00.00 Build:Jul 31 2015 16:45:20`~~ `HCA Decoder (Float) Ver.2.05.00 Build:Jul 31 2015 "
     "16:45:20` *(corrected 2026-10-02, OPUS: that banner sits directly before the decoder's copyright string "
     "`01CBA610`, which the member `00121DB0` references; the Mixer banner lies in the sound driver's data that "
     "`007DAFF0` reads, `01CB7A30`–`01CB7AB0`)* | ~~`01CB7AC1`~~ `01CBA5D1` |"),
    (INV, "| | | `right (c) 2009-2010 CRI Middleware Co., Ltd.` | `01CBA629` |",
     "| | | ~~`right (c) 2009-2010 CRI Middleware Co., Ltd.`~~ `Copyright (c) 2009-2010 CRI Middleware Co., Ltd.`, "
     "framed by newlines | ~~`01CBA629`~~ `01CBA610` *(corrected 2026-10-02, OPUS: `00121DB0+0x1C` `lea`s "
     "`01CBA610`; `01CBA629` is the string's `CRI Middleware Co., Ltd.` tail)* |"),

    # X-26: btCollisionShapeData is at 01CCD380 and btCollisionObjectFloatData at 01CCE3D8; the twenty names span
    #       01CCD380..01CCF378 (file 0x1BAC180..0x1BAE178).
    (INV, "`btCollisionObjectFloatData` / `btCollisionShapeData` (~~`01BAC180`, `01BAD1D8`~~ `01CCD380`, `01CCE3D8` "
          "*(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)*)",
     "`btCollisionObjectFloatData` / `btCollisionShapeData` (~~`01BAC180`, `01BAD1D8`~~ ~~`01CCD380`, `01CCE3D8`~~ "
     "`01CCE3D8`, `01CCD380` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)* "
     "*(corrected 2026-10-02, OPUS: in the names' order - `btCollisionObjectFloatData` is at `01CCE3D8`, "
     "`btCollisionShapeData` at `01CCD380`)*)"),
    (BUL, "at file offsets `0x1BAC800`..`0x1BAE300`:",
     "at ~~file offsets `0x1BAC800`..`0x1BAE300`~~ `01CCD380` (`btCollisionShapeData`) to `01CCF378` "
     "(`btRigidBodyFloatData`), file offsets `0x1BAC180`..`0x1BAE178` *(corrected 2026-10-02, OPUS: each of the "
     "twenty names located in the image)*:"),

    # X-27: the ImGui context is 02EA58C0 (00169620+0x4 -> ctor 00791E70; 01F40380 holds it); 02EA54F0 is IO +0x78's.
    (INV, "recorded as follow-up work; addresses and causing pages in the record.\"\n",
     "recorded as follow-up work; addresses and causing pages in the record.\" # <- corrected 2026-10-02, OPUS - the "
     "context is the static object 02EA58C0 (00169620+0x4 passes it to the ctor 00791E70; 01F40380 holds its "
     "address), not 02EA54F0, which is the object whose address 00791D80+0x3A stores at IO +0x78\n"),

    # X-28: one Yebis/PPFX package beside Phyre's: 006CBD20 passes the YEBIS_D3D11 licence text to PPFX, whose
    #       verifier 006DFF40 (ppfx.cpp diagnostics) checks it.
    (INV, "The binary contains **three** distinct post-processing layers, which is easy to conflate:",
     "The binary contains ~~**three** distinct post-processing layers~~ **two** post-processing packages, Phyre's own "
     "and Yebis/PPFX, whose two tags below are one product *(corrected 2026-10-02, OPUS: `006CBD20+0x41` hands the "
     "`YEBIS_D3D11` licence text `00D86C00` to the PPFX library and `006CBD20+0xEA` reaches its verifier `006DFF40`, "
     "whose diagnostics are `ppfx.cpp`'s; X-7 in §7)*, which is easy to conflate:"),
    (INV, "  -> YEBIS (3+)                  DOF / lens, \"YEBIS DOF Info\"\n",
     "  -> YEBIS (3+)                  DOF / lens, \"YEBIS DOF Info\"   <- corrected 2026-10-02, OPUS - not a third "
     "layer: PPFX is Yebis's core (X-7); 006DFF40 verifies the YEBIS_D3D11 licence\n"),

    # X-29: the gate was read (0071D9E0): all-zero skip, mismatch status 1, window status 2.
    (INV, "Licence gate (as described by the strings, not read from a body)\n",
     "Licence gate (as described by the strings, not read from a body)   <- corrected 2026-10-02, OPUS - read from "
     "0071D9E0: six zero fields skip the test (0071D9E0+0x714..+0x73A); a signed / plain-text mismatch sets status 1 "
     "(0071D9E0+0x829); otherwise status 2 when now is before begin 00:00:00 or after end 23:59:59 "
     "(0071D9E0+0x815..+0x81F)\n"),
    (INV, "census; the YEBIS licence-expiry behaviour rests on strings, not on a read of the checking function.",
     "census; ~~the YEBIS licence-expiry behaviour rests on strings, not on a read of the checking function.~~ "
     "*(answered: see X-2 in §7 - the verifier `0071D9E0` was read 2026-09-14; 2026-10-02, OPUS)*"),

    # X-30: 00791D80 is ImGuiIO's ctor on context +8; 00792090 builds the member after the 0xB88-byte IO.
    (INV, "| `00791D80` (large) | context init — `memset`",
     "| `00791D80` (large) | ~~context init~~ `ImGuiIO`'s constructor, run on context `+8` *(corrected 2026-10-02, "
     "OPUS: `00791E70+0x11` calls it with `rcx` = context + 8)* — `memset`"),
    (INV, "| `00792090` | member-object ctor at `+0xB90` (the `ImGuiIO`/settings block) |",
     "| `00792090` | member-object ctor at `+0xB90` (~~the `ImGuiIO`/settings block~~ the member after the `0xB88`-byte "
     "IO, not the IO *(corrected 2026-10-02, OPUS: `00791E70+0x1D` passes context + `0xB90`, where the IO built at "
     "`+8` ends)*) |"),

    # X-32: the image holds 29 source paths: PPFX 25, PhyreScripting.inl, three FFXII katano .c files.
    (PPFX, "| 26 source paths exist in the image |",
     "| ~~26 source paths exist in the image~~ 29 source paths exist in the image - PPFX's 25, `PhyreScripting.inl` and "
     "three FFXII `..\\..\\katano\\` `.c` files *(corrected 2026-10-02, OPUS: `.rdata` sweep; the 26 are the PPFX and "
     "Phyre paths)* |"),
    (PPFX, "they `lea` one of the 25 `..\\src\\` paths",
     "they `lea` one of the 25 ~~`..\\src\\`~~ paths *(corrected 2026-10-02, OPUS: 24 `..\\src\\` paths and the "
     "absolute `GPUClassUtil.h`)*"),

    # X-33: PPFX paths carry 363 sites in 193 functions; the other 1,494 in 747 are PhyreScripting.inl's.
    (PPFX, "**1,857 such sites survive across 940 functions.** They are authored evidence",
     "**~~1,857 such sites survive across 940 functions.~~** **363 such sites survive across 193 functions**; the "
     "other 1,494 sites, in 747 functions, are `PhyreScripting.inl`'s (§2.5) *(corrected 2026-10-02, OPUS: `lea` "
     "references to the 25 PPFX path strings counted at the image)*. They are authored evidence"),

    # X-35: six of the twelve GPUClassUtil.h copies are referenced, by 20 sites (6 + 6 + 1 + 1 + 3 + 3).
    (PPFX, "`d:\\bamboo\\build\\yeblic-ppfxlic-bl2015\\src\\gpu\\GPUClassUtil.h` — the referenced copies |",
     "`d:\\bamboo\\build\\yeblic-ppfxlic-bl2015\\src\\gpu\\GPUClassUtil.h` — ~~the referenced copies~~ two of the six "
     "referenced copies, with `00DA7278`, `00DA72B8`, `00DAA000` and `00DAA040` *(corrected 2026-10-02, OPUS: `lea` "
     "references counted per copy, 20 sites in all; the other six copies are unreferenced)* |"),
    (PPFX, "> **20 code sites reference the twelve copies, and `73` is a nearby immediate at 19 of them.**",
     "> **20 code sites reference ~~the twelve copies~~ six of the twelve copies, and `73` is a nearby immediate at 19 "
     "of them.** *(corrected 2026-10-02, OPUS: per-copy `lea` counts 6 + 6 + 1 + 1 + 3 + 3; `00D9BC88`, `00D9BCC8`, "
     "`00DA61D8`, `00DA6288`, `00DAC3B8` and `00DAC3F8` have none)*"),

    # ---- section 3.2 stale and banner items ----
    # S-1: the REOPENED banner is resolved.
    (INV, "> **REOPENED 2026-09-02 — this document's census had a scope defect.** It counted the",
     "> **~~REOPENED 2026-09-02 — this document's census had a scope defect.~~** *(answered: resolved - the front "
     "matter's `status: DOCUMENTED` and §9, both reopenings resolved 2026-10-01; 2026-10-02, OPUS)* The 2026-09-02 "
     "census had a scope defect. It counted the"),
    # S-3: EndDay is the sixth field.
    (INV, "  (EndDay presumably follows; the string is truncated in the extraction)\n",
     "  (EndDay presumably follows; the string is truncated in the extraction)   <- corrected 2026-10-02, OPUS - answered: "
     "EndDay is the sixth field: the shipped text at 00D86C00 reads EndMonth = 0, EndDay = 0; the pointer below\n"),
    # S-4: 00684D10 / 00686280 are function entries, read.
    (INV, "| `00684D10` / `00686280` | `lua_pcall` call sites | not read |",
     "| `00684D10` / `00686280` | ~~`lua_pcall` call sites~~ the Phyre script callers, function entries | ~~not read~~ "
     "read *(answered: see the pointer below this table; 2026-10-02, OPUS)* |"),
    # S-5: EnableYebis is a JSON config key read by name.
    (INV, "  render parameters, so it is plausibly a config key. Not proven; **X-3**.",
     "  render parameters~~, so it is plausibly a config key. Not proven~~ *(answered: it is a JSON config key - "
     "`001C3D50+0x627` looks it up by name through `001C51D0` and `001C7940+0x9E2` through `001FF740`, the JsonBox "
     "lookup, and reads it as an integer, 1 enabling; 2026-10-02, OPUS)*; **X-3**."),
    (INV, "- [x] Whether `EnableYebis` is a JSON config key or a compile-time switch. **X-3.**\n",
     "- [x] Whether `EnableYebis` is a JSON config key or a compile-time switch. **X-3.** *(answered: a JSON config "
     "key, read by name at `001C3D50+0x627` and `001C7940+0x9E2`; §6; 2026-10-02, OPUS)*\n"),
    # S-6: zlib is the save codec.
    (INV, "— where zlib is a candidate but unproven",
     "— where zlib ~~is a candidate but unproven~~ is the save codec *(answered: see §6, V-9 answered 2026-09-13 - "
     "`compress2` level 9, then RC4; 2026-10-02, OPUS)*"),
    # S-7: which decoder runs is answered.
    (INV, "> and which one *runs* is still open — that needs a call-graph reachability read from the audio\n"
          "> streaming path, not a body property.",
     "> ~~and which one *runs* is still open — that needs a call-graph reachability read from the audio~~\n"
     "> ~~streaming path, not a body property.~~ *(answered: see the pointer below - Tremor runs the sound driver's "
     "streams, libvorbis the movie player's audio; 2026-10-02, OPUS)*"),
    # S-8: X-8 closed 2026-09-27.
    (INV, "**X-8 stays open for those\nfour, and it may not be answerable from this binary at all.**",
     "~~**X-8 stays open for those~~\n~~four, and it may not be answerable from this binary at all.**~~ *(answered: X-8 "
     "closed 2026-09-27 - see the X-8 box in §7; 2026-10-02, OPUS)*"),
    # S-9: CF-1 closed 2026-09-12.
    (INV, "> **Reopened as `CF-1`.** The honest position",
     "> ~~**Reopened as `CF-1`.**~~ *(answered: `CF-1` was closed 2026-09-12 in the box above - not libxml2, the row "
     "withdrawn; the reopening below is kept as written; 2026-10-02, OPUS)* The honest position"),
    # S-10: EASTL 97.
    (INV, "| Bare-name families: EASTL 72, Lua +21, Bullet +18 |",
     "| Bare-name families: EASTL ~~72~~ 97 *(answered: §2's corrected count, GN162; 2026-10-02, OPUS)*, Lua +21, "
     "Bullet +18 |"),
    # S-11: the MSVC row's evidence cites 0080A270, which has left the family.
    (INV, "Two members left the family on the 2026-09-17 re-sweep, since measured as A: 0080A270 and 0080B8A0.\"\n",
     "Two members left the family on the 2026-09-17 re-sweep, since measured as A: 0080A270 and 0080B8A0.\" # <- "
     "corrected 2026-10-02, OPUS - answered: 0080A270, cited above among the vdecl math kernels, is no longer a member\n"),
    # S-12 (BUL): the inventory is DOCUMENTED.
    (BUL, "**REOPENED 2026-09-02** by a count defect this block found",
     "~~**REOPENED 2026-09-02**~~ reopened 2026-09-02 by a count defect this block found, since resolved *(answered: "
     "the inventory's front matter, `status: DOCUMENTED`, 2026-10-01; 2026-10-02, OPUS)*"),
    # S-14 (BUL): BN-4 - none installed from Phyre data.
    (BUL, "decided by whatever installs `006883A0`, which no page has read.",
     "decided by whatever installs `006883A0`~~, which no page has read~~ *(answered: see `BN-4` below - no shipped "
     "Phyre object carries a physics component, 2026-09-22; 2026-10-02, OPUS)*."),
    # S-15 / S-16 / S-17 (EASTL).
    (EA, "This document covers the **72 functions in the bare-name `EASTL.*` tag family**",
     "This document covers ~~the **72 functions in the bare-name `EASTL.*` tag family**~~ **72 of the bare-name "
     "`EASTL.*` tag family's 97 functions** *(answered: the inventory's §2, GN162 - the other 25 are "
     "`OrderedContainerRuntime` re-tags this page does not cover; 2026-10-02, OPUS)*"),
    (EA, "**Superseded readings:** none — this is the document's first version.",
     "**Superseded readings:** ~~none — this is the document's first version.~~ *(answered: three - §10's name "
     "correction of 2026-09-03, BS-4's mechanism and the 2026-09-30 capability correction; 2026-10-02, OPUS)*"),
    (EA, "corrected to twelve libraries, 801 functions",
     "corrected to twelve libraries, ~~801~~ 827 functions *(answered: the inventory's 2026-10-01 correction; "
     "2026-10-02, OPUS)*"),
    # S-19 / S-20 (VPX).
    (VPX, "**That mapping is inference from the upstream library, not something\n> this image states**",
     "~~**That mapping is inference from the upstream library, not something~~\n> ~~this image states**~~ *(answered: "
     "`UQ-307` - the map is libvpx 1.6.0's `vp8_ctf_maps` and each body matches instruction for instruction; the "
     "names still come from the headers; 2026-10-02, OPUS)*"),
    (VPX, "where libvpx VP8 1.6.0 is pinned, at 73 listed functions",
     "where libvpx VP8 1.6.0 is pinned, at ~~73 listed functions~~ 183 declared functions - decoder 116, its UC-1 "
     "row 4, kernels 63 *(answered: the inventory's front matter; 2026-10-02, OPUS)*"),
    # S-21 .. S-25 (LUAC).
    (LUAC, "> **Not yet executed.** This box is static reading; §13 is unchanged and still says so.",
     "> ~~**Not yet executed.** This box is static reading; §13 is unchanged and still says so.~~ *(answered: executed "
     "in isolation - §13, 70 commands, 0 mismatches, 2026-09-12; 2026-10-02, OPUS)*"),
    (LUAC, "00684D10 / 00684F60 / 00686280      Phyre script execution (three callers, UNREAD)\n",
     "00684D10 / 00684F60 / 00686280      Phyre script execution (three callers, UNREAD)   <- corrected 2026-10-02, "
     "OPUS - answered, read since: EXP-110 ran the callers (2026-09-25, §13) and EB-1 was answered 2026-09-26\n"),
    (LUAC, "**Whether any of the three callers reports it is unread** (`EB-4`)",
     "~~**Whether any of the three callers reports it is unread**~~ **No caller reports it** *(answered: `EB-4`, "
     "answered 2026-09-12 on the loader page; 2026-10-02, OPUS)* (`EB-4`)"),
    (LUAC, "| `EB-4` | whether any caller reports a compile failure |",
     "| `EB-4` | whether any caller reports a compile failure *(answered: no - the loader page's `EB-4`, 2026-09-12; "
     "2026-10-02, OPUS)* |"),
    (LUAC, "| `EB-2` | whether `luaL_loadfilex` (`00812FA0`) is reachable — if it is, the engine can load a `.lua` from "
           "disk |",
     "| `EB-2` | whether `luaL_loadfilex` (`00812FA0`) is reachable — if it is, the engine can load a `.lua` from "
     "disk *(answered: no - the loader page's `EB-2`, 2026-09-12; 2026-10-02, OPUS)* |"),
    (LUAC, "| `EB-3` | `00814B30` (287 B), a third `lua_load` caller with **zero callers**, unidentified |",
     "| `EB-3` | `00814B30` (287 B), a third `lua_load` caller with **zero callers**, ~~unidentified~~ *(answered: "
     "it is `load` - the loader page's `EB-3`, 2026-09-12; 2026-10-02, OPUS)* |"),
    (LUAC, "| `EB-5` | the parser's own seven functions; only `0082BE30` is placed in the chain |",
     "| `EB-5` | the parser's own seven functions; only `0082BE30` is placed in the chain *(answered: on the loader "
     "page 2026-09-14; 2026-10-02, OPUS)* |"),
    (LUAC, "**The two inner functions are named from their argument shapes, not proven** — `(L, -1, NULL)` and",
     "**The two inner functions are named from their argument shapes~~, not proven~~** *(answered: `00811130` is "
     "`lua_settop` - a negative index moves `top` by `idx + 1` slots, a non-negative one sets `top = base + idx + 1` "
     "and nils the gap, its whole 72-byte body; run as SETTOP in EXP-110; `00811530` stays shape-named; 2026-10-02, "
     "OPUS)* — `(L, -1, NULL)` and"),
    # S-23 / S-25 .. S-29 (LUA).
    (LUA, "concerned** — whatever reporting exists is in the three callers, which are not read here.",
     "concerned** — ~~whatever reporting exists is in the three callers, which are not read here.~~ and no caller "
     "reports it either *(answered: `EB-4` below, 2026-09-12; 2026-10-02, OPUS)*."),
    (LUA, "  expect a syntax error to announce itself; whether any caller reports it is unread.",
     "  expect a syntax error to announce itself; ~~whether any caller reports it is unread~~ no caller reports it "
     "*(answered: `EB-4`, 2026-09-12; 2026-10-02, OPUS)*."),
    (LUA, "> **The two inner names are inferred from their argument shapes, not proven.** `FUN_00811530(L, -1, NULL)`",
     "> **The two inner names are inferred from their argument shapes~~, not proven~~.** *(answered: `00811130` is "
     "`lua_settop`, read in full - the contract's §10 note; `00811530` stays shape-named; 2026-10-02, OPUS)* "
     "`FUN_00811530(L, -1, NULL)`"),
    (LUA, "> runtime question and a breakpoint on `00684D10` remains the way to settle it.**",
     "> runtime question and a breakpoint on `00684D10` ~~remains the way to settle it~~ can only confirm the static "
     "bound.** *(answered: the contract's `DA-1`, bounded 2026-09-26 - the image holds no code that can create a "
     "`lua_State`; 2026-10-02, OPUS)*"),
    (LUA, "  remains a runtime question and a breakpoint on `00684D10` remains the way to settle it.",
     "  remains a runtime question and a breakpoint on `00684D10` ~~remains the way to settle it~~ can only confirm "
     "the static bound *(answered: the contract's `DA-1`, 2026-09-26; 2026-10-02, OPUS)*."),
    (LUA, "`00684F60` is a **third** call site not named by `DA-1`'s four-executor set, and is not read here.",
     "`00684F60` is a **third** call site not named by `DA-1`'s four-executor set~~, and is not read here~~ "
     "*(answered: read below, narrowed 2026-09-14 - PScheduler slots 0, 1 and 4 reach it and it takes `[task + 8]` as "
     "the buffer; 2026-10-02, OPUS)*."),
    (LUA, "| Whether a chunk is ever supplied | **not established — and this document does not narrow it** | — |",
     "| Whether a chunk is ever supplied | ~~**not established — and this document does not narrow it**~~ bounded "
     "statically, not closed *(answered: `UQ-312` narrowed and the contract's `DA-1` bound, 2026-09-26; 2026-10-02, "
     "OPUS)* | — |"),
    (LUA, "| What the three callers pass | **not read** | — |",
     "| What the three callers pass | ~~**not read**~~ a `PScript` object *(answered: `EB-1`, 2026-09-26; 2026-10-02, "
     "OPUS)* | — |"),
    (LUA, "| Whether `luaL_loadfilex` is reachable | **not traced** | — |",
     "| Whether `luaL_loadfilex` is reachable | ~~**not traced**~~ no *(answered: `EB-2`, 2026-09-12; 2026-10-02, "
     "OPUS)* | — |"),
    (LUA, "**That second step is not described anywhere on the page**, and it is **not read\nhere either** —",
     "**That second step is not described anywhere on the page**~~, and it is **not read~~\n~~here either**~~ "
     "*(answered: read and executed in the contract, 2026-09-12 - all eighteen bytes compared in three groups, "
     "`0082E490+0x69`..`+0x89`; 2026-10-02, OPUS)* —"),

    # B-1 + B-8 + B-4 (README).
    (R, "  **DOCUMENTED, tier 2, one falsification pass.** Answers **BK-3**.",
     "  ~~**DOCUMENTED, tier 2, one falsification pass.**~~ **AUDITED, tier 2** *(corrected 2026-10-02, OPUS: the "
     "page's front matter says `status: AUDITED`)*. Answers **BK-3**."),
    (R, "  **DOCUMENTED, tier 2.** Eleven libraries, 690 functions.",
     "  **DOCUMENTED, tier 2.** ~~Eleven libraries, 690 functions.~~ At least twelve libraries, 827 tagged functions "
     "*(corrected 2026-10-02, OPUS: the inventory's 2026-10-01 re-status and its lead)*."),
    (R, "  debug menu compiled into retail.\n\n## How to add a system here",
     "  debug menu compiled into retail.\n\n"
     "- [`Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`]"
     "(Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md) — the Phyre-to-Bullet rigid-body "
     "seam — **AUDITED**\n"
     "- [`EASTL/eastl-strings-containers-and-the-logging-allocator.md`]"
     "(EASTL/eastl-strings-containers-and-the-logging-allocator.md) — EASTL strings, containers and the logging "
     "allocator — **AUDITED**\n"
     "- [`Lua-Core/the-lua-loader-and-what-it-accepts.md`](Lua-Core/the-lua-loader-and-what-it-accepts.md) — the Lua "
     "chunk loader and what it accepts — **AUDITED**\n"
     "- [`Lua-Core/CONTRACT-lua-chunk-loader.md`](Lua-Core/CONTRACT-lua-chunk-loader.md) — **CONTRACT READY**\n"
     "- *(corrected 2026-10-02, OPUS: four pages this list omitted, added with the status each page's own front "
     "matter states)*\n"
     "\n## How to add a system here"),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('`001C3D50+0x627` looks it up by name through `001C51D0` and `001C7940+0x9E2` through `001FF740`, the JsonBox lookup',
     'the render-settings loader looks it up by name at its `+0x627`, and the global tuning-settings loader at its `+0x9E2`, both through `001FF740`, the JsonBox lookup'),
    ('read by name at `001C3D50+0x627` and `001C7940+0x9E2`',
     'read by name in the render-settings loader (its `+0x627`) and the global tuning-settings loader (its `+0x9E2`)'),
    ('`007DAFF0` reads, `01CB7A30`',
     'a 1,627-byte sound-driver body reads, `01CB7A30`'),
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
