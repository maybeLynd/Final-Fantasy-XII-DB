"""apply_22phyre.py [--apply] - 22-Middleware-PhyreEngine readiness map (cloud-reports/re-readiness/22-phyre.md),
section 3.1 value items C-V1-C-V101 and the section 3.2 stale / banner items, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the side the shipping image REFUTES (or, for C-V1/C-V2/C-V3/C-V38/C-V57/C-V58, the side the
generated census and ledger refute) and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*, or answers a stale
"not read / open" line, tagged *(answered: see ...; 2026-10-02, OPUS)*. Verdicts and deciding instructions:
scratchpad ph22/verdicts-22.md.
Items with no edit: C-V4 (counting rule), C-V12 / C-V39 / C-V50-C-V53 / C-V68 / C-V72 / C-V75 / C-V85 (census or
count drift, not an image value), C-V32 / C-V47 / C-V59 / C-V65 / C-V66 / C-V78 / C-V82 / C-V84 / C-V92 / C-V97
(both sides right), C-V74 / C-V100 (undecidable statically); stale C-S5, C-S7, C-S9, C-S15, C-S24, C-S26, C-S44,
C-S45, C-S51-C-S54 (already annotated on the page, or no favoured side, or front-matter dates).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment in the block's comment syntax instead of a strike (their OLD
includes the line end, so NEW never contains OLD). Front-matter rows get a trailing YAML `# <- corrected` comment.
No heading changes. X1 is the map's outside-knowledge note (SetPriorityClass 0x8000).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "22-Middleware-PhyreEngine/"
R = F + "README.md"
CAM = F + "the-camera-state-snapshot.md"
MAP = F + "Subsystem-Map/phyre-subsystem-map.md"
MOD = F + "Subsystem-Map/the-fifteen-modules-registered-before-main.md"
APP = F + "Application-Framework-Boundary/the-game-is-a-phyre-application.md"
HDR = F + "Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md"
CHDR = F + "Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md"
NS = F + "Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md"
CNS = F + "Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md"
CDMS = F + "Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md"
CCD = F + "Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md"
MR = F + "Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md"
AR = F + "Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md"
IS = F + "Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md"
LUA = F + "Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md"
ACC = F + "Script-Object-Accessors/phyre-script-object-accessors.md"
PPF = F + "Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md"
PFX = F + "Post-Process-Chain/the-phyre-post-effect-class-family.md"
CTX = F + "Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md"
FRM = F + "The-Frame/what-happens-between-two-frames.md"
ANI = F + "Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md"

C = "*(corrected 2026-10-02, OPUS: "
K = "<- corrected 2026-10-02, OPUS - "
THREADS = ("thirteen creation sites - the five `CreateThread` and four `_beginthreadex` call sites plus the four calls "
           "of the engine's thread API `008636E0` (`0035E920`, `00368D41`, `00368E97`, `00369000`) - start ten bodies: "
           "`005CCAB0`, `005CCBA0`, `007DEC40`, `007DD950`, `00171370`, `007A5550` (three `_beginthreadex` sites), and "
           "through the trampoline `00863500` (`0086348B`) `0035EA40`, `00368C10`, `00369100`, `00368AE0`")

EDITS = [
    # C-V1: 6,769 - the class map members/phyre-function-class-map.tsv has 6,769 rows; the 6,768 is the GN161 snapshot
    #     (Tools/work/graph_gn/functions.tsv); today's ledger Tools/work/graph/functions.tsv tags 6,771.
    (R, "| Functions | 6,768 |",
     "| Functions | ~~6,768~~ 6,769 " + C + "the per-function class map `Subsystem-Map/members/phyre-function-class-map.tsv` "
     "has 6,769 rows; 6,768 is the GN161 snapshot, before `00180A70` was classified; the ledger "
     "`Tools/work/graph/functions.tsv` tags 6,771 today, `005A7BF0` and `0067F9D0` added after the map)* |"),
    # C-V2: Rendering 288 (the ledger's CodeDomain.Phyre.Rendering count; 287 is GN161).
    (R, "Middleware 347 · Rendering 287 · PostProcessing",
     "Middleware 347 · Rendering ~~287~~ 288 " + C + "the ledger tags 288 `CodeDomain.Phyre.Rendering` functions, "
     "`00180A70` included; 287 is the GN161 count)* · PostProcessing"),
    (MAP, "| `Rendering` | 54 | 287 | 18.8 % |",
     "| `Rendering` | 54 | ~~287~~ 288 " + C + "the 2026-09-14 count above, `00180A70` included)* | 18.8 % |"),

    # C-V3: 2,248 RTTI classes (rtti_recover.py over the image, Tools/work/rtti/classes.tsv) of which 1,739 Phyre;
    #     an independent complete-object-locator walk of .rdata finds 1,739 Phyre classes with a locator.
    (MAP, "`rtti_recover.py` recovered **2,133 classes** image-wide, of which **1,604 are `Phyre::`**, carrying",
     "`rtti_recover.py` recovered ~~**2,133 classes**~~ **2,248 classes** image-wide, of which ~~**1,604 are "
     "`Phyre::`**~~ **1,739 are `Phyre::`** " + C + "`Tools/work/rtti/classes.tsv` has 2,248 rows today and 1,739 "
     "`Phyre::` names; an independent walk of the image's complete-object locators finds the same 1,739 `Phyre::` "
     "classes; the 2,133 run failed to demangle most names, class-descriptor-and-metadata-system.md §14; the "
     "namespace table below is that older run's)*, carrying"),
    (MAP, "| `Tools/work/rtti/classes.tsv` | 2,133 classes: name, mangled, vtable count, method count |",
     "| `Tools/work/rtti/classes.tsv` | ~~2,133 classes~~ 2,248 classes " + C + "the table's current row count)*: "
     "name, mangled, vtable count, method count |"),
    (CDMS, "| 2,134 RTTI classes | independent MSVC RTTI walk",
     "| ~~2,134 RTTI classes~~ 2,248 RTTI classes " + C + "superseded by §14, as §2 already says; `classes.tsv` "
     "has 2,248 rows)* | independent MSVC RTTI walk"),

    # C-V5: the slot-4 tick 0017CCD0 returns 0 (0017CD89 / 0017CDA9 -> 005C5230 xor eax,eax) or 9 (0017CDB2);
    #     0017D6E0 itself returns 0022A580's eax: 1 at 0022A594, else the mode body's.
    (APP, "                       -> FUN_0017D6E0(frameTime, mode) -> 0 / 1 / 9\n",
     "                       -> FUN_0017D6E0(frameTime, mode) -> 0 / 1 / 9   " + K + "the tick returns 0 (0017CD89, "
     "0017CDA9 -> 005C5230) or 9 (0017CDB2); 0017D6E0 returns 0022A580's eax, 1 at 0022A594 or the mode body's\n"),
    # C-V6: slot 28 0079C140 calls slot 7 ([rax+0x38] 0079C26B) before slot 4 ([rax+0x20] 0079C2D6); no slot 6 call.
    (APP, "             slot 4  GameApplication : FRAME TICK\n",
     "             slot 4  GameApplication : FRAME TICK   " + K + "order is slot 7 (0079C26B) then slot 4 "
     "(0079C2D6), then slot 9 (0079C526), the viewports (0079C5FE) and slot 8 (0079C655), once per call of slot 28 "
     "0079C140; 0079C140 makes no slot 6 call\n"),
    # C-V7: 008C5760 slots 22 / 25 hold 0017D170 / 0017D1E0; PApplication 01CB2508 holds 0016D6A0 in both.
    (APP, "**The 145 CFG guard adapters.** Slot 22 and 25 inherit `0016D6A0`, which is the CFG check",
     "**The 145 CFG guard adapters.** ~~Slot 22 and 25 inherit `0016D6A0`~~ `PApplication`'s slots 22 and 25 hold "
     "`0016D6A0`, and the game overrides both " + C + "`008C5760` slot 22 = `0017D170`, slot 25 = `0017D1E0`, against "
     "`0016D6A0` at `01CB2508` - the slot table above)*, which is the CFG check"),
    # X1: SetPriorityClass immediate 0x8000 (00792F80 mov edx, 0x8000) is ABOVE_NORMAL_PRIORITY_CLASS.
    (APP, "applies `SetPriorityClass` with `0x8000` (HIGH_PRIORITY_CLASS),",
     "applies `SetPriorityClass` with `0x8000` (~~HIGH_PRIORITY_CLASS~~ `ABOVE_NORMAL_PRIORITY_CLASS` " + C +
     "`00792F80 mov edx, 0x8000` before the call at `00792F85`; the Windows SDK defines `0x8000` as "
     "`ABOVE_NORMAL_PRIORITY_CLASS`, `HIGH_PRIORITY_CLASS` is `0x80`)*),"),
    # C-S10 / C-S11 / C-S12: answered on the page.
    (APP, "  **Still open for slots 10, 15 and 16:** neither",
     "  **Still open for slots 10, 15 and 16:** *(answered: see PA-1, ANSWERED 2026-09-27 - nothing in this build "
     "dispatches slots 10, 15, 16, 22, 23 or 24; 2026-10-02, OPUS)* neither"),
    (APP, "Slots 1, 12, 13, 17–20, 29 and\n  30 are not read.",
     "Slots 1, 12, 13, 17–20, 29 and\n  30 ~~are not read~~ *(answered: see the ANSWERED 2026-09-26 block below - "
     "every inherited slot now has a behaviour; 2026-10-02, OPUS)*."),
    (APP, "**the caller is inside PhyreEngine and\nwas not read**.",
     "**the caller is inside PhyreEngine and\nwas not read** *(answered: see PA-5 - the framework's per-frame "
     "update, inherited slot 28 `0079C140`, calls slot 4 at `0079C2D6`; 2026-10-02, OPUS)*."),

    # C-V8: 005A0840 is also called directly from 007980A0 (007986D5, 00798886); the guard 02CACCA0 (005A0844 test,
    #     005A08C5 clear) makes the first call do the work.
    (MOD, "`call 00808B90`) — so the shutdown walk runs at process exit, not from game code.",
     "`call 00808B90`) — ~~so the shutdown walk runs at process exit, not from game code.~~ and the start-up "
     "function also calls it directly " + C + "`007980A0` calls `005A0840` at `007986D5` and `00798886`; the guard "
     "byte `02CACCA0`, tested at `005A0844` and cleared at `005A08C5`, makes the first call do the walk and the "
     "`atexit` one a no-op - as the-game-is-a-phyre-application.md's shutdown sequence says)*."),
    # C-V9: 006388C0 returns a bool (sete al at 006389A1): 0x12 is internal, the duplicate returns false.
    (MOD, "(`0067F700`), returning `0x12` on a duplicate insert.",
     "(`0067F700`), ~~returning `0x12` on a duplicate insert.~~ returning a bool " + C + "`0x12` is only an "
     "internal code, `0063898A`; the result is `sete al` at `006389A1`, so a duplicate insert or an already-present "
     "name (`0063894A`) returns false and a fresh insert true)*."),
    # C-V10: the base-vtable column is the destructor column: 00167810 hands 008B6A40 to atexit (00167810+0x43 / 00167810+0x51);
    #     008B6A40 re-stamps the base vtable 00D26BC0 into 01F2EE60 (008B6A40+0x8 / 008B6A40+0xF) and unlinks.
    (MOD, "> vtable into the same objects.** Which is ctor-versus-base-ctor and which is ctor-versus-dtor is\n"
          "> **not** established, and the column is headed accordingly.",
     "> vtable into the same objects.** ~~Which is ctor-versus-base-ctor and which is ctor-versus-dtor is~~\n"
     "> ~~**not** established, and the column is headed accordingly.~~ The base-vtable column is the destructor "
     "column " + C + "the registrar `00167810` passes `008B6A40` to `atexit` (`00167810+0x43`, `00167810+0x51`), and "
     "`008B6A40` re-stamps the base vtable `00D26BC0` into `01F2EE60` (`008B6A40+0x8`, `008B6A40+0xF`) before unlinking; the "
     "answer block below)*."),
    (MOD, "| **Those fifteen are constructors, not destructors** | **not established** — the image's initial vtable",
     "| **Those fifteen are constructors, not destructors** | ~~**not established**~~ **refuted: they are the "
     "exit-time destructors** " + C + "`00167810+0x43`/`00167810+0x51` hand `008B6A40` to `atexit`; `008B6A40+0x8`/`008B6A40+0xF` "
     "re-stamp `00D26BC0`)* — the image's initial vtable"),
    # C-V11: 00617810 is real (00686C40 calls it at 00686C6C) and registers PShaderComputeProgramD3D11's members
    #     (descriptor 02CF1C40, 00632960 at 006178A2 ...); the PUtilityDynamicGeometry registrar is 00167810.
    (MOD, "(including `00617810`, the `PUtilityDynamicGeometry` registrar of the §2 table)",
     "(including `00617810`, ~~the `PUtilityDynamicGeometry` registrar of the §2 table~~ the member registration of "
     "`PShaderComputeProgramD3D11`, descriptor `02CF1C40` " + C + "called at `00686C6C`, it registers fields through "
     "`00632960` from `00617810` + 0x92; the `PUtilityDynamicGeometry` registrar is `00167810`, held by the CRT table at "
     "`008C44B0`, so this is not a digit slip)*)"),
    # C-V13: the 0xE0 object is at 01F7F5B8 (005A08FC mov ecx,0xE0; 005A0919 mov [01F7F5B8],rax); 01F3F5B8 has no refs.
    (MOD, "**Init allocates a `0xE0`-byte object at `01F3F5B8`**",
     "**Init allocates a `0xE0`-byte object at ~~`01F3F5B8`~~ `01F7F5B8`** " + C + "`005A08FC mov ecx, 0xE0`, "
     "`005A0919` stores the result to `01F7F5B8`; nothing references `01F3F5B8`)*"),
    # C-S8: 005A0CB0 read 2026-09-14 (the answer block).
    (MOD, "| `005A0CB0` | 100 B | slot `+0x00` of every module vtable — **body unread** |",
     "| `005A0CB0` | 100 B | slot `+0x00` of every module vtable — ~~**body unread**~~ *(answered: see the "
     "2026-09-14 answer block - the modules' shared scalar deleting destructor; 2026-10-02, OPUS)* |"),
    (MOD, "| `+0x00` | shared `005A0CB0` — **unread** |",
     "| `+0x00` | shared `005A0CB0` — ~~**unread**~~ the shared scalar deleting destructor *(answered: see the "
     "2026-09-14 answer block; 2026-10-02, OPUS)* |"),
    (MOD, "| `005A0CB0` | vtable slot 0, shared by all fifteen — body unread |",
     "| `005A0CB0` | vtable slot 0, shared by all fifteen — ~~body unread~~ *(answered: see the 2026-09-14 answer "
     "block; 2026-10-02, OPUS)* |"),
    (MOD, "| **Slot `+0x00`'s role** | **not established — `005A0CB0` unread** | — |",
     "| **Slot `+0x00`'s role** | ~~**not established — `005A0CB0` unread**~~ *(answered: see the 2026-09-14 "
     "answer block - destroy and unlink; 2026-10-02, OPUS)* | — |"),

    # C-V14: thirteen creation sites, ten thread bodies (007A5550 starts three; 0086348B starts the trampoline).
    (FRM, "image's **nine** thread procedures is a plausible consumer",
     "image's ~~**nine**~~ ten thread procedures " + C + THREADS + "; so the next line's \"no others\" is wrong too)* "
     "is a plausible consumer"),
    (FRM, "all nine thread\n      procedures in the image",
     "all ~~nine~~ ten thread " + C + "thirteen creation sites, ten bodies, see section 2.4)*\n      procedures in "
     "the image"),
    (FRM, "nine procedures, largest 555 B.",
     "~~nine procedures~~ ten bodies from these and the four below " + C + THREADS + ")*, largest 555 B."),
    (FRM, "so the claim stands on thirteen procedures, not nine (CG-3)",
     "so the claim stands on ~~thirteen procedures, not nine~~ thirteen creation sites and ten thread bodies " + C +
     "`007A5550` starts three of the `_beginthreadex` sites and `0086348B` starts the trampoline `00863500` that "
     "runs the four engine threads)* (CG-3)"),
    (FRM, "none of the image's nine thread procedures could consume",
     "none of the image's ~~nine~~ ten thread procedures " + C + "thirteen creation sites, section 2.4)* could "
     "consume"),
    # C-V15: 003A2090 ends `and dword ptr [rax], 0x8000` (003A20B0): an AND-mask, not an OR.
    (FRM, "`[r10] = rdx` link, `[head+8] = r8`, `or [head], 0x8000` flag — the queue push",
     "`[r10] = rdx` link, `[head+8] = r8`, ~~`or [head], 0x8000` flag~~ `and [head], 0x8000` " + C + "`003A20B0 and "
     "dword ptr [rax], 0x8000` keeps bit 15 and clears NLOOP, the begin-subpacket of section 2's table)* — the "
     "queue push"),
    # C-V16: the index global is 02EBEFF0 (003A1DB6, 003A1DCA).
    (FRM, "the flip is `eax = 1 - dword [02F8EFF0]` stored back",
     "the flip is `eax = 1 - dword ~~[02F8EFF0]~~ [02EBEFF0]` " + C + "`003A1DB6` reads and `003A1DCA` writes "
     "`02EBEFF0`)* stored back"),
    # C-V17: 47 direct call sites in 38 functions.
    (FRM, "              +-> (via 003A1DB0, from 38 call sites across the engine)\n",
     "              +-> (via 003A1DB0, from 38 call sites across the engine)   " + K + "47 direct call sites in 38 "
     "functions\n"),
    # C-V18: ten inline sites (the list in section 2.4), one of them 0022B2C0 inside MainLoop_Draw 0022B0B0.
    (FRM, "inlined spin at `0022BAD0` and its eight siblings exists",
     "inlined spin at `0022BAD0` and its ~~eight~~ nine siblings " + C + "ten inline copies: `0022A850`, `0022AE50`, "
     "`0022AFA0`, `0022B040`, `0022B2C0` (in `MainLoop_Draw`), `0022B720`, `0022B820`, `0022BAD0`, `0022BD20`, "
     "`00262AE0`)* exists"),
    (FRM, "displacement census locates nine more | 1 |",
     "displacement census locates ~~nine~~ eight more " + C + "ten inline copies in all, `02EBA3F8` reads at "
     "`0022A850`, `0022AE50`, `0022AFA0`, `0022B040`, `0022B2C0`, `0022B720`, `0022B820`, `0022BAD0`, `0022BD20`, "
     "`00262AE0`)* | 1 |"),
    # C-V19: mode 3 0022B8C0 calls World_UpdateSimulationTick at 0022BA23 (ecx = edx = 1).
    (FRM, "one in the menu — and mode 3 does not advance the world. The world tick is",
     "one in the menu — ~~and mode 3 does not advance the world~~ and mode 3 calls the world tick too " + C +
     "`0022B8C0` calls `00314020` at `0022BA23` with `ecx = edx = 1`; what those arguments do to the step is not "
     "read here)*. The world tick is"),
    # C-V20: the pass list omits the pre-flush gated calls and the bit-0 thunk 0036F440 (-> 00475390).
    (FRM, "  bit 8   command-buffer flush block (submit / wait / resume)\n",
     "  bit 8   command-buffer flush block (submit / wait / resume)   " + K + "before this the body also runs bits 7 "
     "and 5 -> 0036D400 (0022B20C-0022B238), bit 6 or 1 -> 00332420(3) (0022B23F-0022B258), bit 2 -> 00377230 "
     "(0022B25F), bit 0 -> 003769E0, 00377520, 0036F410 (0022B26F-0022B282), bit 6 or 1 -> 00332420(0) "
     "(0022B289-0022B29F); after post-processing bit 0 -> 0036F440, a jump to 00475390 (0022B57E-0022B587); the "
     "bit table below is the complete gate map\n"),
    # C-V21: AO also needs dword 01FD49E8 != 0; Water needs 01FD49E8 != 0; with 0017FE10() == 0 the draw calls
    #     00229F20(0017FE20() == 0) instead.
    (FRM, "                             \"AO render\"             <- only if 0017FE10() != 0\n",
     "                             \"AO render\"             <- only if 0017FE10() != 0   " + K + "and dword "
     "01FD49E8 != 0 (0022B3BD-0022B3C8); when 0017FE10() == 0 the draw calls 00229F20(0017FE20() == 0) at 0022B45D "
     "instead\n"),
    (FRM, "                             \"Water effect\"          <- only if 0017FE20() != 0\n",
     "                             \"Water effect\"          <- only if 0017FE20() != 0   " + K + "and dword "
     "01FD49E8 != 0 (0022B40E-0022B419); a second site at 0022B474 marks it when 01FD49E8 != 0, 0017FE20() == 0 "
     "and 0017FE10() != 0\n"),
    # C-V22: only mode 3 0022B8C0 passes 01E0C1D8 / 01E0C1DC (0022B957-0022B971, 0022B9E1-0022B9F7).
    (FRM, "The field frame calls it as `00184460(0, 0, *(u32*)0x01E0C1D8, *(u32*)0x01E0C1DC, 1)`",
     "The ~~field frame~~ full-menu frame `0022B8C0` " + C + "it loads `01E0C1D8`/`01E0C1DC` at `0022B957`-"
     "`0022B971` and `0022B9E1`-`0022B9F7`; the field path reaches `00184460` through `00249FD0`, which passes a "
     "record's four words, `0024A035`-`0024A04B`)* calls it as `00184460(0, 0, *(u32*)0x01E0C1D8, "
     "*(u32*)0x01E0C1DC, 1)`"),
    # C-S14 / C-S16: answered on the page.
    (FRM, "Where the commands are actually consumed is the largest thing this\ndocument does not know.",
     "Where the commands are actually consumed is the largest thing this\ndocument does not know *(answered: see "
     "the ANSWERED 2026-09-27 block - nothing in this executable reads a finished batch; 2026-10-02, OPUS)*."),
    (FRM, "                        frame path and was not found: PROPOSED-xiionline-13-1.\n",
     "                        frame path and was not found: PROPOSED-xiionline-13-1.   " + K + "answered "
     "2026-09-27, nothing in this executable reads a finished batch\n"),
    (FRM, "before the walk **and again per entry at `0037559F`–`003755B2`**, and",
     "before the walk **and again per entry at `0037559F`–`003755B2`** *(answered: see section 2.4 - the 17 waits "
     "on `02EAF6D8` are hoisted and cannot wait; 2026-10-02, OPUS)*, and"),

    # C-V23: the record is 0x90 bytes; the second block is +0x48..+0x87, 64 bytes (00865055 lea rcx,[rbx+0x48];
    #     008650EB movss [rcx+0x3c]; 0086510D movss [rbx+0x8c]).
    (CAM, "**It fills a 140-byte record from two sources and nothing else.**",
     "**It fills a ~~140-byte~~ 144-byte (`0x90`) record from two sources and nothing else.** " + C + "the last store "
     "is the dword at `+0x8C`, `0086510D`; the layout section below)*"),
    (CAM, "- **`+0x48 … +0x84`** — 60 bytes taken from a",
     "- **~~`+0x48 … +0x84`~~ `+0x48 … +0x87`** — ~~60 bytes~~ 64 bytes, a 4x4 float matrix " + C + "`00865055 lea "
     "rcx, [rbx+0x48]`, last store `008650EB movss [rcx+0x3c]`)*, taken from a"),
    # C-S13: SD-60 answered.
    (CAM, "What is still not claimed is what the two matrices and the two floats mean, `SD-60`.)*\n",
     "What is still not claimed is what the two matrices and the two floats mean, `SD-60`.)* *(answered: see the "
     "SD-60 answer block below, 2026-09-30; 2026-10-02, OPUS)*\n"),
    # C-S6: the in-body banner against the front matter.
    (MAP, "**PARTIAL, and tier 4 by construction.** This document",
     "~~**PARTIAL, and tier 4 by construction.**~~ **DOCUMENTED, tier 4 by construction.** " + C + "the front "
     "matter says `status: DOCUMENTED`)* This document"),
    (MAP, "No Phyre function body is read here. Its value",
     "No Phyre function body is read here *(answered: see the AQ-2 and AQ-5 answers, 2026-09-18, which decode "
     "bodies; 2026-10-02, OPUS)*. Its value"),

    # C-S1 / C-S2: index banners against each page's front matter (status: AUDITED).
    (R, "  **DOCUMENTED, tier 1, crossref-clean.** The category's second",
     "  ~~**DOCUMENTED, tier 1, crossref-clean.**~~ **AUDITED, tier 1, crossref-clean.** " + C + "the page's front "
     "matter says `status: AUDITED`)* The category's second"),
    (R, "  **DOCUMENTED, tier 1.** 4,557 functions",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* "
     "4,557 functions"),
    (R, "  **DOCUMENTED, tier 1, one falsification pass.** The category's framing",
     "  ~~**DOCUMENTED, tier 1, one falsification pass.**~~ **AUDITED, tier 1, one falsification pass.** " + C +
     "the page's front matter says `status: AUDITED`)* The category's framing"),
    (R, "  **DOCUMENTED, tier 1, one falsification pass.** The engine's own field list",
     "  ~~**DOCUMENTED, tier 1, one falsification pass.**~~ **AUDITED, tier 1, one falsification pass.** " + C +
     "the page's front matter says `status: AUDITED`)* The engine's own field list"),
    (R, "  **DOCUMENTED, tier 2.** **747 functions",
     "  ~~**DOCUMENTED, tier 2.**~~ **AUDITED, tier 2.** " + C + "the page's front matter says `status: AUDITED`)* "
     "**747 functions"),
    # C-S3: the index lists 8 of the 22 pages; the other 14 added with the status each front matter states.
    (R, "  the largest block of `UQ-289`, and joins the post-effect classes to the shader-variant key.\n\n"
        "**Composition of this category**",
     "  the largest block of `UQ-289`, and joins the post-effect classes to the shader-variant key.\n\n"
     "- [`Subsystem-Map/phyre-subsystem-map.md`](Subsystem-Map/phyre-subsystem-map.md) — **DOCUMENTED**\n"
     "- [`Subsystem-Map/the-fifteen-modules-registered-before-main.md`]"
     "(Subsystem-Map/the-fifteen-modules-registered-before-main.md) — **AUDITED**\n"
     "- [`the-camera-state-snapshot.md`](the-camera-state-snapshot.md) — **DOCUMENTED**\n"
     "- [`Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`]"
     "(Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md) — **AUDITED**\n"
     "- [`Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`](Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md)"
     " — **CONTRACT READY**\n"
     "- [`Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md`]"
     "(Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md) — **AUDITED**\n"
     "- [`Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md`]"
     "(Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md) — **CONTRACT READY**\n"
     "- [`Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`]"
     "(Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md) — **CONTRACT READY**\n"
     "- [`Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md`]"
     "(Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md) — **AUDITED**\n"
     "- [`Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md`]"
     "(Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md) — **DOCUMENTED**\n"
     "- [`Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`]"
     "(Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md) — **AUDITED**\n"
     "- [`Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`]"
     "(Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md) — **AUDITED**\n"
     "- [`Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`]"
     "(Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md) — **DOCUMENTED**\n"
     "- *(corrected 2026-10-02, OPUS: fourteen pages this list omitted, added with the status each page's own front "
     "matter states)*\n\n"
     "**Composition of this category**"),
    # C-S4: AQ-2 is SUPERSEDED (2026-09-26 / 2026-09-29), not PARTIAL.
    (R, "per-function placement, **AQ-2** (PARTIAL: 4,515 of the 6,769",
     "per-function placement, **AQ-2** (~~PARTIAL~~ SUPERSEDED as a population statement *(answered: see "
     "Subsystem-Map/phyre-subsystem-map.md, the AQ-2 box, 2026-09-29; 2026-10-02, OPUS)*: 4,515 of the 6,769"),

    # C-V24: nine fields - 00598DF0 calls 00632960 nine times (0059904A ... 00599216).
    (HDR, "| `00598DF0` | registers the 10 `PInstanceListHeader` fields",
     "| `00598DF0` | registers the ~~10~~ nine " + C + "nine `00632960` calls, `0059904A` to `00599216`; the "
     "same row's nine-element battery)* `PInstanceListHeader` fields"),
    # C-V29: three codes over nine causes (contract's return table).
    (HDR, "**Four rejections, three distinct codes: `6` refuse, `9` truncated, `0xD` allocation failed.** Zero",
     "~~**Four rejections, three distinct codes: `6` refuse, `9` truncated, `0xD` allocation failed.**~~ **Three "
     "distinct codes over nine rejection causes: `6` refuse, `9` truncated, `0xD` allocation failed.** " + C +
     "in `0059A3B0` code `9` leaves at `0059A3E2` (short header read) and `0059A57A` (short tail read), `0xD` at "
     "`0059A524` and `0059A51A`, and `6` for five causes - bad magic `0059A421`, platform or physics mismatch "
     "`0059A46C`, null namespace buffer or short-header size mismatch `0059A598`; CONTRACT-phyre-cluster-header.md's "
     "return table)* Zero"),
    # C-V30: both id leaves run whatever checkPlatform says (0059A440 call 00686D00, 0059A457 call 0069E780); only the
    #     compares are guarded (0059A44D / 0059A45C test dil).
    (HDR, "if (checkPlatform && hdr->m_platformID != GetPlatformID())        return 6;   /* 0x44583131 */\n",
     "if (checkPlatform && hdr->m_platformID != GetPlatformID())        return 6;   /* 0x44583131 */   // " + K +
     "both GetPlatformID (0059A440) and GetPhysicsEngineID (0059A457) are called whatever checkPlatform says; only "
     "the compares are guarded (0059A44D, 0059A45C)\n"),
    # C-V31: ten movups (five 16-byte load/store pairs) plus one dword, inline (0059A536-0059A55F).
    (HDR, "  copied in as 21 dwords, and",
     "  copied in ~~as 21 dwords~~ inline as ten `movups` (five 16-byte loads and stores) plus one dword " + C +
     "`0059A536`-`0059A55F`; 84 bytes, no `memcpy` call)*, and"),
    # C-V38: 2,091 meshes (members/user-fixup-census.tsv mesh rows sum to 2,091 of 35,984).
    (HDR, "6 meshes against 2,097 in the archive.",
     "6 meshes against ~~2,097~~ 2,091 " + C + "the mesh rows of `members/user-fixup-census.tsv` sum to 2,091 of "
     "35,984, CU-4)* in the archive."),
    # C-V35: "bit 4" is the 0x04 bit - 12 and 20 both carry 0x04; 12 lacks 0x10.
    (HDR, "class\" is a class whose namespace record carries **bit 4 of class word `w7`** — in this title",
     "class\" is a class whose namespace record carries **~~bit 4~~ the `0x04` bit of class word `w7`** " + C +
     "`0x04` is the header flag, CONTRACT-phyre-packed-namespace.md NS-1; 12 and 20 both carry it, and 12 has no "
     "`0x10`)* — in this title"),
    # C-V41: the three sizes size buffers the loader allocates and fills from the stream (00686DE0: 00686E2C-00686E44).
    (HDR, "**The three D3D11 sizes tell the loader how much GPU memory to reserve.**",
     "**The three D3D11 sizes tell the loader how much ~~GPU~~ memory to reserve.** " + C + "`00686D10` copies "
     "them into the load record and `00686DE0` allocates that many bytes (`00686E2C`-`00686E32`, `0017D260`) and "
     "reads them from the file (`00686E44`, `0059D510`); what the D3D11 side does with the buffers is not read "
     "here)*"),
    # C-S27: 0059A6F0 read in the contract.
    (HDR, "| `0059A6F0` | reads the packed namespace — **not read here** | 116 B |",
     "| `0059A6F0` | reads the packed namespace — ~~**not read here**~~ *(answered: see "
     "CONTRACT-phyre-cluster-header.md, 0059A6F0 read in full; 2026-10-02, OPUS)* | 116 B |"),

    # C-V25 / C-V26 / C-V27: the formula's signature, buffer and namespace-reader argument order.
    (CHDR, "                            bool checkPlatform, uint32 *outSize, bool *outSwapped)\n",
     "                            bool checkPlatform, uint32 *outSize, bool *outSwapped)   // " + K + "real order "
     "is (s, h, nsBuf r8, buf r9, outSwapped [rsp+0x28], outSize [rsp+0x30], checkPlatform [rsp+0x38]): 0059A3C3, "
     "0059A3CB, 0059A3F6, 0059A4DF, 0059A445 - section 2\n"),
    (CHDR, "        if (!grow(nsBuf, size)) return 0xD;\n",
     "        if (!grow(nsBuf, size)) return 0xD;   // " + K + "the grown buffer is r9's, not nsBuf: 0059A50E "
     "mov rcx, r12 (r9) then 0067B100\n"),
    (CHDR, "        memcpy(nsBuf->p, h, 84);                  /* 5 x movups + 1 dword */\n",
     "        memcpy(nsBuf->p, h, 84);                  /* 5 x movups + 1 dword */   // " + K + "into r9's "
     "buffer (0059A52E rdx = [r12+8]), as ten movups plus one dword\n"),
    (CHDR, "                                   h->m_packedNamespaceSize - take, *outSwapped);\n",
     "                                   h->m_packedNamespaceSize - take, *outSwapped);   // " + K + "0059A6F0 "
     "takes (s, swapped dl, buffer r8, length r9d): 0059A5B5-0059A5BF\n"),
    # C-V28: the only caller zeroes the buffer, so the zero-length case is refused (0059A4D6 -> 0059A598).
    (CHDR, "while a zero-length namespace whose capacity already reads zero is accepted, because the second never "
           "replaces the buffer.",
     "while a zero-length namespace whose capacity already reads zero is ~~accepted, because the second never "
     "replaces the buffer~~ refused too in this build " + C + "the null-buffer test at `0059A4D3`-`0059A4D6` comes "
     "first, as §13a says, and the only caller `0059E070` zeroes the buffer, `0059E115`-`0059E11A`; it would pass "
     "only with a non-null buffer of capacity zero, which nothing supplies)*."),
    # C-V31: ten movups, five transfers.
    (CHDR, "`0059A536`–`0059A55F` is five `movups` of 16",
     "`0059A536`–`0059A55F` is ~~five `movups` of 16~~ ten `movups`, five 16-byte loads and five stores " + C +
     "§15a)*, of 16"),
    # C-V33: eight bswaps over the fixed dwords (0059C18B..0059C1C2), fourteen in the whole body.
    (CHDR, "**fourteen `bswap`s over eight fixed dwords,",
     "**~~fourteen~~ eight `bswap`s over eight fixed dwords " + C + "`0059C18B`-`0059C1C2`; the body has fourteen "
     "in all, six more in the loop at `0059C206`-`0059C22E`)*,"),
    (CHDR, "it is the table layout made executable — fourteen",
     "it is the table layout made executable — ~~fourteen~~ eight " + C + "`0059C18B`-`0059C1C2`; fourteen is the "
     "whole body's count)*"),
    # C-V40: two call sites; 0059A5D7 is the equal path.
    (CHDR, "**re-read**: `0059A5BF`, `0059A5D7` and the equal path all call it |",
     "**re-read**: ~~`0059A5BF`, `0059A5D7` and the equal path all call it~~ two call sites, `0059A5BF` for the short "
     "and long paths and `0059A5D7` for the equal path " + C + "the only two direct callers of `0059A6F0`)* |"),
    # C-V41: 00686D10 always returns 0; the copied sizes size the buffers 00686DE0 allocates and reads.
    (CHDR, "three-field status copy\n",
     "three-field ~~status~~ size copy " + C + "it returns 0 on both paths, `00686D26` and `00686D38`)*\n"),
    (CHDR, "the loader's error-field\npropagation.",
     "~~the loader's error-field~~\n~~propagation.~~ the header's three D3D11 sizes, which `00686DE0` allocates "
     "(`00686E2C`-`00686E32`) and reads from the file (`00686E44`) " + C + "no error is produced or "
     "propagated)*."),
    # C-S29 / C-S30: executed 2026-09-12 and 2026-09-18.
    (CHDR, "| any execution of this ladder, isolated or live | **none**; §13 |",
     "| any execution of this ladder, isolated or live | ~~**none**; §13~~ *(answered: see §13, executed "
     "2026-09-12 by diff_phyre_header.py, and §13a, 2026-09-18; 2026-10-02, OPUS)* |"),
    (CHDR, "> **The byte-swap block is the one that matters and the one that cannot be run.** Its",
     "> **The byte-swap block is the one that matters and the one that cannot be run.** *(answered: see §13a - it "
     "was run 2026-09-18; 2026-10-02, OPUS)* Its"),

    # C-V36: bit 1 marks an object pointer (0063C12A shr edx,1 ... 0063C135 test al,1); bit 31 is not consulted.
    (NS, "PString               1   m_buffer +0        (attribute 0x80000010 - the pointer bit)\n",
     "PString               1   m_buffer +0        (attribute 0x80000010 - the pointer bit)   " + K + "bit 31 is "
     "not the pointer bit; 0063C0C0 tests bit 1 (0063C12A-0063C135), see the correction above\n"),
    (NS, "**`m_buffer` is the only field in the file with attribute bit 31 set, and it is the one field that is\n"
         "a pointer** —",
     "**`m_buffer` is the only field in the file with attribute bit 31 set, ~~and it is the one field that is~~\n"
     "~~a pointer~~** " + C + "object pointers carry bit 1, which `0063C0C0` tests at `0063C12A`-`0063C135`; "
     "`m_effectVariant`, `m_mesh` and `m_asset` are pointers too)* —"),
    # C-V35 / C-S31: w7 bits 1-3 named by NS-1 (0x02 abstract, 0x04 header, 0x08 no default constructor).
    (NS, "set on 0 shipped records** (`SD-65`); bits 1–5 stay\n  unexplained.",
     "set on 0 shipped records** (`SD-65`); bits 1–5 ~~stay~~\n  ~~unexplained~~ *(answered: see "
     "CONTRACT-phyre-packed-namespace.md NS-1, 2026-09-26 - `0x02` abstract, `0x04` header, `0x08` no default "
     "constructor; 2026-10-02, OPUS)*."),
    (NS, "bits 1–5 not established (values 0, 2, 8, 12, 20, 32, 34, 40",
     "bits 1–5 ~~not established~~ *(answered: see CONTRACT-phyre-packed-namespace.md NS-1 - `0x02` abstract, "
     "`0x04` header, `0x08` no default constructor; 2026-10-02, OPUS)* (values 0, 2, 8, 12, 20, 32, 34, 40"),
    # C-V37: the two helpers run on different records (0059E27F rcx = rbp+0x30 / 0059E289 rcx = rsp+0x70).
    (NS, "is the four-vector teardown sibling covering the upper half of the same record:",
     "is the four-vector teardown sibling ~~covering the upper half of the same record~~ for a different record "
     + C + "`0059E070` calls it with `rcx = rbp+0x30` at `0059E27F`-`0059E283` and `00598040` with `rcx = rsp+0x70` "
     "at `0059E289`-`0059E28E`; the two offset lists overlap at `+0x38`/`+0x40`)*:"),
    (NS, "dealloc-and-clear pattern. Together with `00598040` it spans `+0x08..+0x58` — eight counted buffers.",
     "dealloc-and-clear pattern. ~~Together with `00598040` it spans `+0x08..+0x58` — eight counted buffers.~~ Each helper frees four counted "
     "buffers of its own record " + C + "different `rcx`, above)*."),
    # C-S28 / C-S32.
    (NS, "| `0059C180` | the namespace byte-swap fixup — **not read** | — |",
     "| `0059C180` | the namespace byte-swap fixup — ~~**not read**~~ *(answered: see section 8, read 2026-09-07; "
     "2026-10-02, OPUS)* | — |"),
    (NS, "| **Why they cluster there** | **not established — a reading, no constructor read** | 8 |",
     "| **Why they cluster there** | ~~**not established — a reading, no constructor read**~~ *(answered: see "
     "CW-3, 2026-09-26; 2026-10-02, OPUS)* | 8 |"),

    # C-V34: five of the nine words use bswap; words 0, 4, 5, 6 are open-coded (0059A790-0059A7C4, 0059A7E0-0059A887).
    (CNS, "swapping **nine** words per record; the first is an inlined byte-reversal, the rest `bswap` |",
     "swapping **nine** words per record; ~~the first is an inlined byte-reversal, the rest `bswap`~~ words 1-3 and "
     "7-8 by `bswap`, words 0 and 4-6 open-coded " + C + "`0059A7CB`, `0059A7D3`, `0059A7DB`, `0059A88E`, "
     "`0059A896` are the five `bswap`s; §15a)* |"),
    # C-S31.
    (CNS, "`NS-1`'s bit names and `NS-4` stay open, and the",
     "`NS-1`'s bit names and `NS-4` stay open *(answered: see NS-1 and NS-4, both answered 2026-09-26, below; "
     "2026-10-02, OPUS)*, and the"),

    # C-V42: byte offsets - 00633390 reads +0xE8 (006333BF), +0x70 (006333DC), walks +0x80/+0x90/+0xA0/+0xB0
    #     (006334B2 / 006333E6 / 0063344E / 0063352C) and unlinks +0x60 (00633557); the name is char* +0x30 (006388CA).
    (CDMS, "| `+0x0C` | `FUN_006b6700` | embedded string (the class name) |",
     "| ~~`+0x0C`~~ `+0x60` | `FUN_006b6700` | ~~embedded string (the class name)~~ a sixth intrusive list " + C +
     "qword indices, see the unit correction below; `00633557` passes `+0x60` to the list-unlink `006B6700`; the "
     "name is the `char *` at `+0x30`, `006388CA`)* |"),
    (CDMS, "| `+0x0E` | `FUN_0063d640` | a sub-object, destroyed first |",
     "| ~~`+0x0E`~~ `+0x70` " + C + "`006333DC`)* | `FUN_0063d640` | a sub-object, destroyed first |"),
    (CDMS, "| `+0x10` | intrusive list walk | list #1 |",
     "| ~~`+0x10`~~ `+0x80` " + C + "`006334B2`)* | intrusive list walk | list #1 |"),
    (CDMS, "| `+0x12` | intrusive list walk | list #2 |",
     "| ~~`+0x12`~~ `+0x90` " + C + "`006333E6`)* | intrusive list walk | list #2 |"),
    (CDMS, "| `+0x14` | intrusive list walk | list #3 |",
     "| ~~`+0x14`~~ `+0xA0` " + C + "`0063344E`)* | intrusive list walk | list #3 |"),
    (CDMS, "| `+0x16` | intrusive list walk | list #4 |",
     "| ~~`+0x16`~~ `+0xB0` " + C + "`0063352C`)* | intrusive list walk | list #4 |"),
    (CDMS, "| `+0x1D` | compared to `DAT_02CF8260` | a generation / registration counter |",
     "| ~~`+0x1D`~~ `+0xE8` " + C + "`006333BF mov eax, [rcx+0xe8]` against `02CF8260` at `006333C7`)* | "
     "compared to `DAT_02CF8260` | a generation / registration counter |"),
    (CDMS, "| `02CF8260` | global compared against descriptor `+0x1D` | — |",
     "| `02CF8260` | global compared against descriptor ~~`+0x1D`~~ `+0xE8` " + C + "byte offset, `006333BF`)* | — |"),
    (CDMS, "  +0x0C   str    embedded string (class name)\n",
     "  +0x0C   str    embedded string (class name)   " + K + "qword index; byte +0x60 is a list cleared by "
     "006B6700 (00633557), the name is the char * at byte +0x30 (006388CA)\n"),
    # C-V43: 006B6700 is a list-unlink loop (006B6710-006B6744), not a string destructor.
    (CDMS, "    FUN_006b6700(self + 7);                       // destroy an embedded string (the name)\n",
     "    FUN_006b6700(self + 7);                       // destroy an embedded string (the name)   // " + K +
     "006B6700 unlinks every node of the list at +0x38 (006B6710-006B6744); no string\n"),
    (CDMS, "  +0x38   str    embedded string (member name)\n",
     "  +0x38   str    embedded string (member name)   " + K + "an intrusive list head cleared by 006B6700 "
     "(00633278-0063327C); the name pointer is at +0x20\n"),
    # C-V44: member +0x28 bit 0 tested (00633282 with rdi = rbx+8) and member +0x20 freed (00633288).
    (CDMS, "and conditionally free `[+0x18]` when `[+0x20] & 1`.",
     "and conditionally free ~~`[+0x18]` when `[+0x20] & 1`~~ member `+0x20` when member `+0x28` bit 0 is set " + C +
     "the offsets were relative to the node at member `+0x08`: `00633261 lea rdi, [rcx+8]`, `00633282 test byte "
     "ptr [rdi+0x20], 1`, `00633288 mov rcx, [rdi+0x18]`)*."),
    # C-V57 / C-V58: the call chain's counts (ledger: 255 static initialisers, 404 / 853 teardowns).
    (CDMS, "     -> PClassDescriptorConcrete<T> static initializer      (227 of these)\n",
     "     -> PClassDescriptorConcrete<T> static initializer      (227 of these)   " + K + "255 in the ledger, "
     "254 in the family file (section 2's table)\n"),
    (CDMS, "     -> ClassDescriptorStaticTeardown       (372)\n",
     "     -> ClassDescriptorStaticTeardown       (372)   " + K + "404 (section 2's table, the ledger)\n"),
    (CDMS, "     -> DataMemberMetadataStaticTeardown    (830)\n",
     "     -> DataMemberMetadataStaticTeardown    (830)   " + K + "853 (section 2's table, the ledger)\n"),
    # C-V62: slot +0x50 of the 331 Concrete<T> descriptor vtables is a per-class construct-in-place body, never the
    #     xor al,al stub 00657140; 00639A60 hands off to 0063CB80 only on flags bit 0 (00639AB6-00639ABE) or a false
    #     +0x50 (00639B20-00639B25).
    (CDMS, "`+0x50` returns **false on every class measured**, so `00639A60` always hands off to `0063CB80`",
     "`+0x50` ~~returns **false on every class measured**, so `00639A60` always hands off to `0063CB80`~~ returns "
     "false only on some classes, so `00639A60` hands off to `0063CB80` only then or when flags bit 0 is set " + C +
     "`00639AB6`-`00639ABE` and `00639B20`-`00639B25`; slot `+0x50` of all 331 `Concrete<T>` vtables is a per-class "
     "construct body, never the `xor al, al` stub `00657140`; the WITHDRAWN block above)*"),
    (CDMS, "> survives untouched: the stub is measured, the branch is measured, `0063CB80` always runs.",
     "> survives untouched: the stub is measured, the branch is measured, ~~`0063CB80` always runs~~ `0063CB80` "
     "runs only on flags bit 0 or a false `+0x50` " + C + "`00639AB6`-`00639ABE`, `00639B20`-`00639B25`)*."),
    # C-V61 / C-S: +0xD0 has a reader-builder, 00639C80 (00639CD8-00639CE4).
    (CDMS, "| `+0xD0` | a third buffer registered by the same family; **no reader identified** |",
     "| `+0xD0` | a third buffer registered by the same family; ~~**no reader identified**~~ a byte mask over the "
     "instance, built by `00639C80` " + C + "zero-filled at `00639CD8`-`00639CE4`; "
     "CONTRACT-phyre-class-descriptor.md, purpose read 2026-09-25)* |"),
    # C-V63: head insertion - r14 = rbx+0x10 sentinel (006391C2), H.next = N at 00639244.
    (CDMS, "else appending `rdi+0x50` into `[rbx+0x10]`'s list (`006391FF`..`00639244`",
     "else ~~appending~~ linking `rdi+0x50` at the head of `[rbx+0x10]`'s list " + C + "`r14 = rbx+0x10` is the "
     "sentinel, `006391C2`; `00639244 mov [r14], rdx` makes the node the first, next being node `+0`, as "
     "`006B6710` walks it)* (`006391FF`..`00639244`"),
    # C-V64: 00632C90 is a 226-byte descriptor constructor (stamps 00D581C0 at 00632CD7, ret 00632D71).
    (CDMS, "**00632C90** (66 B; heads the ICF-folded cluster of identical scalar-deleting destructors",
     "**00632C90** (~~66 B; heads the ICF-folded cluster of identical scalar-deleting destructors~~ 226 B, a "
     "`PClassDescriptor` constructor " + C + "it self-links `+0x08`/`+0x50`/`+0x60`, stores the name at `+0x30`, "
     "stamps `00D581C0` at `00632CD7` and zeroes `+0xF0`/`+0xF8`, ending at `00632D71`; the destructor described "
     "next is not at this address)*"),
    # C-S33 / C-S34.
    (CDMS, "| `0063D640` | descriptor sub-object destructor | not read |",
     "| `0063D640` | descriptor sub-object destructor | ~~not read~~ *(answered: see "
     "CONTRACT-phyre-class-descriptor.md, 0063D640 takes (rcx = the sub-object, rdx = the descriptor); "
     "2026-10-02, OPUS)* |"),
    (CDMS, "**Four separate intrusive linked lists.** Their individual roles are not established — see §7.\n",
     "**Four separate intrusive linked lists.** Their individual roles are not established — see §7. *(answered: "
     "see the unit correction below - six lists, four walked - and CONTRACT-phyre-class-descriptor.md's "
     "destructor correction, 2026-09-12; 2026-10-02, OPUS)*\n"),

    # C-V48: the base descriptor is 0x100 (90 adjacent static descriptors sit 0x100 apart); 0x140 is the Dynamic form.
    (CCD, "| size | **at least `0x140`** — `0063D550` writes `+0x138` and `+0x104`; the exact end is not established (§14) |",
     "| size | ~~**at least `0x140`**~~ **`0x100`**, and `0x140` for `PClassDescriptorDynamic` " + C + "PCD-3, "
     "answered 2026-09-25; 90 pairs of the schema's static descriptors sit exactly `0x100` apart in `.data`)* — "
     "`0063D550` writes `+0x138` and `+0x104`, fields of the Dynamic form ~~; the exact end is not established "
     "(§14)~~ |"),
    # C-V60: entry stamps PClassDescriptor (006333B5-006333BC, 00D581C0), exit PType (00633561-00633568, 00D31168).
    (CCD, "| `+0x00` | 8 | vftable. The destructor overwrites it with `PType`'s before releasing anything |",
     "| `+0x00` | 8 | vftable. The destructor overwrites it with ~~`PType`'s before releasing anything~~ "
     "`PClassDescriptor`'s on entry and `PType`'s on exit " + C + "`006333BC` stores `00D581C0`, "
     "`.?AVPClassDescriptor@Phyre@@`; `00633568` stores `00D31168`, `.?AVPType@Phyre@@`)* |"),
    # C-V61: +0xC8 / +0xD0 are byte masks over the instance (00639C80: 0xFF fill 00639CD3, zero fill 00639CE4).
    (CCD, "| `+0xC8` | 8 | **a second full-size instance**, set by",
     "| `+0xC8` | 8 | ~~**a second full-size instance**~~ **an instance-size byte mask** " + C + "`00639C80` fills it "
     "with `0xFF` over the instance size, `00639CBE`-`00639CD3`; purpose read below)*, set by"),
    (CCD, "| `+0xD0` | 8 | **a third full-size instance**, set by",
     "| `+0xD0` | 8 | ~~**a third full-size instance**~~ **an instance-size byte mask** " + C + "`00639C80` "
     "zero-fills it, `00639CD8`-`00639CE4`)*, set by"),
    # C-V63: head, not append.
    (CCD, "when the parent's `+0x70` is the same registry, and appends it otherwise |",
     "when the parent's `+0x70` is the same registry, and ~~appends it otherwise~~ links it at the head otherwise "
     + C + "`0063922E`-`00639244` sets the sentinel `rbx+0x10`'s first pointer to the node)* |"),
    # C-S35 / C-S36.
    (CCD, "| any execution of any of this | **none**; §13 |",
     "| any execution of any of this | ~~**none**; §13~~ *(answered: see the EXP-097 execution and the PCD-3 "
     "answer; 2026-10-02, OPUS)* |"),
    (CCD, "   - **Not established:** what `+0x38` measures, and so what the two totals mean.\n",
     "   - **Not established:** what `+0x38` measures, and so what the two totals mean. *(answered: see the "
     "2026-09-20 reading - `+0x38` is this contract's own size field, the one `0063C910` passes to `memcpy`; "
     "2026-10-02, OPUS)*\n"),

    # C-V45: 0063C0C0 returns a literal 8 only with a null context (0063C0D3 -> 0063C17D); with a context the pointer
    #     width is ctx->vslot08() (0063C100-0063C106) and the inline width ctx->vslot10(type) or type+0x38.
    (MR, "| `0063C0C0` | `FieldStorageWidth` | — | returns 8 when attribute bit 1 is set, else the type's inline size "
         "from `type+0x38` |",
     "| `0063C0C0` | `FieldStorageWidth` | — | ~~returns 8 when attribute bit 1 is set, else the type's inline "
     "size from `type+0x38`~~ when bit 1 is set returns `ctx->vslot08()`, or a literal 8 when `ctx` is null, else "
     "the inline width " + C + "`0063C100`-`0063C106` and `0063C137`; null context `0063C0D3` → `0063C17D`)* |"),
    (MR, "                   storage size of literally 8 when this bit is set, and the type's own\n",
     "                   storage size of literally 8 when this bit is set, and the type's own   " + K + "8 only "
     "with a null context (0063C0D3 -> 0063C17D); with one it is ctx->vslot08() (0063C106)\n"),
    (MR, "complete body of `0063C0C0`: returns literally `8` when bit 1 is set, else",
     "complete body of `0063C0C0`: returns ~~literally `8`~~ the context's pointer width (a literal `8` only "
     "for a null context) " + C + "`0063C106`, `0063C17D`)* when bit 1 is set, else"),
    (MR, "no direct calls; returns 8 when attribute bit 1 is set, else the type's inline size from `type+0x38`.",
     "no direct calls; returns ~~8~~ `ctx->vslot08()` " + C + "`0063C106`; a literal 8 only for a null context, "
     "`0063C17D`)* when attribute bit 1 is set, else the type's inline size from `type+0x38`."),
    (MR, "(`0063C106: call qword ptr [rax+8]` with `rcx = rdx = ctx`), not a constant in this function.",
     "(`0063C106: call qword ptr [rax+8]` with `rcx = rdx = ctx`)~~, not a constant in this function~~, and a "
     "literal 8 when `ctx` is null " + C + "`0063C0D3` jumps to `0063C14C`, which loads `mov eax, 8` at `0063C17D`)*."),
    # C-V46: +0xF4 is the running sum of +0xF0 up the parent chain (0063E416-0063E448), not zero.
    (MR, "`descriptor+0xF4`/`+0xF8` are the offset adjustments, both zero (§12).",
     "`descriptor+0xF4`/`+0xF8` are the offset adjustments, ~~both zero (§12)~~ sums of `+0xF0` up the parent "
     "chain " + C + "`0063E410`, `0063E416`-`0063E448`; §16 below)*."),
    # C-V48: descriptors are 0x100 (base), 0x140 (Dynamic).
    (MR, "Descriptors are about\n0x110 bytes and packed in `.data`",
     "Descriptors are ~~about~~\n~~0x110 bytes~~ `0x100` bytes " + C + "90 pairs of static descriptors sit exactly "
     "`0x100` apart; `0x140` is `PClassDescriptorDynamic`, CONTRACT-phyre-class-descriptor.md PCD-3)* and packed "
     "in `.data`"),
    # C-V49: 00632960 stores arg5 (offset) at +0x48 (006329B9-006329BD) and 0 at +0x50 (006329C0).
    (MR, "`00D580B0` installs at `006329B6`, `+0x48`/`+0x50` take the name and context args,",
     "`00D580B0` installs at `006329B6`, `+0x48`/`+0x50` ~~take the name and context args~~ take the field offset "
     "(argument 5) and zero " + C + "`006329B9`-`006329C0`; the name goes to the node through `00632FB0` and the "
     "context only to the attach call)*,"),
    # C-V55: 103 bytes (008AF9D0 ends at 008AFA37).
    (MR, "| `008AF9D0` | `02CF90E0` | `m_offsetFromParent` (`0xF0`) | same 96-byte `PClassDataMember` teardown shape |",
     "| `008AF9D0` | `02CF90E0` | `m_offsetFromParent` (`0xF0`) | same ~~96-byte~~ 103-byte " + C + "`008AF9D0` "
     "returns at `008AF9D0+0x66`; the array-member page's 103)* `PClassDataMember` teardown shape |"),
    # C-S37 / C-S38 / C-S39 / C-S40 / C-S41.
    (MR, "list-unlink helper. Only `+0x80` is identified.",
     "list-unlink helper. Only `+0x80` is identified *(answered: see BL-8 - four of six identified, `+0x60` "
     "2026-09-25; 2026-10-02, OPUS)*."),
    (MR, "**(c) is the whole remaining search space, and it is not searched here.** The row",
     "**(c) is the whole remaining search space, and it is not searched here.** *(answered: see the ANSWERED "
     "2026-09-25 block above; 2026-10-02, OPUS)* The row"),
    (MR, "the `+0x4` dword's purpose; the other 186 unharvested registrations (`RM-1`).",
     "the `+0x4` dword's purpose; the other 186 unharvested registrations (`RM-1`) *(answered: see RM-1, "
     "ANSWERED 2026-09-27 - all 215 registrations of the three constructors are in the store; 2026-10-02, OPUS)*."),
    (MR, "the exact type and offset, so the schema side of the propagation is complete and this is about what",
     "the exact type and offset, so the schema side of the propagation is complete *(answered: see §20, corrected "
     "2026-09-27 - four more registrations were added; 2026-10-02, OPUS)* and this is about what"),
    (MR, "something about the corpus rather than the method: **the registered Phyre hierarchy here is\nshallow.** "
         "Almost",
     "something about the corpus rather than the method: **the registered Phyre hierarchy here is\nshallow.** "
     "*(answered: see §19c - this reading of control 5 was wrong; 2026-10-02, OPUS)* Almost"),

    # C-V54: the array registrations are lazy too - all 124 functions that call 00632A10 call _Init_thread_header
    #     008092FC (246 of the 248 for 00632960).
    (AR, "class-descriptor initialisers (static init)\n",
     "class-descriptor initialisers (static init)   " + K + "lazy: all 124 functions calling 00632A10 sit behind "
     "_Init_thread_header 008092FC, run the first time the class is touched\n"),
    (AR, "the member descriptors are built by code at static initialisation.",
     "the member descriptors are built by code ~~at static initialisation~~ lazily, the first time the class is "
     "touched " + C + "all 124 functions that call `00632A10` also call `_Init_thread_header` `008092FC`; "
     "member-registration-and-the-recovered-field-schema.md, correction to a sibling document)*."),
    # C-V56: the elements are initialised in the file image (each 0x50 element carries 19-31 non-zero bytes).
    (AR, "own 15-byte thunk, and `_Init_thread_footer`. The objects are zero-initialised and only",
     "own 15-byte thunk, and `_Init_thread_footer`. ~~The objects are zero-initialised and only~~ The objects are "
     "initialised in the image " + C + "every element from `01F2E330` to `01F2E790` carries non-zero bytes in the "
     "file, self-links among them; answered 2026-09-14 below)* and only"),
    # C-S42.
    (AR, "| 98 B each | 26–52 | **seven lazy-static accessors**, §5 |",
     "| 98 B each | 26–52 | **seven lazy-static accessors**, §5 *(answered: see §9 - there are fifteen, "
     "2026-09-13; 2026-10-02, OPUS)* |"),
    # C-S43.
    (IS, "so the parent of each class is\n  *not* recovered by this sweep and no class hierarchy is asserted.",
     "so the parent of each class is\n  *not* recovered by this sweep and no class hierarchy is asserted *(answered: "
     "see member-registration-and-the-recovered-field-schema.md §19 and members/phyre-class-parent-chain.tsv; "
     "2026-10-02, OPUS)*."),

    # C-V67: the named library spans 008140A0-00828D30 (148 luaL_Reg records; io 00825xxx-00826500, os 00827430,
    #     debug 00828540, package 00828D30).
    (LUA, "the named functions span `00814xxx`–`0081Cxxx`, which is where",
     "the named functions span ~~`00814xxx`–`0081Cxxx`~~ `008140A0`–`00828D30` " + C + "the 148 registration "
     "records point as far as `luaopen_package` `00828D30`, with `io` at `00825xxx`-`00826500`, `os` `00827430` and "
     "`debug` `00828540`; the link range of the 2026-09-13 note above)*, which is where"),
    # C-V69: math / bit32 / string / coroutine opens also have a lea in 00685AC0 (00685ADD, 00685AF0, 00685B03,
    #     00685B16); the other six only their table qword.
    (LUA, "Each open function's **only** reference in\n      the image is its table entry (one 8-byte hit each;",
     "Each open function's ~~**only**~~ reference in\n      the image is its table entry " + C + "and four of them, "
     "`luaopen_math`, `luaopen_bit32`, `luaopen_string`, `luaopen_coroutine`, also have a `lea` in `00685AC0`, "
     "`00685ADD`, `00685AF0`, `00685B03`, `00685B16`; UQ-284 below)* (one 8-byte hit each;"),
    # C-V70: 00681720 and 00681880 re-stamp their vtables on teardown (00681727, 00681897): destructors.
    (LUA, "| `PScripting::PAsyncProcessBuffer` | `00D6FD50` | `00681560`, `00681720` |",
     "| `PScripting::PAsyncProcessBuffer` | `00D6FD50` | `00681560` " + C + "`00681720` re-stamps `00D6FD50` at "
     "`00681727` and unlinks, call-free - the teardown, not a constructor)* |"),
    (LUA, "| `PScripting::PScheduler` | `00D6FD68` | `00681560`, `00681880` |",
     "| `PScripting::PScheduler` | `00D6FD68` | `00681560` " + C + "`00681880`, which re-stamps `00D6FD68` at "
     "`00681897`, is the destructor, as the 2026-09-22 section says)* |"),
    # C-V71: 02E41570 is the list count (006844CB, 0068458A with the buffer 02E41578).
    (LUA, "The sixth `0x100` slot `02E41570` belongs to a class none of the five registers and is outside this "
          "question.",
     "The sixth `0x100` slot `02E41570` ~~belongs to a class none of the five registers and is outside this "
     "question~~ is no class slot " + C + "it is the count of the `(name, luaopen_*)` list, read and written with "
     "its buffer `02E41578` by `006844C0` at `006844CB` and `0068458A`; UQ-284 below)*."),
    # C-V73: the adapter's own arguments are (?, L, obj): 005A0E80 moves rdx -> rcx and r8 -> rdx.
    (LUA, "void FUN_005a0e80(L, obj, ctx) { thunk_FUN_00682d20(obj, ctx, &DAT_02cad640); return; }\n",
     "void FUN_005a0e80(L, obj, ctx) { thunk_FUN_00682d20(obj, ctx, &DAT_02cad640); return; }   // " + K +
     "the adapter takes (this, L in rdx, obj in r8) and calls 00682D20(L, obj, descriptor): 005A0E80-005A0E90\n"),
    # C-V79: a second gate exists - 00682A10 checks the registry's "Vector" metatable (00682A3F-00682A5F).
    (LUA, "is rejected by every accessor. Anything constructing",
     "is rejected by ~~every accessor~~ the object accessors " + C + "not the only gate: the vector getter "
     "`00682A10` compares against the registry's `\"Vector\"` metatable, `00682A3F`-`00682A5F`; "
     "phyre-script-object-accessors.md)*. Anything constructing"),
    # C-S20 / C-S21 / C-S22 / C-S23.
    (LUA, "see **R-4**, which is the single\nhighest-value open question in this document.",
     "see **R-4**, which is the single\nhighest-value open question in this document *(answered: see R-4, "
     "ANSWERED 2026-09-12 - no standard library is ever opened; 2026-10-02, OPUS)*."),
    (LUA, "| `01CCB3E0` | 8 | **loadedlibs — opened at startup** |",
     "| `01CCB3E0` | 8 | **loadedlibs — ~~opened at startup~~ never opened** *(answered: see R-4, 2026-09-12; "
     "2026-10-02, OPUS)* |"),
    (LUA, "**Upstream:** whatever schedules script execution — not yet identified (**R-5**).",
     "**Upstream:** whatever schedules script execution — not yet identified (**R-5**) *(answered: see R-5, "
     "ANSWERED 2026-09-22; 2026-10-02, OPUS)*."),
    (LUA, "| `00684D10` / `00686280` | Lua execution sites (`lua_pcall`) | not read |",
     "| `00684D10` / `00686280` | Lua execution sites (`lua_pcall`) | ~~not read~~ *(answered: see §12, the two "
     "callers executed, 2026-09-19; 2026-10-02, OPUS)* |"),

    # C-V76: null -> lua_checkstack(L, 1) then lua_pushnil 00810620; non-null -> the forwarder (e.g. 005A0EC0:
    #     005A0ED2-005A0EFB; 006B2B70: 006B2B8B-006B2BB6).
    (ACC, "the member records - this row disposes of the adapter, not the adapted. Selector: "
          "members/select_optptr_dispatch_siblings_2.py\"\n",
     "the member records - this row disposes of the adapter, not the adapted. Selector: "
     "members/select_optptr_dispatch_siblings_2.py\""
     "  # " + K + "branch sense: the null path calls 0080F420 with edx=1 then tail-jumps 00810620 (lua_pushnil), "
     "the non-null path tail-jumps the forwarder (005A0ED2-005A0EFB)\n"),
    (ACC, "x2 subset-shared, 6 distinct others). NOT dispositioned: the shared implementations and the member-specific "
          "ops - this row disposes of the adapter, not the adapted. Selector: "
          "members/select_optptr_dispatch_siblings_2.py\"\n",
     "x2 subset-shared, 6 distinct others). NOT dispositioned: the shared implementations and the member-specific "
     "ops - this row disposes of the adapter, not the adapted. Selector: "
     "members/select_optptr_dispatch_siblings_2.py\"  # " + K + "branch sense: null calls 0080F420 with edx=1 and "
     "tail-jumps 00810620, non-null tail-jumps the member forwarder with rdx=rdi (006B2B8B-006B2BB6)\n"),
    (ACC, "plus member-specific ops (5 distinct). NOT dispositioned: the shared implementations and the "
          "member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py\"\n",
     "plus member-specific ops (5 distinct). NOT dispositioned: the shared implementations and the "
     "member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py\"  # " + K + "branch sense: null "
     "calls 0080F420 with edx=1 and tail-jumps 00810620, non-null tail-jumps 00684080 (005A0B9B-005A0BC9)\n"),
    # C-V77: 0080F420 is lua_checkstack (stack room against edx, limit 0xF4240 at 0080F457); it pushes nothing.
    (ACC, "the shared implementation(s) 0080F420/0080FA50/00810240/00810F60. Selector: "
          "members/select_optptr_dispatch_siblings_4.py\"\n",
     "the shared implementation(s) 0080F420/0080FA50/00810240/00810F60. Selector: "
     "members/select_optptr_dispatch_siblings_4.py\"  # " + K + "0080F420 is lua_checkstack (0080F42E-0080F457, "
     "limit 0xF4240) and pushes nothing\n"),
    # C-S25.
    (ACC, "this path and does not write them through it.",
     "this path and does not write them through it *(answered: see below - `Get` hands out writable access, and "
     "AZ-2's \"script cannot write\" reading is refuted, 2026-09-14; 2026-10-02, OPUS)*."),
    (ACC, "- **XIIOnline:** these are read-side accessors for Phyre's own object graph.",
     "- **XIIOnline:** these are ~~read-side~~ accessors for Phyre's own object graph *(answered: see below - "
     "`Get` hands out writable access, 2026-09-14; 2026-10-02, OPUS)*."),

    # C-V80: kind 2 reads the object at +0x20 (005C753A mov rcx, [rbx+0x20]); kind 3 at +0x28 (005C751F).
    (ANI, "kind 2 -> 005A7E90(obj @ +0x28 ... ctx @ +0x18)             005C7531\n",
     "kind 2 -> 005A7E90(obj @ +0x28 ... ctx @ +0x18)             005C7531   " + K + "kind 2's object is +0x20 "
     "(005C753A mov rcx, [rbx+0x20]); +0x28 is kind 3's (005C751F)\n"),
    # C-V81: the shader-parameter binder writes kind 1 (005C1274 mov dword [rsi], 1).
    (ANI, "and, through kinds 2/3, arbitrary reflected properties including shader parameters.",
     "and, through kinds 2/3, arbitrary reflected properties ~~including shader parameters~~; shader parameters go "
     "through kind 1 " + C + "`PAnimationChannelTargetBindShaderParameter`'s binder `005C1160` writes kind 1 at "
     "`005C1274` and the destination at `005C127A`)*."),
    # C-V83: 00632FB0's rcx is the node at member +0x08 (00632998), so its +0x18 is member +0x20.
    (ANI, "copy `00861EBA`, pointer to `+0x18`)",
     "copy `00861EBA`, pointer to `+0x18` of the node at member `+0x08`, so member `+0x20` " + C + "`00632998` "
     "passes `rcx = member+8`; member `+0x18` is the owning class, `005C0999`)*)"),
    # C-S17 / C-S18 / C-S19.
    (ANI, "It means **no code in this document produces a kind-2 or",
     "It means *(answered: see BM-6, 2026-09-14 - the binder is a virtual family; 2026-10-02, OPUS)* **no code in "
     "this document produces a kind-2 or"),
    (ANI, "  +0x18  ...  (remaining 16 B not read by 005C72A0)\n",
     "  +0x18  ...  (remaining 16 B not read by 005C72A0)   " + K + "answered 2026-09-26: +0x18 u16 and +0x1C dword "
     "from the bind-time writer 005BF290, +0x20..+0x27 an uninterpreted tail\n"),
    (ANI, "The `ChannelValue` bytes `+0x18`..`+0x27` stay unread. Nothing",
     "The `ChannelValue` bytes `+0x18`..`+0x27` stay unread *(answered: see BM-3, ANSWERED 2026-09-26; "
     "2026-10-02, OPUS)*. Nothing"),
    (ANI, "**Not claimed.** The `ChannelValue` bytes `+0x18`..`+0x27` stay unread.",
     "**Not claimed.** The `ChannelValue` bytes `+0x18`..`+0x27` stay unread *(answered: see BM-3, ANSWERED "
     "2026-09-26; 2026-10-02, OPUS)*."),
    (ANI, "nothing in these bodies says whether it is.",
     "nothing in these bodies says whether it is *(answered: see UQ-280, 2026-09-14 - it is pure; 2026-10-02, "
     "OPUS)*."),

    # C-V86: the second test is offset >= 4 (001E3619 cmp r9w, 4 with r9w = word [rcx+0x10], 001E35FE).
    (PPF, "a second test requires `size >= 4`, and only",
     "a second test requires ~~`size >= 4`~~ `offset >= 4` " + C + "`001E3619 cmp r9w, 4`, `r9w` the offset loaded "
     "at `001E35FE`; the size is `dx`, `001E3620`)*, and only"),
    (PPF, "copies `r9w` bytes from",
     "copies ~~`r9w`~~ `r8w` " + C + "`r9w` is the offset, `0019458D`; the length is `r8w`, `00194599`)* bytes "
     "from"),
    # C-V87: 53 call sites in 21 functions; eleven of them in 0018D850..00190260.
    (PPF, "returns 0. Eleven call sites in `0018D850`–`00190260`.",
     "returns 0. ~~Eleven call sites in `0018D850`–`00190260`.~~ 53 call sites in 21 functions, eleven of them in "
     "`0018D850`–`00190260` " + C + "the rest include `001930F0`, `00191E90`, `001E2AF0`, `001EE8E0` and "
     "`001F7790`)*."),
    # C-V88: 2,839 B (the v4 extent of 001925D0).
    (PPF, "`001925D0` (~220 B) — an EH-protected pass body",
     "`001925D0` ~~(~220 B)~~ (2,839 B " + C + "its extent; the table above and the 2026-09-13 re-measure)*) — an "
     "EH-protected pass body"),
    # C-V89: 17 call sites in 16 functions; it names ColorBuffer / ColorBufferSampler / ColorBufferOffset.
    (PPF, "`001EE8E0` — 840 B, 7 callers; the submit composer",
     "`001EE8E0` — 840 B, ~~7 callers~~ 17 call sites in 16 functions " + C + "it also looks up `ColorBuffer`, "
     "`ColorBufferSampler` and `ColorBufferOffset` at `001EE97A`-`001EE9EC` and submits through `0060B980` at "
     "`001EEBE1`)*; the submit composer"),
    # C-V90: 00606A20 is the variant-key builder, not a teardown (00606AB3-00606ADF evaluators, 00606B10 search).
    (PPF, "`02CB6360` global, `00606A20`/\n`00606C60`/`00600B30` teardown).",
     "`02CB6360` global, ~~`00606A20`/~~\n`00606C60`/`00600B30` teardown; `00606A20` is the variant-key builder, "
     "not a teardown " + C + "it runs each switch evaluator, `00606AB3`-`00606ADF`, then binary-searches the "
     "variant table from `00606AFB`; the context-switch page)*)."),
    # C-V91: 005DC2F0 is PRenderer's constructor (stamps 00D49930 at 005DC375-005DC37C), with an embedded array.
    (PPF, "`005DC2F0` (267 B) is an array constructor over `eh_vector_constructor_iterator`;",
     "`005DC2F0` (267 B) is ~~an array constructor over `eh_vector_constructor_iterator`~~ `PRenderer`'s "
     "constructor, which also builds an embedded array through `eh_vector_constructor_iterator` " + C + "it "
     "stamps `00D49930`, `.?AVPRenderer@PRendering@Phyre@@`, at `005DC375`-`005DC37C`, the only reference to that "
     "vtable, then runs `00808FE4` over `+0x140`)*;"),
    # C-S46 / C-S47 / C-S48 / C-S49 / C-S50.
    (PPF, "**but the link is not\nread, and this document does not claim it.**\n",
     "**but the link is not\nread, and this document does not claim it.** *(answered: see the 2026-09-14 answer "
     "below - the `HDAO` setting selects the AO; 2026-10-02, OPUS)*\n"),
    (PPF, "| Which setting selects which AO | **not established** | — |",
     "| Which setting selects which AO | ~~**not established**~~ *(answered: see the 2026-09-14 answer, the `HDAO` "
     "setting; 2026-10-02, OPUS)* | — |"),
    (PPF, "  - **The class name is still open.** The reflection-schema route",
     "  - **The class name is still open.** *(answered: see the 2026-09-22 reading - not recoverable from this "
     "image by any route this database uses; 2026-10-02, OPUS)* The reflection-schema route"),
    (PPF, "| The context object's class | **not recovered** | — |",
     "| The context object's class | **not recovered** *(answered: see the 2026-09-22 reading - not recoverable "
     "from this image; 2026-10-02, OPUS)* | — |"),
    (PPF, "  **Still open:** what the asset puts in bits 13–15. It is",
     "  ~~**Still open:**~~ *(answered: see the ANSWERED 2026-09-27 line below - the shipped assets store 0; "
     "2026-10-02, OPUS)* what the asset puts in bits 13–15. It is"),
    (PPF, "| `001945B0` | 296 B, called before the parameter runs in several passes; **not read** |",
     "| `001945B0` | 296 B, called before the parameter runs in several passes; ~~**not read**~~ *(answered: see "
     "EA-6, 2026-09-12; 2026-10-02, OPUS)* |"),
    (PPF, "**The remaining 48 reference no string and were not read** (`EA-5`).",
     "**The remaining 48 reference no string and were not read** (`EA-5`) *(answered: see the 2026-09-21 reading - "
     "every one of the 48 now has an identity; 2026-10-02, OPUS)*."),
    (PPF, "members (458 B). `UQ-289` stays open on those 30.",
     "members (458 B). `UQ-289` stays open on those 30 *(answered: see UQ-289, superseded 2026-09-26; "
     "2026-10-02, OPUS)*."),

    # C-V93: 24 direct + 11 via a wrapper; the 36th, PDepthOfFieldLayered, has no descriptor type in RTTI at all.
    (PFX, "call to a wrapper that does it, and in **zero** cases not at all.",
     "call to a wrapper that does it, and in ~~**zero** cases not at all~~ one case not at all " + C + "the 36th, "
     "`PDepthOfFieldLayered`, has no `PClassDescriptor` type in the image's RTTI, so no slot 10 reaches it)*."),
    # C-V94: 66 distinct bodies reference the 36 family vtables.
    (PFX, "Each class's vtable is installed by exactly one body, in the `0064xxxx` band,",
     "Each class's vtable is installed by ~~exactly one body~~ one or more bodies " + C + "66 distinct bodies "
     "reference the 36 family vtables, 27 of them `PPostEffectBase`'s; P7 below)*, in the `0064xxxx` band,"),
    # C-V95: PMotionBlurD3D11 adds one 8-byte field, +0xD68 (ctor 0063F5B2; dtor 00646A4C-00646A59).
    (PFX, "| `00646A30` | `PMotionBlurD3D11` (second body) | 3 |",
     "| `00646A30` | `PMotionBlurD3D11` (second body) | ~~3~~ 1 " + C + "this is the destructor: it releases "
     "`+0xD68` through `006505A0`, `00646A4C`-`00646A59`, then re-stamps `00D61E50` and frees the base's "
     "`+0x30`/`+0x38`)* |"),
    (PFX, "| `0063F580` | `PMotionBlurD3D11` | 0 |",
     "| `0063F580` | `PMotionBlurD3D11` | ~~0~~ 1 " + C + "`0063F5B2` zeroes `+0xD68` after the base constructor "
     "`00646000`, which writes no further than `+0xD60`)* |"),
    (PFX, "— 58 bytes. Six of\nthe seven are that.",
     "— 58 bytes. ~~Six~~ Five of\nthe seven are that " + C + "`PMotionBlurD3D11` adds `+0xD68`, above)*."),
    # C-V96: one post-effect, PFXAA, is constructed by code (0018CFCE-0018CFD5 -> 00645DB0).
    (PFX, "**no code constructs one and no shipped asset names one**.",
     "**~~no code constructs one and~~ no shipped asset names one** " + C + "code constructs one, the `PFXAA` at "
     "context `+0x378`: `0018CFD5` calls `00645DB0`, which stamps `00D625D0` at `00645DD7`; CON-198 above)*."),

    # C-V98: 0018D0E0 has 52 direct call sites; the other six have none.
    (CTX, "| vtable-slot members (reached only through a data qword) | 7 |",
     "| vtable-slot members (reached ~~only~~ through a data qword; `0018D0E0` also has 52 direct call sites " + C +
     "the other six have none, CON-200)*) | 7 |"),
    # C-V99: the eleven bodies are reached from slot 6 (0065B920 at 00D626F0 = 00D626C0 slot 6).
    (CTX, "they are vtable slots, one of them `PPostProcessing::PScreenSpaceReflection` slot 1.",
     "they are vtable slots, one of them `PPostProcessing::PScreenSpaceReflection` slot ~~1~~ 6 " + C + "`0065B920` "
     "sits at `00D626F0`, slot 6 of `00D626C0`; the post-effect page's slot-6 render overrides, so these are "
     "post-effect workers)*."),
    # C-V101: +0x38 / +0x40 are rewritten before the key call (0060BC46 r13, 0060BC4D esi; key call 0060BDEF).
    (CTX, "| `+0x38`, `+0x40`, `+0x48` | `0` | `0060BAF3`, `0060BAFE`, `0060BB08` |",
     "| `+0x38`, `+0x40`, `+0x48` | `0`, then `+0x38` = a `0xC0`-stride geometry entry and `+0x40` = `esi` " + C +
     "`0060BC46` and `0060BC4D` overwrite the zeros before the key call at `0060BDEF`)* | `0060BAF3`, `0060BAFE`, "
     "`0060BB08` |"),
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
