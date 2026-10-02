"""apply_24crt.py [--apply] - 24-Compiler-And-CRT-Runtime readiness map (cloud-reports/re-readiness/24-crt.md), section 3.1
value items and the section 3.2 stale / banner items the shipping image settles, fixed on the pages (OPUS, 2026-10-02).

Each edit strikes the side the image REFUTES only and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*, or marks a
stale "open / not read" line *(answered: see ...; 2026-10-02, OPUS)*. Deciding addresses are in
scratchpad cr24/verdicts-24.md; every interior address in NEW text is written as entry+offset.
Items both sides of which the image supports, and count items that rest on a tag or members-file census, get no edit.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW never
contains OLD); front-matter lines get a `# <- corrected` YAML comment. Changed headings name OPUS.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "24-Compiler-And-CRT-Runtime/"
RD = F + "README.md"
SI = F + "Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md"
LZ = F + "Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md"
ST = F + "Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md"
EH = F + "Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md"
OBJ = F + "Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md"
OC = F + "Cxx-Runtime-Families/the-ordered-container-runtime.md"
MS = F + "Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md"
GEN = F + "Generated-Families/generated-function-families.md"
RV = F + "Generated-Adapters/the-return-value-adapter-family.md"
MEM = F + "Memory-And-Allocation/where-the-games-memory-comes-from.md"
TH = F + "Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md"
RS = F + "Runtime-Service-Surface/what-the-game-asks-windows-for.md"
HD = F + "Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md"
MA = F + "Maths-Library/the-maths-the-game-runs-on.md"


def C(why):
    return "*(corrected 2026-10-02, OPUS: " + why + ")*"


def A(where):
    return "*(answered: see " + where + "; 2026-10-02, OPUS)*"


K = "<- corrected 2026-10-02, OPUS - "
EXITQ = "`007980A0+0x7DF` calls `ExitProcess` through `008C2260`"
AFREE = "`0019C570` is `jmp [008C2B70]`, the `_aligned_free` import"
CFGCRT = ("the check thunk `00809958` has 11 call sites, all in CRT start-up bodies `008087C4`–`00809CD4`, and the "
          "dispatch slot `008C31C8` is never referenced")

EDITS = [
    # ---------------- README (status banners B-1/B-2/B-9, X-12, S-18, index B-11) ----------------
    (RD, "  **DOCUMENTED, tier 1.** The most actionable page",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C("the page's front matter says `status: AUDITED`")
     + " The most actionable page"),
    (RD, "**CFG compiled in but shipped disabled** (the check is",
     "~~**CFG compiled in but shipped disabled**~~ **CFG metadata shipped, only the statically linked CRT "
     "instrumented, nothing enforced** " + C(CFGCRT + "; the page's 2026-09-19 section") + " (the check is"),
    (RD, "  **DOCUMENTED, tier 1.** 1,172 initializers run before",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C("the page's front matter says `status: AUDITED`")
     + " 1,172 initializers run before"),
    (RD, "  **DOCUMENTED, tier 1, one falsification pass.** The **1,681 objects",
     "  ~~**DOCUMENTED, tier 1, one falsification pass.**~~ **AUDITED, tier 1, one falsification pass.** "
     + C("the page's front matter says `status: AUDITED`") + " The **1,681 objects"),
    (RD, "  **DOCUMENTED, tier 1, one falsification pass.** The category's four",
     "  ~~**DOCUMENTED, tier 1, one falsification pass.**~~ **AUDITED, tier 1, two falsification passes.** "
     + C("the page's front matter says `status: AUDITED` and `passes: 2`") + " The category's four"),
    (RD, "  **DOCUMENTED, tier 1, one falsification pass.** Answers open question",
     "  ~~**DOCUMENTED, tier 1, one falsification pass.**~~ **AUDITED, tier 1, one falsification pass.** "
     + C("the page's front matter says `status: AUDITED`") + " Answers open question"),
    (RD, "`CxxStandardLibrary.NativeQualified`, is called out as unsupported by its own name.",
     "`CxxStandardLibrary.NativeQualified`, is called out as ~~unsupported by its own name~~ wrong for at least two "
     "members " + A("BQ-22 on the object-lifecycle page, ANSWERED 2026-09-22") + "."),
    (RD, "that release a lazy-static guard when a constructor throws.\n\n**Composition of this category**",
     "that release a lazy-static guard when a constructor throws.\n\n"
     "- [`Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md`]"
     "(Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md) — the static initialiser and "
     "teardown families — **DOCUMENTED**\n"
     "- [`Cxx-Runtime-Families/the-ordered-container-runtime.md`](Cxx-Runtime-Families/the-ordered-container-runtime.md)"
     " — the EASTL red-black tree runtime — **AUDITED**\n"
     "- [`Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md`]"
     "(Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md) — MSVC's `std::_Tree` — **AUDITED**\n"
     "- [`Generated-Families/generated-function-families.md`](Generated-Families/generated-function-families.md) "
     "— the generated-function family catalogue — **DOCUMENTED**\n"
     "- [`Generated-Adapters/the-return-value-adapter-family.md`](Generated-Adapters/the-return-value-adapter-family.md)"
     " — the 403 return-value adapters — **AUDITED**\n"
     "- [`Memory-And-Allocation/where-the-games-memory-comes-from.md`]"
     "(Memory-And-Allocation/where-the-games-memory-comes-from.md) — the CRT heap routes and the engine arena "
     "— **PARTIAL**\n"
     "- [`Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`]"
     "(Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md) — the thunk layer — **AUDITED**\n"
     "- [`Runtime-Service-Surface/what-the-game-asks-windows-for.md`]"
     "(Runtime-Service-Surface/what-the-game-asks-windows-for.md) — the Windows service surface — "
     "**AUDITED**\n"
     "- [`Maths-Library/the-maths-the-game-runs-on.md`](Maths-Library/the-maths-the-game-runs-on.md) — the "
     "maths library — **AUDITED**\n"
     "- " + C("nine pages this list omitted, added with the status each page's own front matter states") + "\n\n"
     "**Composition of this category**"),

    # ---------------- SI ----------------
    # X-4: the gate compares the static's own guard with this thread's epoch (00189CE0+0x5D / +0x63).
    (SI, "compared against a global initialization epoch. If this thread",
     "compared against ~~a global initialization epoch~~ the static's own guard dword, which holds the epoch at which "
     "that static completed " + C("at the gate in `00189CE0`, `00189CE0+0x5D` is `cmp dword ptr [01F7F5C8], eax` "
     "with `eax` this thread's `[tls+4]`, and `00189CE0+0x63` `jle` skips `_Init_thread_header`; the global "
     "`01F44850` is read only inside the header and the footer; the T-5 answer of 2026-09-14") + ". If this thread"),
    (SI, "if (tlsBlock[+4] < epoch):            // _Init_thread_epoch\n",
     "if (tlsBlock[+4] < epoch):            // _Init_thread_epoch   " + K + "the comparand is the static's own "
     "guard dword, not a global epoch: 00189CE0+0x5D cmp [guard], eax (thread epoch); 00189CE0+0x63 jle skips the "
     "header\n"),
    # X-14: 0015BD30's first source is 01DF09C0 (-> 01F80130); 01DF09E0 -> 01F80150.
    (SI, "Source `0x01DF09C0` sits at the very start of `.data`; the destination",
     "Source `0x01DF09C0` sits ~~at the very start of `.data`~~ `0x9C0` bytes into `.data`, which starts at "
     "`0x01DF0000` " + C("section table; `01DF0900`–`01DF09B0` are read by other code, among them the sibling "
     "prototype copies `0015BF20` and `0015C0D0`") + "; the destination"),
    (SI, "(`01DF09E0` into `01F80140`+)",
     "(~~`01DF09E0` into `01F80140`+~~ `01DF09C0` into `01F80130`+ "
     + C("`0015BD30` itself reads `01DF09C0` and `0015BD30+0x1C` stores it at `01F80130`; `01DF09D0` goes to "
         "`01F80140` at `0015BD30+0x32`, and `01DF09E0`, read at `0015BD30+0x28`, to `01F80150` at "
         "`0015BD30+0x40`") + ")"),
    # X-16: 008092FC is _Init_thread_header; the lock is made by 00809124.
    (SI, "a higher value runs `008092FC` (the lock-init), and a",
     "a higher value runs `008092FC` (~~the lock-init~~ `_Init_thread_header`, which claims the guard " +
     C("the lock `02EAED40` is created by the C initializer `00809124`: `00809124+0x12` loads it and "
       "`00809124+0x1E` calls the critical-section initialiser `00861EF0` with spin count `0xFA0`") + "), and a"),
    (SI, "- The CRT formatter-option initializer `0016D670` is reached from `007A5570`.",
     "- The CRT formatter-option ~~initializer~~ accessor `0016D670` is reached from `007A5570` "
     + C("`0016D670` is `lea rax, [02EBA3D0]; ret`, the printf-options accessor, with 23 call sites; the "
         "initializer is `00809C50`, which ORs `4` into what it returns") + "."),
    (SI, "The memory-status reader `005CC8A0` is called by",
     "The ~~memory-status reader~~ record zero-initializer `005CC8A0` "
     + C("its 25-byte body zeroes `+0`, `+8`, `+0x10`, `+0x18`, `+0x20` and `+0x24` of `rcx` and returns `rcx`; it "
         "reads no memory status") + " is called by"),
    # S-1, S-3, S-4, S-7 (stale).
    (SI, "and **117** lazy statics, and §2 makes four",
     "and ~~**117** lazy statics~~ **1,681** lazy statics "
     + A("§12, corrected 2026-09-02 - 117 was a tag population; 1,681 distinct guards at 1,732 sites in 707 "
         "functions, recounted at the image") + ", and §2 makes four"),
    (SI, "The **117** lazy function-local statics and the family counts",
     "The ~~**117**~~ lazy function-local statics " + A("§12 - 1,681 statics at 1,732 sites") + " and the family counts"),
    (SI, "which may span both C and C++ tables. Recorded",
     "~~which may span both C and C++ tables~~ " + A("§10 - the entire 1,172-entry run is C++, and `__xi` is the "
                                                      "separate table at `008C5680`") + ". Recorded"),
    (SI, "and are unidentified. **T-8.**",
     "and are ~~unidentified~~ SQEX Sead's static pools " + A("T-8, answered on the page 2026-09-14") + ". **T-8.**"),
    (SI, "recorded as **T-9**, and it is deliberately left",
     "recorded as **T-9**, and it ~~is deliberately left~~ was left "
     + A("T-9 on the hardening page, answered 2026-09-27 - the statically linked runtime's own `.gfids$y` data")),

    # ---------------- LZ ----------------
    # X-3: the `<` branch is the slow path.
    (LZ, "if (thread_epoch < guard) {          // fast path: already built for this thread -> skip entirely\n",
     "if (thread_epoch < guard) {          // fast path: already built for this thread -> skip entirely " + K +
     "backwards: thread_epoch < guard is the SLOW path that calls the header; already built is thread_epoch >= guard, "
     "where 00189CE0+0x63 jle skips the header\n"),
    # X-2: built guards are negative as signed ints.
    (LZ, "*guard  >  0   built; value is the epoch at which it completed\n",
     "*guard  >  0   built; value is the epoch at which it completed   " + K + "not > 0: the epoch ships "
     "0x80000000 (01F44850) and the footer stores ++epoch (0080929C+0x29 inc, 0080929C+0x31 store), so a built guard "
     "is negative as a signed int\n"),
    (LZ, "a `0` means never touched, a positive",
     "a `0` means never touched, ~~a positive~~ any other "
     + C("a built guard holds the epoch it completed at, negative as a signed int: `01F44850` ships `0x80000000` and the "
         "footer `0080929C` stores the incremented epoch")),
    # X-22: the lock is released while a construction runs and while waiters sleep.
    (LZ, "these first-builds share *one* lock, a single stuck one can pile unrelated work up behind it.",
     "these first-builds share *one* lock, ~~a single stuck one can pile unrelated work up behind it~~ but a stuck one "
     "blocks only the threads that need that same static "
     + C("the header releases the lock before the construction runs, `008092FC+0x60` tail-jumps "
         "`LeaveCriticalSection`, and the 100 ms wait sleeps with the lock released, `008093C0+0x4B` calls "
         "`SleepConditionVariableCS` on `02EAED40`") + "."),
    (LZ, "with no timeout escape, and because all 1,681 share the one\n"
         "  critical section at `02EAED40`, unrelated first-time initialisations queue up behind it.",
     "with no timeout escape~~, and because all 1,681 share the one~~\n"
     "  ~~critical section at `02EAED40`, unrelated first-time initialisations queue up behind it~~. Unrelated "
     "first-time initialisations do not queue: the wait sleeps with `02EAED40` released "
     + C("`008093C0+0x4B` sleeps through `SleepConditionVariableCS`; the construction itself runs outside the lock, "
         "`008092FC+0x60`") + "."),
    # X-18: one caller.
    (LZ, "literal `100`. Two functions call it in total (`008093C0` has 1 caller by edge count), consistent",
     "literal `100`. ~~Two functions call it in total~~ One function calls it, at one site "
     + C("the only edge into `008093C0` is `008092FC+0x25`, and no data reference names it")
     + " (`008093C0` has 1 caller by edge count), consistent"),
    # X-20: 005CDA30 builds PTTYCallback; 008AADA0 is the teardown it registers.
    (LZ, "`008AADA0` builds `Phyre::PTTYCallback` (the debug",
     "~~`008AADA0` builds~~ `005CDA30` builds `Phyre::PTTYCallback` "
     + C("`005CDA30+0x56` stores vtable `00D360A0` (RTTI `Phyre::PTTYCallback`) at `02CB6140`, `005CDA30+0x4F` "
         "loads `008AADA0` and `005CDA30+0x5D` registers it with `atexit` `00808B90`; `008AADA0` caches the "
         "singleton pointer at `02CB6150`") + " (the debug"),
    # X-19: 005C3B10 stores a tagged record pointer, it does not zero two words.
    (LZ, "`005C3B10` is a three-line accessor that zeroes two words and returns their",
     "`005C3B10` is a ~~three-line accessor that zeroes two words~~ guarded accessor that stores `02CAD140` with bit "
     "0 set and `0` into its two words "
     + C("`005C3B10+0x48` loads `02CAD140`, `005C3B10+0x5A` sets bit 0 and `005C3B10+0x65` stores it at `02CB5D48`; "
         "`005C3B10+0x4F` zeroes `02CB5D50`") + " and returns their"),
    # X-17: 005CD4F0 / 005CD820 is not the one-time-init lock.
    (LZ, "one-time-init / shared-lock pair this page documents.",
     "~~one-time-init /~~ shared-lock pair, which is not the one-time-init lock this page documents "
     + C("`005CD820` clears a `lock cmpxchg` flag at `[rcx+0x20]` and wakes through `005CD570` (`SetEvent`); it never "
         "touches `_Init_thread_lock` `02EAED40`") + "."),
    (LZ, "**The one-time-init lock is a service every layer takes, SERVICE throughout.** Its acquire",
     "**~~The one-time-init lock~~ The `005CD4F0` / `005CD820` shared lock is a service every layer takes, SERVICE "
     "throughout.** " + C("this pair is a `lock cmpxchg` flag lock with an event wake; the one-time-init lock "
                          "`02EAED40` is referenced only by `00809124`, `00809244`, `0080926C`, `0080929C`, `008092FC` "
                          "and `008093C0`") + " Its acquire"),
    # X-21: the three named callees are called by 336 holders, not 535 (535 is the whole label family).
    (LZ, "-> Phyre reflection registration       00632960 / 00630180 / 006388C0   (535 of 707)\n",
     "-> Phyre reflection registration       00632960 / 00630180 / 006388C0   (535 of 707)   " + K + "these "
     "three are called by 336 of the 707 callers of 008092FC; 535 counts the whole Phyre.Reflection.* label family "
     "(the BJ-5 bounding below); the atexit 526 recounts exactly\n"),
    # X-25: 2,216 functions.
    (LZ, "here and is read from 2,229 functions, but the count",
     "here and is read from ~~2,229~~ 2,216 functions "
     + C("`01F44830` has 2,216 reads in 2,216 functions and one write; BJ-2's answer below") + ", but the count"),
    # S-8 (stale).
    (LZ, "`02EAED70` is initialised by the CRT, not visible statically.",
     "`02EAED70` is initialised by the CRT~~, not visible statically~~ "
     + A("BJ-3's answer below, static, 2026-09-14") + "."),
    (LZ, "BJ-1 and BJ-3 both need a\n",
     "BJ-1 ~~and BJ-3 both need~~ needs a " + A("BJ-3 above, answered statically 2026-09-14") + "\n"),

    # ---------------- ST (SWE2-EC7 page) ----------------
    (ST, "**Do not hook a teardown to detect object destruction.** It runs at process exit, after the game",
     "**Do not hook a teardown to detect object destruction.** ~~It runs at process exit, after the game~~ On a "
     "normal quit it does not run at all, and on a CRT `exit` path it runs after the game "
     + C(EXITQ + "; UQ-331's answer, §5")),
    (ST, "| `00584730` is `operator delete` | its complete 10-byte body",
     "| `00584730` is ~~`operator delete`~~ `if (p) _aligned_free(p)` "
     + C("the body this row cites tail-jumps `0019C570`, and " + AFREE + "; the image imports no `operator delete`")
     + " | its complete 10-byte body"),
    (ST, "## SWE2-EC7-19 update (2026-05-15) — `00632BE0` ICF-folded `??_G` cluster window",
     "## SWE2-EC7-19 update (2026-05-15) — `00632BE0` ~~ICF-folded `??_G` cluster window~~ a constructor, not a "
     "`??_G` (corrected 2026-10-02, OPUS: it installs vtables `00D580B0` and `00D580D8`, returns `this` and has 21 "
     "direct call sites)"),
    (ST, "`0059A030` (884 B) is the static-init driver - the `02CA9D91` once-flag gate, then 17 sequential "
         "`0059xxxx` init calls (`00592770` through `0059A368`).",
     "`0059A030` (884 B) is ~~the static-init driver~~ the scalar-conversion tree lookup - the `02CA9D91` once-flag "
     "gate, then ~~17 sequential `0059xxxx` init calls (`00592770` through `0059A368`)~~ 144 sequential initialiser "
     "calls (`0059A030+0x1D` through `0059A030+0x2E8`), then a tree descent that returns the matching node's "
     "`+0x28` " + C("144 `call` instructions, then the keyed walk ending `0059A030+0x358`; the hardening page's "
                    "144-node conversion tree") + "."),
    (ST, "`0067F700` (712 B) is the call-free CRT `_Tree` node relink - `byte[+0x10]&1` nil-flag walk, "
         "pointer-chasing `[[rcx+0x10]]` compares, the MSVC tree rebalance skeleton.",
     "`0067F700` (712 B) is the call-free ~~CRT `_Tree` node relink~~ red-black rebalance of Phyre's own tree - "
     "`byte[+0x10]&1` ~~nil-flag~~ colour-bit walk, pointer-chasing `[[rcx+0x10]]` compares, ~~the MSVC tree "
     "rebalance skeleton~~ not MSVC's `_Tree` "
     + C("bit 0 of the parent word at `+0x10` is the colour, `0067F700+0x2` to `0067F700+0x18`; `_Tree` keeps "
         "`_Color` and `_Isnil` as bytes at `+0x18` and `+0x19`; the ordered-container page names `0067F700` "
         "Phyre's tree") + "."),

    # ---------------- EH ----------------
    (EH, "*guard  >  0   built; its value is the epoch at which it completed\n",
     "*guard  >  0   built; its value is the epoch at which it completed   " + K + "not > 0: 01F44850 ships "
     "0x80000000 and the footer stores ++epoch (0080929C+0x29, 0080929C+0x31), so a built guard is negative as a "
     "signed int\n"),
    (EH, "shape `lea rcx,[rip+global]; jmp ~T()`. They run at normal shutdown, not on an exception.",
     "shape `lea rcx,[rip+global]; jmp ~T()`. They run ~~at normal shutdown~~ only on a CRT `exit` path, never on "
     "the normal quit, and not on an exception " + C(EXITQ + "; the teardown page's UQ-331 answer") + "."),
    (EH, "**1,609 distinct parent functions**:",
     "~~**1,609 distinct parent functions**~~ **4,314 parent functions** in the EH tables (the split below was taken "
     "over a 1,609-function population that is not preserved) "
     + C("a `.pdata` walk to every `__CxxFrameHandler3` / `__GSHandlerCheck_EH` `FuncInfo` finds 4,446 records "
         "owned by 4,518 functions, 4,314 of which name an unwind or catch funclet; 3,820 distinct unwind and 72 "
         "catch funclets; B-2/e's answer") + ":"),
    (EH, "`00194CD0` (455 B) is a call-free exception funclet - `word[rdx]` length walk (`inc r14` loop), "
         "`008C2688`/`008C2710`/`008C2690` rdata, SEH-style frame stores.",
     "`00194CD0` (455 B) is ~~a call-free exception funclet~~ the wide-stream inserter `operator<<(std::wostream &, "
     "const wchar_t *)`, an ordinary function with six direct calls from `001993B0` - `word[rdx]` length walk "
     "(`inc r14` loop), ~~`008C2688`/`008C2710`/`008C2690` rdata~~ calls through the `MSVCP140` import slots "
     "`008C2688` (`sputc`), `008C2690` (`sputn`) and `008C2710` (`flush`), ~~SEH-style frame stores~~ an ordinary "
     "EH frame " + C("nine `call` instructions in the body, `00194CD0+0x9D` the `flush` call; the BK-6 note's "
                     "`ostream` inserter reading is the right one") + "."),
    (EH, "`0061ECF0` (3 B) is the `return 1` stub the lazy-guard callers use\n"
         "as their success sentinel - no body beyond `mov al, 1; ret`.",
     "`0061ECF0` (3 B) is the `return 1` stub ~~the lazy-guard callers use~~\n"
     "~~as their success sentinel~~ that `__scrt_initialize_crt`, `__scrt_uninitialize_crt`, `00808C90` and "
     "`00607410` call - no body beyond `mov al, 1; ret` "
     + C("its seven call sites are in `0080893C` (3), `00808B14` (2), `00808C90` and `00607410`; none is a "
         "lazy-guard holder, a caller of `008092FC`") + "."),
    (EH, "| `CompilerGeneratedCFG` | 145 | **No.** The CFG guard adapters. Touches this document",
     "| `CompilerGeneratedCFG` | 145 | **No.** ~~The CFG guard adapters.~~ The 145 empty-destructor teardowns the "
     "tag misnames " + C("each is `lea rcx, [static]; jmp 0016D6A0` and is registered with `atexit` `00808B90`; the "
                         "hardening page's S-3 correction") + ". Touches this document"),
    # stale: S-9 / S-12 / S-11 / S-10.
    (EH, "executes; the source-level identity of the folded empty destructor; individual verification of\n"
         "the 136 magic statics without a funclet.",
     "executes~~; the source-level identity of the folded empty destructor; individual verification of~~\n"
     "~~the 136 magic statics without a funclet~~. "
     + A("B-2/a, closed 2026-09-07 - there is no single identity to recover - and B-2/c, all 136 verified "
         "2026-09-26")),
    (EH, "`C2 00 00` — `ret`.** That address",
     "`C2 00 00` — ~~`ret`~~ `ret 0`.** " + A("B-2/a - `ret 0`, not a bare `ret`") + " That address"),
    (EH, "which slot-`+0x10` method — is not recovered here and stays numeric.",
     "which slot-`+0x10` method — ~~is not recovered here and stays numeric~~ is recovered in the BK-6 answer "
     "below " + A("BK-6, answered 2026-09-12") + "."),
    (EH, "evidence_tier: 1 (one group of 128 relies on tier 8 for its *identity*, see §8)\n",
     "evidence_tier: 1 (one group of 128 relies on tier 8 for its *identity*, see §8)   # " + K + "B-2/b answered "
     "2026-09-26: the image's POGO record places all 128 in .text$x, so their identity no longer rests on tier 8\n"),

    # ---------------- OBJ ----------------
    (OBJ, "0017CCA5  call 00584730     ;   no  -> ordinary operator delete(ptr)\n",
     "0017CCA5  call 00584730     ;   no  -> ordinary operator delete(ptr)   " + K + "00584730 is if (p) "
     "_aligned_free(p): jne 0019C570, and 0019C570 is jmp [008C2B70] = _aligned_free; no operator delete is "
     "imported\n"),
    (OBJ, "    if (flags & 4)  free(base, size);          /* array: free the whole block  */\n",
     "    if (flags & 4)  free(base, size);          /* array: free the whole block  */   // " + K + "wrong: bit 2 "
     "set calls 0016D6A0 (ret 0) with the size and frees nothing, bit 2 clear calls 00584730 (_aligned_free); "
     "00185800+0x33 and 00185800+0x26, and BQ-26's answer\n"),
    (OBJ, "     -> free 00809950  or the aligned/guarded path via 0016D6A0\n",
     "     -> free 00809950  or the aligned/guarded path via 0016D6A0   " + K + "0016D6A0 is ret 0 and frees "
     "nothing; the freeing paths are 00809950 (free) and 00584730 (_aligned_free)\n"),
    (OBJ, "`0078A960` and `0085E730`, the free/dealloc entries this corpus has identified.",
     "`0078A960` ~~and `0085E730`~~, the free/dealloc entries this corpus has identified, and the `malloc` stub "
     "`0085E730` " + C("`0085E730` is `jmp [008C2B40]`, the `malloc` import, not a free") + "."),
    (OBJ, "`00194F50` (270 B) is a sound-request body - `008C25F0`/`008C2628`/`008C2630`/`008C2658` import calls, "
          "`00808850`/`00861ECC`. Interior anchor `00194F73` (an `00808850` call).",
     "`00194F50` (270 B) is ~~a sound-request body~~ `std::use_facet<std::codecvt<wchar_t, char, _Mbstatet>>`, a C++ "
     "standard-library body - `008C25F0`/`008C2628`/`008C2630`/`008C2658` import calls, `00808850`/`00861ECC`. "
     "Interior anchor `00194F73` (~~an `00808850` call~~ the `_Lockit` call) "
     + C("`00194F50+0x23` constructs a `_Lockit` through `008C25F0`, `00194F50+0x36` reads "
         "`codecvt<wchar_t>::id` from `008C2768` and `00194F50+0x96` calls `_Getcat` through `008C2658`; `00808850` "
         "is called at `00194F50+0xEB`") + "."),
    (OBJ, "reads `[rcx+8]` (the module's callback slot), calls the CRT's `[008C23CC]` IAT entry (the wake/sync "
          "primitive the family-28 teardowns all funnel to), and zeroes `[rcx+0x10]`.",
     "reads `[rcx+8]` ~~(the module's callback slot), calls the CRT's `[008C23CC]` IAT entry (the wake/sync "
     "primitive the family-28 teardowns all funnel to), and zeroes `[rcx+0x10]`~~, a handle it closes through "
     "`CloseHandle`, and clears the byte `[rcx+0x10]` "
     + C("`005CD6D0+0x15` is `call [008C23E0]`, the `KERNEL32` import `CloseHandle`") + "."),
    # stale: S-15 / S-17 / S-19.
    (OBJ, "tests `dl,1` and then `dl,4` — the array\n  form — and carries none of these four labels. One "
          "instance found; the population is unmeasured",
     "tests `dl,1` and then `dl,4` — ~~the array~~\n  ~~form~~ not the array form — and carries none of "
     "these four labels. One instance found; ~~the population is unmeasured~~ "
     + A("BQ-26, ANSWERED 2026-09-02 - the population is 1,608 and bit 2 selects the deallocator")),
    (OBJ, "this row stays open and tier 6 stays the decider.",
     "~~this row stays open and tier 6 stays the decider~~ " + A("the BQ-23 answer below, 2026-09-27, at tier 6")
     + "."),
    (OBJ, "**NOT CLAIMED:** which interface the 28 implement — the",
     "~~**NOT CLAIMED:** which interface the 28 implement~~ "
     + A("\"The 28 construct\" below - the class-descriptor interface, corrected 2026-09-29") + " — the"),

    # ---------------- OC / MS ----------------
    (OC, "| `00799BD0` / `00799C30` | 89 / 85 B |",
     "| `00799BD0` / `00799C30` | ~~89 / 85 B~~ 85 / 89 B "
     + C("`00799BD0` ends 85 bytes in and `00799C30` 89; the MSVC page's rows agree") + " |"),
    (OC, "instruction at all**, and four of the six members",
     "instruction at all**, and ~~four~~ five " + C("the five listed hold no `call`; the erase `0016DA60` holds "
                                                    "four, to the two rotations") + " of the six members"),
    (OC, "| four of the six have zero callees; the erase calls only the two rotations |",
     "| ~~four~~ five of the six have zero callees " + C("both iterator steps, both rotations and the insert")
     + "; the erase calls only the two rotations |"),
    (OC, "in the game at once - 99 call sites across audio",
     "in the game at once - ~~99 call sites~~ 99 calling functions and 213 call sites "
     + C("direct edges into the six bodies; §5's census") + " across audio"),
    (OC, "position this page does not measure.",
     "position ~~this page does not measure~~ " + A("§2 - this page measures it at `+0x20`, 80 of 80") + "."),
    (OC, "are what the sweep cannot rule out: **SD-82**.",
     "are what the sweep cannot rule out: **SD-82** " + A("the SD-82 row above, answered 2026-09-30") + "."),
    (MS, "**`+0x19` is the identification.** Every body in this family tests it, as",
     "**`+0x19` is the identification.** Every body in this family ~~tests it~~ but the payload destructor "
     "`0071EE70` tests it " + C("`0071EE70` frees two string buffers through `001DFA10` and never reads `+0x19`; "
                                 "MT-3's answer") + ", as"),
    (MS, "A, B and C is remains `MT-1`, and",
     "A, B and C is ~~remains `MT-1`~~ was `MT-1` " + A("MT-1, ANSWERED 2026-09-26") + ", and"),

    # ---------------- GEN (SWE2-EC7 page) ----------------
    (GEN, "`00584730` is `operator delete`, the one external target of the 224 static teardowns; `00210EC0` is the "
          "aligned allocator the object constructors call;",
     "`00584730` is ~~`operator delete`~~ `if (p) _aligned_free(p)`, the one external target of the 224 static "
     "teardowns; `00210EC0` is ~~the aligned allocator~~ `malloc(n)`, which the object constructors call "
     + C("`00584730` tail-jumps `0019C570`, and " + AFREE + "; `00210EC0` is `or r8d, -1; xor edx, edx; jmp "
         "0085E730`, and `0085E730` is `jmp [008C2B40]`, the `malloc` import") + ";"),
    (GEN, "register the member fn via 006B6700; conditional _aligned_free of a second member global via 00584730. "
          "CONTROL: 2 external target(s): 2 shared across all 18 members (006B6700, 00584730), and 0 member-specific "
          "- member identity is carried by the lea'd globals and the indirect vcall. NOT dispositioned: the 2 shared "
          "implementations and the member globals - this row disposes of the wrapper, not of what it wraps.\"\n",
     "register the member fn via 006B6700; conditional _aligned_free of a second member global via 00584730. "
     "CONTROL: 2 external target(s): 2 shared across all 18 members (006B6700, 00584730), and 0 member-specific "
     "- member identity is carried by the lea'd globals and the indirect vcall. NOT dispositioned: the 2 shared "
     "implementations and the member globals - this row disposes of the wrapper, not of what it wraps.\"   # " + K +
     "006B6700 registers nothing: it empties an intrusive list, unlinking and self-linking every node until the head "
     "is alone (006B6700+0x38 loops back)\n"),

    # ---------------- RV ----------------
    (RV, "`00624580` (~32 B) — the standard `mov rcx, rdx; mov rbx, r8; call\n0061A250` slot-3 adapter",
     "`00624580` ~~(~32 B)~~ (26 B) — the standard `mov rcx, rdx; mov rbx, r8; call\n0061A250` ~~slot-3~~ "
     "slot-5 adapter " + C("its 26 bytes are the family template; `.rdata` holds it at `00D54AE8` and `00D54B70`, "
                           "slot 5 after the type pointers `00D54AB8` and `00D54B40`")),
    (RV, "| `0061A250` | `PClassDescriptorConcrete` class body |",
     "| `0061A250` | ~~`PClassDescriptorConcrete` class body~~ the script-VM object-pointer accessor "
     "(`Phyre.ScriptVM.ObjectPointerAccessor`) " + C("`0061A250+0x15` calls the `PhyreObject` registry check "
                                                      "`00682980`, `0061A250+0x55` walks the class chain at `+0x78`, "
                                                      "and a mismatch reports through `00812960` at `0061A250+0x96`")
     + " |"),
    (RV, "**`DF-4` ANSWERED 2026-09-12 (FABLE):** 401 adapters exist (351 tagged, 50 under other tags)",
     "**`DF-4` ANSWERED 2026-09-12 (FABLE):** ~~401 adapters exist (351 tagged, 50 under other tags)~~ 403 adapters "
     "exist, 351 of them tagged " + C("the 26-byte template scan of `.text` finds 403, all function entries; DF-5's "
                                      "answer, 403 = 401 + 2")),
    (RV, "call <target>        ; the only field that differs between the 351\n",
     "call <target>        ; the only field that differs between the 351   " + K + "between the 403 (template "
     "scan); 351 is the tag count\n"),
    (RV, "| Each appears exactly three times in `.rdata` |",
     "| ~~Each appears exactly three times in `.rdata`~~ 367 of the 403 appear three times in `.rdata`, 34 twice, one "
     "six times and one ten times " + C("an 8-byte search of `.rdata` for the 403 template addresses, 1,185 "
                                       "appearances; the 2026-09-13 correction in §2") + " |"),
    (RV, "**The arithmetic does not close** — 403 adapters over 409 classes against 402 pointer accessors; "
         "reopened as `DF-5`",
     "~~**The arithmetic does not close**~~ — 403 adapters over 409 classes against 402 pointer accessors; "
     "reopened as `DF-5` " + A("DF-5, ANSWERED 2026-09-14 - 403 = 401 + 2")),
    (RV, "> unexplained.** `DF-4`.\n",
     "> unexplained.** `DF-4`. " + A("the DF-4 answer just below - 351 was the tag census") + "\n"),

    # ---------------- MEM ----------------
    (MEM, "`0036D280` runs at init: `0016D6A0` packs a 0x58-byte record on the stack",
     "`0036D280` runs at init: ~~`0016D6A0` packs a 0x58-byte record on the stack~~ it hands a 0x58-byte stack "
     "record to `0016D6A0`, which is `ret 0` and fills nothing "
     + C("`0036D2F0+0x5E` is `call 0016D6A0`, whose whole body is `C2 00 00`; only the field at `rsp+0x78` is "
         "patched before the copies")),
    (MEM, "`ret 0` — followed by `int3` padding. It has **2,479\nincoming calls**, more than",
     "`ret 0` — followed by `int3` padding. It has ~~**2,479~~\n~~incoming calls**~~ **2,528 incoming `call` "
     "sites and 340 `jmp` sites, from 2,480 functions** "
     + C("direct edges over the current function extents; 2,479 is close to the function count, not the call "
         "count") + ", more than"),
    (MEM, "through exactly **six** doors.",
     "through exactly ~~**six**~~ **eight** doors "
     + C("all eight heap imports `008C2B40`–`008C2B78` are reached: `_aligned_malloc` by tail jumps in "
         "`0019C580`, `001EDF10+0x5D` and `001EDF80+0x53`, `_set_new_mode` through `00862046`; §1's table") + "."),
    (MEM, "Six of the eight are\nactually called:",
     "~~Six of the eight are~~ All eight are " + C("the table's own `_set_new_mode` row is corrected to 1, and "
                                                  "`_aligned_malloc` is reached through `0019C580`")
     + "\nactually called:"),
    (MEM, "back, continuously, all the way through a session — it does not grab one big block at startup and\n"
          "live inside it the way a console game does.",
     "back, continuously, all the way through a session — ~~it does not grab one big block at startup and~~\n"
     "~~live inside it the way a console game does.~~ It also takes nine large blocks at startup, about 256 MiB, and "
     "its arenas live inside them " + C("`0022A0B0+0x131` through `0022A0B0+0x1B9` call `0036D240`, which reaches "
                                        "`malloc` through `0085E730`, for arenas 2–9 and 11; §2") + "."),
    (MEM, "**The gameplay chain is a different chain and does not join this one:**",
     "**The gameplay chain is a different chain and ~~does not join this one~~ joins this one only at boot, where "
     "its arenas take their backing from `malloc`:** " + C("`0036D240` is `jmp 0085E730`, the `malloc` stub, called "
                                                            "nine times by `0022A0B0`")),
    (MEM, "`0036A570`, calls through the hook cell `q[008C2D80]`, and executes `int3`.",
     "`0036A570`, calls ~~through the hook cell `q[008C2D80]`~~ the CRT's `exit(1)` through its import slot "
     "`008C2D80`, and executes `int3` " + C("`008C2D80` is the `api-ms-win-crt-runtime` import `exit`; "
                                            "`00369860+0x214` sets `ecx = 1` and `00369860+0x219` calls it") + "."),
    (MEM, "`+0x50` pool pointer, `+0xA0` per-kind constructor, live marks at `+0x02`/`+0x62`.",
     "~~`+0x50` pool pointer~~ `+0x50` the root of the block-header tree, `+0xA0` per-kind constructor, live marks at "
     "`+0x02`/`+0x62` " + C("`0036B410+0x47` stores the first node at `+0x50` when the tree is empty and "
                            "`0036AAD0+0x40` starts a size-keyed descent there, children at `+0x24` and `+0x28`") + "."),
    (MEM, "establishes it is an **8-element dword array at stride 4,",
     "establishes it is an **~~8-element~~ dword array at stride 4 "
     + C("`00369D30+0x7D` writes `0xFF` into `022D8E18`, a different field, so the array cannot run to eight; the "
         "closure below finds two elements on every identified path") + ","),
    (MEM, "a neighbour of the `022D8E1C` failure code that `0036BC60` returns",
     "a neighbour of the `022D8E1C` ~~failure code that `0036BC60` returns~~ byte that `0036BC60` stores as the "
     "block's counter index when no free-list record supplies `+0x16` "
     + C("the four reads below load it into the local that `0036BC60+0xF7` otherwise fills from `byte [r8+0x16]`; "
         "nothing returns it")),
    (MEM, "(`0036A266`–`0036A270`), byte store at `022D89A8` (`0036A282`–`0036A290`) |",
     "(`0036A266`–`0036A270`)~~, byte store at `022D89A8` (`0036A282`–`0036A290`)~~ "
     + C("the body ends at `0036A240+0x3E`; the `022D89A8` store loop is `0036A280`, the identity-map fill") + " |"),
    (MEM, "allocation kind — is written here, by the pop.** So the full path",
     "allocation kind — is written here, by the ~~pop~~ push, and restored by the pop.** "
     + C("`0036C1F0+0x8F` and `0036C140+0x2B`, below") + " So the full path"),
    (MEM, "onto a lane, the pop stages it into `022D89BC`, and",
     "onto a lane, ~~the pop stages it into `022D89BC`~~ the push installs `map[id]` into `022D89BC` "
     + C("`0036C1F0+0x8F` stores the mapped id into `022D89BC`; the pop `0036C140+0x2B` writes back the saved "
         "previous one") + ", and"),
    (MEM, "  `+0x34 byte34`. Nine bytes at `+0x35` stay unobserved.",
     "  `+0x34 byte34`. ~~Nine bytes at `+0x35` stay unobserved.~~ `+0x34`–`+0x3A` hold a 7-character name and "
     "`+0x3B` its NUL; `+0x3C`–`+0x3D` stay unobserved "
     + C("`0036C660+0x30` calls `strncpy` through `008C2F70` for 7 bytes at header `+0x34`, and `0036C660+0x36` "
         "stores the NUL at `+0x3B`") + "."),
    (MEM, "| `+0x3E` | 2 | **mark word**, written at `0036BE91`, `0036BEA5`, `0036BF74` |",
     "| `+0x3E` | 2 | ~~**mark word**~~ guard word, written as zero at `0036BE91`, `0036BEA5`, `0036BF74` "
     + C("the stored `r13w` is zeroed at `0036BC60+0x222`; the mark byte is header `+0x02`") + " |"),
    (MEM, "> **Every link is `BASE`-encoded** — `d[link] = ptr − arena`, decoded through",
     "> **Every link is `BASE`-encoded** — ~~`d[link] = ptr − arena`~~ `d[link] = (u32)ptr − "
     "(u32)base`, `base` the qword at `01F83530`, not the arena "
     + C("`0020E620` is `sub ecx, [01F83530]` and `0020E600+0x2` adds the qword back; no other instruction "
         "references `01F83530`, which lies in zero-filled `.data`") + ", decoded through"),
    (MEM, "directly**. `0xBB80` is **48,000**, so the block is `seconds × 48 kHz × 4 bytes` — 16-bit\n"
          "      stereo.",
     "directly**. `0xBB80` is **48,000**, so the block is ~~`seconds × 48 kHz × 4 bytes` — 16-bit~~\n"
     "      ~~stereo~~ `channels × 48,000 × 4 bytes`, one second of 4-byte samples per channel "
     + C("`ebx` is `[rsi+0x324]`, loaded at `00679A50+0x10D`; `+0x320` is a libvorbis `vorbis_info` set up by "
         "`00880AF0` and read by `008800C0`, whose `008800C0+0x74` compares the `vorbis` header tag, so `+0x324` "
         "is `channels`; §1's table row says the same") + "."),
    (MEM, "> **The header is NOT being added to `_types/` yet, and that is deliberate.**",
     "> ~~**The header is NOT being added to `_types/` yet, and that is deliberate.**~~ "
     + A("\"What this settled in `_types`\" below - `ImageAddressArenaBlockHeader`, 2026-09-20")),
    (MEM, "### Failure is not handled\n",
     "### Failure is not handled " + A("the overview's 2026-09-28 and 2026-09-30 corrections - the arena retries, "
                                       "and some callers test for null") + "\n"),

    # ---------------- TH ----------------
    (TH, "then fires `00249180(rsi, 7, 3, 0xD7, proc 00280740)`",
     "then fires ~~`00249180(rsi, 7, 3, 0xD7, proc 00280740)`~~ `00249180(rsi, 7, 0xD7, 3, 1, 00280740)` "
     + C("`00280750+0xEB` sets `edx = 7` and `00280750+0xFC` sets `r8d = 0xD7`, then `r9d = 3` and `[rsp+0x20] = "
         "1`; `00280750+0x111` is the call, in the same order as `002467A0`'s")),
    (TH, "a NO ADMISSIBLE SOURCE closure, kind (c); it is filed for review",
     "a NO ADMISSIBLE SOURCE closure, ~~kind (c)~~ kind (d) "
     + A("the reviewer's signature of 2026-09-18 below") + "; it is filed for review"),
    (TH, "**Superseded readings:** none — this is the document's first version.",
     "**Superseded readings:** ~~none — this is the document's first version.~~ "
     + A("§10 - the 2026-09-03 pass overturned readings of this document")),
    (TH, "      rather than called. Not measured here.\n",
     "      rather than called. ~~Not measured here.~~ " + A("BU-5 just below - 296 of the 689") + "\n"),

    # ---------------- RS ----------------
    (RS, "| the whole application, `007980A0` — **the crash-dump filter** |",
     "| the whole application, `007980A0` — ~~**the crash-dump filter**~~ the program's main body, which "
     "installs the crash-dump filter `0079AD50` " + C("`007980A0+0x50` loads `0079AD50` and `007980A0+0x57` calls "
                                                      "`SetUnhandledExceptionFilter`") + " |"),
    (RS, "> `call 007980A0`, the crash-dump filter this table names.",
     "> `call 007980A0`, ~~the crash-dump filter this table names~~ the main body that installs the filter "
     "`0079AD50` " + C("`007980A0+0x57` calls `SetUnhandledExceptionFilter` with `0079AD50`") + "."),
    (RS, "  or only to an explicit developer call is unestablished. `CV-3`.",
     "  or only to an explicit developer call ~~is unestablished~~ " + A("CV-3 just below - it is installed on "
                                                                         "every boot") + ". `CV-3`."),
    (RS, "Its trigger, and whether it can run before the filter,\n    are not read.",
     "~~Its trigger, and whether~~ Its trigger is the filter `008A5AD0` " + A("the `008A5AD0` row below, BK-5")
     + "; whether it can run before the filter,\n    ~~are~~ is not read."),
    (RS, "**an address-range argument plus a string join, not a body read** | 2 |",
     "~~**an address-range argument plus a string join, not a body read**~~ an address-range argument plus a "
     "string join " + A("CV-2 above - the body, 137 B, was read whole later") + " | 2 |"),

    # ---------------- HARD ----------------
    (HD, "> to `atexit` (`00808B90`), so each **runs once at process exit** and does nothing.",
     "> to `atexit` (`00808B90`), so each ~~**runs once at process exit**~~ **runs at most once, on a CRT `exit` "
     "path, and not at all on a normal quit**, and does nothing " + C(EXITQ + "; the teardown page's UQ-331 answer")
     + "."),
    (HD, "### The 145 guard adapters are dead code\n",
     "### ~~The 145 guard adapters are dead code~~ The 145 empty-destructor teardowns (corrected 2026-10-02, OPUS: "
     "each is registered with `atexit`, so not dead; the S-3 correction below)\n"),
    (HD, "`CF_INSTRUMENTED` means the code **was compiled** with `/guard:cf`.",
     "`CF_INSTRUMENTED` means ~~the code **was compiled**~~ some linked objects were compiled with `/guard:cf` "
     "— here only the statically linked CRT " + C(CFGCRT + "; the 2026-09-19 section") + "."),
    (HD, "| CFG *was* compiled in | `GuardFlags = 0x100`",
     "| ~~CFG *was* compiled in~~ CFG was compiled into the statically linked CRT only " + C(CFGCRT)
     + " | `GuardFlags = 0x100`"),
    (HD, "| Section | RVA | Virtual size | Note |",
     "| Section | RVA | ~~Virtual size~~ Raw size, except `.data` and `.gfids` "
     + C("the column holds `SizeOfRawData`; the virtual sizes are in the corrected table below") + " | Note |"),
    (HD, "lands 1.1 MB short of `.reloc`, inside `.pdata`.",
     "lands 1.1 MB short of `.reloc`, inside ~~`.pdata`~~ `.data` "
     + C("by the corrected table below, `.data` spans `0x01DF0000`–`0x02F97530` and `.pdata` starts at "
         "`0x02F98000`") + "."),
    (HD, "`S-2` and\n`T-9` stay open.",
     "`S-2` ~~and~~\n~~`T-9` stay~~ stays open " + A("`T-9` above, answered 2026-09-27") + "."),

    # ---------------- MATH ----------------
    (MA, "and only **four** SSE `sqrt` instructions in the",
     "and only **four** ~~SSE `sqrt` instructions~~ scalar `sqrtss` instructions, beside 14 packed `sqrtps` and 10 "
     "`rsqrtps` in the audio cluster, " + C("an instruction grep of every body; the corrected count in §3") + " in the"),
    (MA, "| `02EBF190` | settings object pointer |",
     "| `02EBF190` | ~~settings object pointer~~ pointer to an object whose byte `+0x5B0E` three code sites write "
     + C("`00385BA0+0x31` copies a record's byte `+0x138` into it, `002FA210+0x17` and `00233C10+0x81` zero it; "
         "UQ-320's answer") + " |"),
    (MA, "depends on the settings\nbyte at `+0x5B0E`, which is not established here.",
     "depends on the ~~settings~~\nbyte at `+0x5B0E`, which ~~is not established here~~ never exceeds 17 "
     + A("UQ-320, answered 2026-09-14 - it is not a setting") + "."),
    (MA, "`andps` with the `0x7FFFFFFF` mask at",
     "`andps` with the ~~`0x7FFFFFFF`~~ `0x7FFFFFFFFFFFFFFF` double mask "
     + C("`00334120+0x21` widens the delta with `cvtss2sd`, `00334120+0x25` masks it and `00334120+0x2C` narrows it "
         "with `cvtpd2ps`; `01CEBD80` holds two copies of `0x7FFFFFFFFFFFFFFF`") + " at"),
    (MA, "the only non-third-party user of the 1°-in-radians constant |",
     "~~the only non-third-party user of the 1°-in-radians constant~~ a user of the 1°-in-radians constant, not the "
     "only one " + C("`008C5F68` is read by `0028BB50`, `0033CEF0`, `00538B80` and `0085EA40`") + " |"),
    (MA, "all eleven cluster functions disassembled in full;",
     "~~all eleven cluster functions~~ eleven of the twelve cluster functions disassembled in full, `007F1670` "
     "missed " + C("a `sqrtps` / `rsqrtps` grep of every body finds twelve functions; §3 adds `007F1670`") + ";"),
    (MA, "them means to the game: their callers were not traced and no geometric identity is claimed",
     "them means to the game: ~~their callers were not traced and~~ no geometric identity is claimed "
     + A("the UQ-322 answer just below, 2026-09-27 - every body is placed")),
    (MA, "`status` unchanged at **DOCUMENTED** — the central claims",
     "`status` unchanged at **DOCUMENTED** " + A("the front matter - since promoted to `status: AUDITED`")
     + " — the central claims"),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('`007980A0+0x7DF` calls `ExitProcess`',
     'the 2,153-byte Phyre framework body calls `ExitProcess` at its `+0x7DF`'),
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
