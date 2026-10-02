"""apply_00engine_a.py [--apply] - 00-Engine-Core-Runtime readiness map (cloud-reports/re-readiness/00-engine.md),
section 3.1 value-changing items C-V1 to C-V82 (report lines 1835-2350, part A), settled on the pages (OPUS, 2026-10-02).

Each edit strikes the side the shipping image REFUTES and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* with
the deciding instruction as entry+offset. The verdicts and deciding addresses are in the scratch file
verdicts-00a.md (en00a). Items whose sides both hold, or that the image cannot decide, get no edit:
C-V4 (left: census over 102 console arms not re-run), C-V8, C-V9, C-V15, C-V16, C-V28, C-V44, C-V49, C-V50, C-V52,
C-V64, C-V68, C-V69, C-V72, C-V77, C-V79, C-V80.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`<- corrected` comment instead of a strike (their OLD includes the line end, so NEW never contains OLD). No front-matter
edits. One heading changes (C-GATE "All seven children censused"), and it names OPUS. Stale / banner items (section
3.2) are part B's.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "00-Engine-Core-Runtime/"
BOOT = F + "what-the-engine-fixes-at-boot.md"
CBOOT = F + "CONTRACT-boot-fixups.md"
FLOAT = F + "Startup-Data-Construction/generated-float-table-builders.md"
APP = F + "Application-Root/game-application.md"
TICK = F + "Battle-Frame/the-world-tick-and-the-field-frame.md"
FORCE = F + "Force-Fight-Mode/force-fight-mode.md"
GATE = F + "Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md"
CGATE = F + "CONTRACT-per-frame-update-gate.md"
STOP_C = F + "System-Stop-Registry/CONTRACT-system-stop-registry.md"
MODE = F + "Battle-Runtime-Mode/battle-runtime-mode-ladder.md"
CMODE = F + "Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md"
LOG = F + "Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md"
EID = F + "the-encoded-id-space-and-the-query-record.md"
CLS = F + "the-encoded-id-class-registry.md"
BASIS = F + "the-basis-column-helpers.md"
RTTI = F + "Object-Model/rtti-vtable-object-model.md"
HUBS = F + "Shared-State-Accessors/cross-subsystem-accessor-hubs.md"
NBR = F + "Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md"
TUNES = F + "Developer-Tuning-Console/what-the-console-tunes.md"
EVSLOT = F + "Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md"

C = "*(corrected 2026-10-02, OPUS: "
NOOP = "`0016D6A0` is `ret 0`, three bytes"
POS = ("`00265020` is the actor world-position getter: it copies three dwords from `[actor+0xB8]` to its three out "
       "pointers, `00265020+0x1A`–`+0x2E`; the force-fight flag reader is `00253B90`, `[01E0C2B8] == 0`")
SING = "thirteen singleton getters — twelve 8-byte qword getters plus the byte getter `001E05E0` — BE-6"

EDITS = [
    # C-V1: 0016D6A0 is `ret 0` (3 bytes, 2,868 direct call sites) - no release, free or report.
    (TICK, "is the commit/notify tail; `0016D6A0` is the string-member release.",
     "is the commit/notify tail; ~~`0016D6A0` is the string-member release.~~ the call to `0016D6A0` does nothing "
     + C + NOOP + ")*."),
    (TICK, "+ `0016D6A0` free + `002EA6A0`/`0037B4D0`)",
     "+ ~~`0016D6A0` free~~ `0016D6A0`, a `ret 0` stub " + C + NOOP + ")* + `002EA6A0`/`0037B4D0`)"),
    (RTTI, "`+0x18` - each allocation\nimmediately handed back to\n`0016D6A0` on the same\nallocator object - then",
     "`+0x18` - each allocation\n~~immediately handed back to~~\n~~`0016D6A0` on the same~~\n~~allocator object~~ "
     "kept: the call that follows each one, `0016D6A0(allocator, block)` at `00864210+0x35`/`+0x56`/`+0x77`, does "
     "nothing " + C + NOOP + ", so no block is released)* - then"),
    (EID, "`0057CF20` and `0057D620` call: `ecx\n> 0xB` reports `0016D6A0(0x200)` and\nclamps the index to 0",
     "`0057CF20` and `0057D620` call: `ecx\n> 0xB` ~~reports `0016D6A0(0x200)`~~ calls the `ret 0` stub `0016D6A0` "
     "with `0x200`, which reports nothing " + C + NOOP + ")*, and\nclamps the index to 0"),

    # C-V2: 001EC560 answers 1 only when 00265680() returns 0 (001EC560+0x20 call, +0x25 test, +0x2A je).
    (TICK, "`01F832B0` is set, and `00265680()` holds* — the same marker",
     "`01F832B0` is set, and ~~`00265680()` holds~~ `00265680()` answers zero* " + C + "`001EC560+0x20` "
     "`call 00265680`, `+0x25` `test eax, eax`, `+0x27` `lea eax, [rbx+1]`, `+0x2A` `je` — 1 only when it returned "
     "0)* — the same marker"),
    (EVSLOT, "| `001EC560` | pending probe | 59 B | `01F832B0[marker] != 0` and `00265680()` |",
     "| `001EC560` | pending probe | 59 B | `01F832B0[marker] != 0` and ~~`00265680()`~~ `00265680() == 0` "
     + C + "`001EC560+0x25`–`+0x2A`, `test eax, eax` then `je` to the 1 result)* |"),

    # C-V3: 00265020 is Actor_GetWorldPosition, not the force-fight / console getter.
    (FORCE, "Economy` (`002FB150`, `00312280`, 2) and `Audio` (`00362850`, 1). The force-fight getter is\n"
            "read wherever the mode matters — spawn, rewards, audio — which is what a mode flag is for.)*",
     "Economy` (`002FB150`, `00312280`, 2) and `Audio` (`00362850`, 1). ~~The force-fight getter is~~\n"
     "~~read wherever the mode matters — spawn, rewards, audio — which is what a mode flag is for.~~ These readers "
     "fetch an actor's position, not the mode " + C + POS + ").)*"),
    (TUNES, "`00265020` — the console-side fetch the arms share — is called from",
     "`00265020` — ~~the console-side fetch the arms share~~ the actor world-position getter " + C + POS + ")* — is "
     "called from"),

    # C-V5 / C-V6: boot code blocks.
    (BOOT, "                                     0022A28B  0x0100000 -> (not stored here)\n",
     "                                     0022A28B  0x0100000 -> (not stored here)   <- corrected 2026-10-02, OPUS - "
     "stored: 0022A0B0+0x1F3 mov [01FD4A90], rax, after the call at 0022A0B0+0x1DB\n"),
    (BOOT, "002648..  func_0x00379CF0(0x11B9);      // through a 5-byte thunk -> 00863D30\n",
     "002648..  func_0x00379CF0(0x11B9);      // through a 5-byte thunk -> 00863D30   <- corrected 2026-10-02, OPUS - "
     "the call is at 0022A0B0+0x360 (mov ecx, 0x11B9 at +0x35B), not 002648..; the thunk's only callers are "
     "0022A0B0+0x360 and 00584210+0x1C3\n"),

    # C-V7: 0017D000 calls 0017D4C0 first (+0x1F), then allocates 0x80 (+0x29).
    (APP, "`0017D000` itself allocates an `0x80` record into `[01F7E340]`, then calls three bodies before",
     "`0017D000` itself ~~allocates an `0x80` record into `[01F7E340]`, then calls three bodies before~~ calls "
     "`0017D4C0` first, then allocates an `0x80` record into `[01F7E340]` and constructs it with `0018A840`, then "
     "calls `00189000`, before " + C + "`0017D000+0x1F` `call 0017D4C0`, `+0x29` `call 00210EC0` with `ecx = 0x80`, "
     "`+0x3B` `call 0018A840`, `+0x6F` `call 00189000`)*"),

    # C-V10: 001C0D40 allocates unconditionally (+0xF cmp/+0x16 sete feed the 0016D6A0 stub; +0x23 alloc).
    (APP, "| the shared shape `cmp [G],0 → jne done → alloc → ctor → store [G]`: lazy-create for one global each —",
     "| the shared shape `cmp [G],0 → jne done → alloc → ctor → store [G]`: lazy-create for one global ~~each~~ "
     "each but `001C0D40`, which branches on nothing: it passes `[01F81258] == 0` to the `0016D6A0` stub and then always "
     "allocates `0x1B8` and stores the result " + C + "`001C0D40+0xF` `cmp`, `+0x16` `sete cl`, `+0x19` `call 0016D6A0`, "
     "`+0x23` `call 00210EC0`, `+0x3B` the store)* —"),

    # C-V11: 0017D6E0 has 37 distinct callees; 13 are singleton getters (12 qword getters + 001E05E0).
    (APP, "       +-> 37 callees: 16 are 8-10 byte singleton getters, each followed by a\n",
     "       +-> 37 callees: 16 are 8-10 byte singleton getters, each followed by a   <- corrected 2026-10-02, OPUS - "
     "13 are singleton getters (12 qword getters + the byte getter 001E05E0); 14 callees are 8-10 B, 001A1460 is a "
     "member read\n"),
    (APP, "names, and it is enough to identify the pattern the other fifteen follow.",
     "names, and it is enough to identify the pattern the other ~~fifteen~~ twelve follow " + C + SING + ")*."),
    (APP, "on all three of its paths. That function has **37 callees, 16 of them 8-10 byte singleton\n      getters**",
     "on all three of its paths. That function has **37 callees, ~~16 of them 8-10 byte singleton~~ 13 of them "
     "singleton\n      getters** " + C + SING + ")*"),
    (APP, "has **37 callees of which 16 are 8-10 byte accessors**,",
     "has **37 callees of which ~~16 are 8-10 byte accessors~~ 13 are singleton getters** " + C + SING + ")*,"),

    # C-V12 / C-V13: the two hubs' pair counts (lea rcx + call/jmp), counted over each body.
    (CBOOT, "46 straight `lea rcx, 02AE9xxx`/`02AEAxxx`/`02AEBxxx`/`02AECxxx` globals each handed to a "
            "`004C2040`/`004Dxxxx`/`004Exxxx`/`004Fxxxx` initializer, with a lone `jmp 004C3610`",
     "~~46 straight `lea rcx, 02AE9xxx`/`02AEAxxx`/`02AEBxxx`/`02AECxxx` globals each handed to a "
     "`004C2040`/`004Dxxxx`/`004Exxxx`/`004Fxxxx` initializer~~ 49 `lea rcx` globals from `02AE8620` to `02AED330`, "
     "48 of them handed by `call` to an initializer (47 distinct, `004E3110` twice; `002EFF50`, `002F0110` and six "
     "`0047xxxx` bodies among them) " + C + "counted over all 596 bytes of `0037E0F0`)*, the last with a lone "
     "`jmp 004C3610`"),
    (CBOOT, "thirty `lea rcx, 02ADExxx/02AExxxx` + `call` pairs run",
     "~~thirty~~ 28 `lea rcx, 02ADExxx/02AExxxx` + `call` pairs — 27 calls to distinct bodies and the tail "
     "`jmp 004A8860` at `0037DF90+0x153` " + C + "counted over all 344 bytes of `0037DF90`)* — run"),

    # C-V14: the next data pointer after 02AE8900 is 02AE8BE0 (0037E0F0+0x124 lea, call 0047A800).
    (FLOAT, "| `02AE8900` | `004F4F80` | `0x2E0` | `0x530` | |",
     "| `02AE8900` | `004F4F80` | `0x2E0` | ~~`0x530`~~ `0x2E0` | **exact** against `02AE8BE0`, the next data pointer, "
     "which `0037E0F0+0x124` hands to `0047A800` below the band; `0x530` is the gap to the next in-band pointer "
     "`02AE8E30` " + C + "not counted in the nine above)* |"),

    # C-V17: 001EDDA0 reads 01DFE0C0 and 01F82E38.
    (TICK, "`dword[01FCE0C0] != 0` **or** `dword[0209DE38] == 0`; equivalently",
     "~~`dword[01FCE0C0] != 0` **or** `dword[0209DE38] == 0`~~ `dword[01DFE0C0] != 0` **or** "
     "`dword[01F82E38] == 0` " + C + "`001EDDA0+0x0` `cmp [01DFE0C0], 0`, `+0x9` `cmp [01F82E38], 0`)*; equivalently"),

    # C-V18: 003DF760's displacements are image-base relative (rdx = 00120000).
    (TICK, "selects parallel arrays — `qword[0x2A39C40 + i*8] = r9`,\n"
           "`qword[0x2A39C80 + i*8] = stack arg`, `dword[0x2A39CC0 + i*4] = r8d`,\n"
           "`dword[0x2A39CE0 + i*4] = ecx` ([`003DF76F`](../../_index/ADDRESS-INDEX.md)).",
     "selects parallel arrays — ~~`qword[0x2A39C40 + i*8] = r9`,~~ `qword[02B59C40 + i*8] = r9`,\n"
     "~~`qword[0x2A39C80 + i*8] = stack arg`, `dword[0x2A39CC0 + i*4] = r8d`,~~ `qword[02B59C80 + i*8] = stack arg`, "
     "`dword[02B59CC0 + i*4] = r8d`,\n"
     "~~`dword[0x2A39CE0 + i*4] = ecx`~~ `dword[02B59CE0 + i*4] = ecx` " + C + "the displacements are image-base "
     "relative, `003DF760+0x8` `lea rdx, [00120000]`)* ([`003DF76F`](../../_index/ADDRESS-INDEX.md))."),

    # C-V19: the skip pending/active masks are 022CB9C0 / 022CB9D8 (image-base relative displacements).
    (TICK, "`0x21AB9C0`/`0x21AB9D8` dword tables, `022CB732`",
     "~~`0x21AB9C0`/`0x21AB9D8`~~ `022CB9C0`/`022CB9D8` dword tables " + C + "image-base relative, "
     "`003605A0+0x1A` `lea rcx, [00120000]`)*, `022CB732`"),
    (TICK, "that ANDs `~(1<<n)` out of the two `02CDC4xx`-region dword masks at\n`+0x21AB9C0`/`+0x21AB9D8` per slot,",
     "that ANDs `~(1<<n)` out of the two ~~`02CDC4xx`-region~~ dword masks at\n~~`+0x21AB9C0`/`+0x21AB9D8`~~ "
     "`022CB9C0`/`022CB9D8` " + C + "image-base relative, `003604D0+0x23` `lea r15, [00120000]`)* per slot,"),

    # C-V20: 00360710 is 360 B over 16-byte entries (shl rdi, 4).
    (TICK, "`00360710` (64 B) — an 8-byte-element range bound: `rsi =",
     "`00360710` ~~(64 B) — an 8-byte-element range bound~~ (360 B, `ret` at `00360710+0x167`) " + C + "measured)* — "
     "a 16-byte-entry index: `rsi ="),
    (TICK, "(`00360728`); else `rdi = r14 + rsi*8` over the `022CB730` array",
     "(`00360728`); else ~~`rdi = r14 + rsi*8` over the `022CB730` array~~ `rdi = 022CB730 + (r14 + rsi*8) × 16`, a "
     "16-byte entry " + C + "`00360710+0x3B` `lea rdi, [r14+rsi*8]`, `+0x41` `shl rdi, 4`, `+0x45` `add rdi, rax`)*"),

    # C-V21: 00467730 bounds against dword[02EBB6E0] and indexes 0x50-byte records at *02EBB6F0.
    (TICK, "`ecx` bounds-checks against `dword[01EAB6D8]`, selects the x80 record\nin `01EAB6E0`, and",
     "`ecx` bounds-checks against ~~`dword[01EAB6D8]`, selects the x80 record~~ `dword[02EBB6E0]`, selects the "
     "`0x50`-byte record\n~~in `01EAB6E0`~~ at `*02EBB6F0` " + C + "`00467730+0x4` `cmp ecx, [02EBB6E0]`, "
     "`+0xC`–`+0x17` index × `0x50` + `[02EBB6F0]`)*, and"),

    # C-V22: the loader state is 022C51C0.
    (TICK, "re-polls `[020C51C0]` and",
     "re-polls ~~`[020C51C0]`~~ `[022C51C0]` " + C + "`0032E520+0x48` `cmp qword [022C51C0], 0`)* and"),
    (TICK, "returns `([020C51C0] != 0) | !0046DFE0()`.",
     "returns ~~`([020C51C0] != 0) | !0046DFE0()`~~ `([022C51C0] != 0) or !0046DFE0()` " + C + "`0032E520+0x16` "
     "reads `022C51C0`)*."),

    # C-V23: 00267360 indexes 02098E10.
    (TICK, "indexes the `0x288`-stride table at `0209BE10`, and when",
     "indexes the `0x288`-stride table at ~~`0209BE10`~~ `02098E10` " + C + "`00267360+0xA` `lea rax, [02098E10]`)*, "
     "and when"),

    # C-V24: 0022A580's seven-entry table: 2 and >6 -> 0022A770, 3 -> 0022B8C0, 5 -> 0022BC20.
    (CMODE, "state arms `0022B8C0` (2),\n       `0022BC20` (3), `0022A770` (>6)",
     "state arms `0022B8C0` (~~2~~ 3),\n       `0022BC20` (~~3~~ 5), `0022A770` (2 and >6) " + C + "the seven-entry table "
     "`0022A580+0x119` reads sends 2 and anything above 6 to `0022A770`, 3 to `0022B8C0` and 5 to `0022BC20`)*"),

    # C-V25 / C-V26 / C-V27: extents.
    (TICK, "`00234520` (~220 B) — 64-aligned stack frame;",
     "`00234520` ~~(~220 B)~~ (109 B, `ret` at `00234520+0x6C`) " + C + "measured)* — 64-aligned stack frame;"),
    (TICK, "`00265A20` (`ActorSystem_BindBattleUnitsForEligibleRecords`, ~200 B) —",
     "`00265A20` (`ActorSystem_BindBattleUnitsForEligibleRecords`~~, ~200 B~~, 320 B) " + C + "`ret` at "
     "`00265A20+0x13F`)* —"),
    (TICK, "`0022BC20` (~80 B) — `0016D6A0(3)`,",
     "`0022BC20` ~~(~80 B)~~ (463 B, through the tick call at `0022BC20+0xA8`) " + C + "measured)* — `0016D6A0(3)`,"),

    # C-V29: 0036DE70 stores the constant 4 (r15d = ebx + 4 computed once while ebx = 0).
    (TICK, "set, it stores `bx+4` into `word[+4]` then runs",
     "set, it stores ~~`bx+4`~~ the constant 4 " + C + "`r15d = ebx + 4` is computed once at `0036DE70+0x32`, before the "
     "loop, while `ebx` is 0; `0036DE70+0x78` `mov word [rdi+4], r15w`)* into `word[+4]` then runs"),

    # C-V30: 003DEE10's slots start at 02B59360.
    (TICK, "      `02B58960 + m × 8 × 0x38`, by state",
     "      ~~`02B58960 + m × 8 × 0x38`~~ `02B59360 + m × 8 × 0x38` " + C + "`003DEE10+0x37` `lea rcx, [02B59360]`, "
     "`+0x59` `imul rbx, rax, 0x38`)*, by state"),

    # C-V45: 00226280's loop is the AND over the 28 stop records (SS-1), not a best-fit search.
    (TICK, "walks a packed table rooted at `01FD4410` with `ebp = 0x3FF` as the\n"
           "element mask and `0x20000000000` as a validity bit, tracking the minimum slot dword in `ecx`\n"
           "(`cmp ecx,edx` / `cmov` shape at `002262F4`–`00226301`) — a best-fit/free-slot search over a\n"
           "1024-entry index space, not a linear lookup.",
     "walks ~~a packed table~~ the 28 `0x18`-byte stop records rooted at `01FD4410` ~~with `ebp = 0x3FF` as the~~\n"
     "~~element mask and `0x20000000000` as a validity bit~~ (ANDing record A's first qword into `rdi` and record B's "
     "into `rbx`, and setting bit 41, `0x20000000000`, in record B), tracking the minimum slot dword in `ecx`\n"
     "(`cmp ecx,edx` / `cmov` shape at `002262F4`–`00226301`) — ~~a best-fit/free-slot search over a~~ an AND over all "
     "28 slots\n"
     "~~1024-entry index space, not a linear lookup.~~ " + C + "`00226280+0x57` `lea rax, [01FD4410]`, `+0x64`/`+0x6B` "
     "the two ANDs, `+0x8E`–`+0x95` stride `0x18` up to `01FD46B0`; `ebp = 0x3FF` seeds the mask built after the loop; "
     "CONTRACT-system-stop-registry.md SS-1)*"),

    # C-V61 (TICK part): 00304440 is 345 B.
    (TICK, "`00304440` (~27 B) — `byte[02EBF190 + 0x5AE0] & 1` gate, then",
     "`00304440` ~~(~27 B)~~ (345 B, `ret` at `00304440+0x158`) " + C + "measured)* — `byte[02EBF190 + 0x5AE0] & 1` "
     "gate, then"),

    # C-V31: the enable word is read as a dword (8 test dword sites), shipped FF FF FF FF.
    (GATE, "**A single 16-bit word decides, every frame,",
     "**A single ~~16-bit~~ 32-bit word " + C + "eight of its sixteen tests are `test dword`, e.g. `0028E290+0x16F`, and "
     "it ships `FF FF FF FF`; only its low sixteen bits are tested)* decides, every frame,"),
    (CGATE, "One 16-bit word at `01E0C464` decides which subsystems tick,",
     "One ~~16-bit~~ 32-bit word " + C + "eight `test dword` sites, e.g. `0028E290+0x16F`; the `uint32` row of §2)* at "
     "`01E0C464` decides which subsystems tick,"),
    (CGATE, "| read | the enable word at `01E0C464`, sixteen bits, every frame |",
     "| read | the enable word at `01E0C464`, ~~sixteen bits~~ a dword whose low sixteen bits are tested " + C
     + "`0028E290+0x16F` `test dword`)*, every frame |"),

    # C-V32: 8 test byte + 8 test dword.
    (GATE, "| 16 `test byte [01E0C464], imm` sites in `0028E290`, all the same global |",
     "| 16 ~~`test byte [01E0C464], imm`~~ `test [01E0C464], imm` sites, 8 `test byte` for the masks below `0x100` "
     "and 8 `test dword` for `0x100`–`0x8000` " + C + "`0028E290+0x4` to `+0x1C0` byte, `+0x16F` to `+0x2BE` "
     "dword)*, in `0028E290`, all the same global |"),
    (GATE, "    test byte [01E0C464], <mask>   x15\n",
     "    test byte [01E0C464], <mask>   x15   <- corrected 2026-10-02, OPUS - 16 tests: 8 test byte (masks below "
     "0x100) and 8 test dword (0x100-0x8000), 0028E290+0x4 to +0x2BE\n"),

    # C-V33 / C-V34: FramePump takes an argument and the handlers take pointer arguments.
    (CGATE, "void FramePump(void) {                      /* 0028E290 */\n",
     "void FramePump(void) {                      /* 0028E290 */   // <- corrected 2026-10-02, OPUS - one argument "
     "(word[01E0C2B0], 0028E290+0x10 mov edi, ecx), and the handlers take a pointer, e.g. rcx = [0209BE80] + 0x5380 for "
     "00289970 (0028E290+0x14 to +0x22)\n"),
    (CGATE, "    if (en & 0x0002) Group_00291B90();      /* same bit, second group */\n",
     "    if (en & 0x0002) Group_00291B90();      /* same bit, second group */   // <- corrected 2026-10-02, OPUS - "
     "and only when (arg & 1): 0028E290+0x127 test dil, 1\n"),

    # C-V35: word[01E0C2B0] has two writers (00253970+0x75 with 0xF, 002547C0+0x0 with the caller's cx).
    (CGATE, "`word[01E0C2B0]`, written once at\n  `002539E5` with `0xF` (so always true in this build).",
     "`word[01E0C2B0]`, written ~~once~~ at\n  ~~`002539E5` with `0xF` (so always true in this build).~~ "
     "`00253970+0x75` with `0xF` and at `002547C0+0x0` with its caller's `cx` (`00226280+0x203`, `0036D840+0x2B`), "
     "so not fixed in this build " + C + "the two stores to `01E0C2B0`)*."),
    (CGATE, "feeds the pump `word[01E0C2B0]` (single writer `002539E5`, value `0xF`)",
     "feeds the pump `word[01E0C2B0]` (~~single writer `002539E5`, value `0xF`~~ two writers: `00253970+0x75` stores "
     "`0xF`, `002547C0+0x0` stores its caller's `cx` " + C + "the two stores to `01E0C2B0`)*)"),

    # C-V36: 001EDE80 is the 60 fps half-rate predicate over two frame counters.
    (GATE, "`001EDE80` returns 1 under the pause predicate (`[01F82E38]` zero or `[01DFE0C0]` set) and otherwise the sum "
           "of the two cutscene-name-slot counters `0022A080()` and `0022A030()`;",
     "`001EDE80` returns 1 under the ~~pause predicate~~ 60 fps half-rate test (`[01F82E38]` zero or `[01DFE0C0]` set) "
     "and otherwise the sum of the two ~~cutscene-name-slot counters~~ frame counters `0022A080()` and `0022A030()` "
     + C + "`01F82E38` is set to 1 with `01DFE0B4 = 2` by the 60 fps arm, `001EDDC0+0x28`/`+0x32`; `0022A080` and "
     "`0022A030` read `02064AD8` and `02064AA8`, and `02064AD8` toggles every frame at `0022A580+0xC6`–`+0xCF`)*;"),
    (CGATE, "  pause/cutscene-name-slot predicate (`[01F82E38]==0` or `[01DFE0C0]!=0` → return 1, else",
     "  ~~pause/cutscene-name-slot predicate~~ 60 fps half-rate predicate " + C + "`001EDDC0+0x28` sets `01F82E38` with "
     "the 60 fps divisor; `0022A080`/`0022A030` read the frame counters `02064AD8`/`02064AA8`)* (`[01F82E38]==0` or "
     "`[01DFE0C0]!=0` → return 1, else"),

    # C-V37: 0030C300 keeps members without a terminal status, and those with one only when bit 15 holds.
    (GATE, "the members whose status words `+0x64` or `+0x3C` carry `0x80000003` (KO, Stone, X-Zone) or whose field "
           "record bit 15 (`00377C20`) is set,",
     "the members whose status words `+0x64` or `+0x3C` ~~carry `0x80000003` (KO, Stone, X-Zone) or whose field "
     "record bit 15 (`00377C20`) is set~~ carry none of `0x80000003` (KO, Stone, X-Zone), and those that do only when "
     "the field record bit 15 (`00377C20`) is set " + C + "`0030C300+0x44`–`+0x58`)*,"),

    # C-V38: +0xD44 is bumped by pi/10 and capped at 2*pi/15 (single floats); the kind byte goes to +0xD7C.
    (GATE, "`+0xD44` a timer bounded by the per-kind constants at `00916028`/`0091602C` with the kind byte from "
           "`00916010` (`002918A8`..`002918DD`);",
     "`+0xD44` ~~a timer bounded by the per-kind constants at `00916028`/`0091602C` with the kind byte from "
     "`00916010` (`002918A8`..`002918DD`)~~ the radian field `0028BB50` decays (below): the builder adds "
     "`[01DFE0BC]` × `[00916028]` (π/10) and caps it at `[01DFE0BC]` × `[0091602C]` (2π/15) " + C + "`002917E0+0xC8`–"
     "`+0xFD`; the two constants are single floats, not per-kind, and the kind byte from `00916010` goes to `+0xD7C`, "
     "`002917E0+0xB3`–`+0xBB`)*;"),

    # C-V39: 0028CD80 runs on the object itself; only 0028CE90 runs on the two lanes.
    (GATE, "then `0028CD80` and `0028CE90` on the two `0x20`-byte lanes at `+0x30` and `+0x50`: a two-lane rotating fade.",
     "then ~~`0028CD80` and~~ `0028CD80` on the object itself and `0028CE90` on the two `0x20`-byte lanes at `+0x30` "
     "and `+0x50` " + C + "`0028C870+0x97` calls `0028CD80` with `rcx` unchanged, then `+0xA0`–`+0xB8` loops "
     "`0028CE90` over `obj + 0x30 + i × 0x20`, `i` below 2)*: a two-lane rotating fade."),

    # C-V40: 0028BB50's only caller is the 0x0004 group's walk.
    (GATE, "the fixed-width decimal digit writer the `0x0020`-group widget spawner reaches through `0028BB50`.",
     "the fixed-width decimal digit writer ~~the `0x0020`-group widget spawner reaches through `0028BB50`~~ " + C
     + "`0028BB50` is not in the `0x0020` group: its only caller is `0028C4C0+0x13`, run by `0028E290+0x98` under "
     "mask `0x04`, and neither it nor its callee `0028CF80` calls `0029FB50` directly)*."),

    # C-V41: 00377C20 reads a field-record bit, not 01E0C464.
    (GATE, "**That getter is the one word this page is named for**, so the crossing is the AI layer reading\n"
           "the same gate as the fifteen subsystems rather than owning anything here.",
     "**~~That getter is the one word this page is named for~~**~~, so the crossing is the AI layer reading~~\n"
     "~~the same gate as the fifteen subsystems~~ That getter is not this page's word " + C + "`00377C20` returns bit "
     "15 of a record in the `[02ADD100]` table, `00377C20+0x9`–`+0x35`; `01E0C464` is read only by the sixteen tests "
     "in `0028E290`)*, so the AI layer reads field data here rather than owning anything here."),

    # C-V42: a second bulk write (the 0x61F0 clear of +0xAB30) reaches the 23,224-byte hole.
    (CGATE, "exactly once, at construction.**",
     "~~exactly once, at construction.~~ by two bulk writes, at construction and in the `0x61F0`-byte clear of the "
     "`+0xAB30` child.** " + C + "`00290CF0+0xA6` hands `+0xAB30` to `00276650`, whose `+0x88`–`+0x90` calls "
     "`00245000(obj, 0x61F0)`, and `002465F0+0x36` clears it; the RETRACTED 2026-09-19 note above)*"),
    (CGATE, "> So on the extended sweep the constructor's `memset` remains the **only** bulk write reaching the hole.",
     "> ~~So on the extended sweep the constructor's `memset` remains the **only** bulk write reaching the hole.~~ "
     + C + "a second bulk write reaches it, the `0x61F0`-byte clear of `+0xAB30` at `00276650+0x88`–`+0x90`; the "
     "RETRACTED 2026-09-19 note above)*"),

    # C-V43: _8FA0 is 0x1110 = 4,368 bytes (002BE450+0x10 mov edx, 0x1110).
    (CGATE, "bodies** touch **sixteen offsets** across 4,400 bytes",
     "bodies** touch **sixteen offsets** across ~~4,400~~ 4,368 bytes " + C + "`002BE450+0x10` `mov edx, 0x1110`)*"),
    (CGATE, "### All seven children censused: 103 offsets over 43,456 bytes, and they sit in bands",
     "### All seven children censused: 103 offsets over ~~43,456~~ 43,424 bytes, and they sit in bands *(corrected "
     "2026-10-02, OPUS)*"),
    (CGATE, "| `_8FA0` | 4,400 | 16 | 14 |",
     "| `_8FA0` | ~~4,400~~ 4,368 " + C + "`0x1110`, `002BE450+0x10`)* | 16 | 14 |"),

    # C-V51: the word ships FF FF FF FF.
    (CGATE, "Bit 4 is therefore set (`0xFFFF` at ship) and",
     "Bit 4 is therefore set (~~`0xFFFF`~~ `0xFFFFFFFF` at ship " + C + "the image bytes at `01E0C464` are "
     "`FF FF FF FF`)*) and"),

    # C-V46 / C-V47 / C-V48: stop-registry roles.
    (STOP_C, "start `00225CD0` and\n  stop-sweep `00225EB0` both set it.",
     "~~start~~ cancel `00225CD0` " + C + "it clears the request's bit at `00225CD0+0x38`; the start is `00226BE0`)* "
     "and\n  stop-sweep `00225EB0` both set it."),
    (STOP_C, "2026-09-23 (SWE2-CONTRACT): yes — at least ten.**",
     "2026-09-23 (SWE2-CONTRACT): yes — at least ~~ten~~ nine.** " + C + "`00252D90` and `002544C0` below only "
     "cancel)*"),
    (STOP_C, "`0026B980` (start-B), `00252D90`, `002544C0`,",
     "`0026B980` (start-B), ~~`00252D90`, `002544C0`,~~ " + C + "these two only cancel, through `00225CD0` or the id-22 "
     "cancel `002260A0`: `00252D90+0x22`/`+0x2E`, `002544C0+0x21`/`+0x30`; they start nothing)*"),
    (STOP_C, "and **`+0x14` byte — zeroed** at start/reset in\n  both records (`00225E30`/`00226003`/`00226008`).",
     "and **`+0x14` byte — ~~zeroed~~ the start's flag argument** in record B (`00227680+0x30` "
     "`mov [r8+0x14], r9b`, called from `00226BE0+0x92`), ~~at start/reset in~~ zeroed at cancel and reset in\n"
     "  both records (`00225E30`/`00226003`/`00226008`) " + C + "the start stores the flag)*."),

    # C-V53: 00313650 tail-jumps to 00313840 only when bit 0 is clear; 00313840 clears bit 0 only when set.
    (MODE, "`00313650` — resets through `00313840` if bit 0 is still on |",
     "`00313650` — resets through `00313840` ~~if bit 0 is still on~~ only when bit 0 is clear " + C
     + "`00313650+0x7` `test byte [rax+0x5B04], 1`, `+0xE` `je 00313840`)* |"),
    (MODE, "`00313650` sets bit 0 through `00313840` when it is clear (the summon reset, §2c);",
     "`00313650` ~~sets bit 0 through `00313840` when it is clear~~ tail-jumps to `00313840` when bit 0 is clear, and "
     "`00313840` clears bit 0 only when it is set " + C + "`00313840+0x13`–`+0x18`)* (the summon reset, §2c);"),

    # C-V54: 00307200 / 00307240 are compare-and-write setters.
    (MODE, "Two plain `jmp` thunks into the `02EBF190 + 0x5B04` bit getters.",
     "Two plain `jmp` thunks into the `02EBF190 + 0x5B04` bit ~~getters~~ setters " + C + "each compares the bit with "
     "`ecx` and writes the word when they differ, `00307200+0x16`–`+0x2C` and `00307240+0x16`–`+0x2C`)*."),
    (MODE, "| `0037D110` | `00307200` | `dword[+0x5B04] >> 3 & 1` |",
     "| `0037D110` | `00307200` | ~~`dword[+0x5B04] >> 3 & 1`~~ sets or clears bit 3 to `ecx`, no write when equal "
     + C + "`00307200+0x1E`/`+0x29`)* |"),
    (MODE, "| `0037D120` | `00307240` | `dword[+0x5B04] >> 2 & 1` |",
     "| `0037D120` | `00307240` | ~~`dword[+0x5B04] >> 2 & 1`~~ sets or clears bit 2 to `ecx`, no write when equal "
     + C + "`00307240+0x1E`/`+0x29`)* |"),

    # C-V55: 00313550 works on [02EBF190] + 0x5B04.
    (MODE, "of the `+0x5B04` dword on the `02EC4BA9` object - equal returns,",
     "of the `+0x5B04` dword on the ~~`02EC4BA9` object~~ `[02EBF190]` block " + C + "`00313550+0x0` "
     "`mov r8, [02EBF190]`)* - equal returns,"),

    # C-V56: state + 0x5AE0 is a dword.
    (CMODE, "| `state + 0x5AE0` | 8 |",
     "| `state + 0x5AE0` | ~~8~~ 4 " + C + "every access is a dword or a byte, e.g. `00304060+0xD1` "
     "`or dword [rax+0x5AE0], 1`, `00304440+0xB` `test byte [rax+0x5AE0], 1`; never a qword)* |"),

    # C-V57: one mode word (+0x5B04) is persisted, not two.
    (MODE, "§\"It survives area transitions\" describes is therefore the chocobo's block plus the two mode\n"
           "words — a ride survives a zone change and a save.",
     "§\"It survives area transitions\" describes is therefore the chocobo's block plus ~~the two mode~~ the one "
     "mode\n~~words~~ word `+0x5B04` " + C + "the capture `002EF3C0` copies `+0x5AE0`, `+0x5AD0` and `+0x5B04` only, "
     "`002EF3C0+0x13`–`+0x3D`, and the restore `002EF410` writes back the same; `+0x5B08` is not captured)* — a ride "
     "survives a zone change and a save."),

    # C-V58: five 18-byte tables at +0x5A48, +0x5A5A, +0x5A6C, +0x5A7E, +0x5A90.
    (MODE, "`+0x5A58`, four 18-byte entries) to the **leader alone**:",
     "~~`+0x5A58`, four 18-byte entries~~ the class tables at `+0x5A5A`, `+0x5A6C`, `+0x5A7E`, `+0x5A90`, 18 bytes "
     "each " + C + "`00329CC0+0x123`–`+0x167` copies the 18-byte table at `+0x5A48` into the four; `+0x5A58` is the "
     "last word of `+0x5A48`'s table)*) to the **leader alone**:"),
    (HUBS, "then one of five byte arrays of the block at `+0x5A58`…`+0x5A90`)",
     "then one of five ~~byte arrays of the block at `+0x5A58`…`+0x5A90`~~ 18-byte arrays of the block at "
     "`+0x5A48`, `+0x5A5A`, `+0x5A6C`, `+0x5A7E` and `+0x5A90`, read as bytes at a two-byte stride " + C
     + "`0031B9F0+0x4D` to `+0xBA`)*)"),

    # C-V59: 002E73C0 tail-calls 003E6AA0 when dword[+0x284] is non-zero.
    (CMODE, "`0x740`-stride render-record array, and only when the record's `[+0x284]` word is\nzero does it tail "
            "`003E6AA0`.",
     "`0x740`-stride render-record array, and only when the record's `[+0x284]` ~~word is~~ dword is\n~~zero~~ "
     "non-zero " + C + "`002E73C0+0x33` `cmp dword [rcx+0x284], 0`, `+0x3A` `jne 003E6AA0`)* does it tail "
     "`003E6AA0`."),

    # C-V60: six of the named callers call the wrapper 00303EC0, not the ladder; the ladder has 22 call sites.
    (CMODE, "**Callers of the ladder:** `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`),\n"
            "`InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), `BattleUnit_ApplyUnitDefinition`\n"
            "(`0023A570`), `BattleGroup_RefreshFourActorDefinitions` (`003266C0`), `00235EA0`, `00320230`,\n"
            "`0035BC50`, `00313DB0` (inline), and the two mode getters.",
     "**Callers of the ladder:** ~~`PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`),~~\n"
     "~~`InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), `BattleUnit_ApplyUnitDefinition`~~\n"
     "~~(`0023A570`),~~ `BattleGroup_RefreshFourActorDefinitions` (`003266C0`), ~~`00235EA0`, `00320230`,~~\n"
     "~~`0035BC50`,~~ `00313DB0` (inline), and the two mode getters. " + C + "`0023B040`, `00253C70`, `0023A570`, "
     "`00235EA0`, `00320230` and `0035BC50` call the wrapper `00303EC0`, which calls the ladder at `00303EC0+0x4` and "
     "answers `mode == 2`; the ladder's own 22 direct call sites are in 21 functions from `002FFCF0` to `003266C0`)*"),
    (CMODE, "The ladder `0030D9A0` has **20 call sites, all in the `0x2FF…0x326` battle cluster**",
     "The ladder `0030D9A0` has **~~20~~ 22 call sites, all in the `0x2FF…0x326` battle cluster** " + C + "22 direct "
     "`call` sites in 21 functions, `00326500` twice)*"),

    # C-V61 (MODE part): extents of 00303F00 (342 B), 00304060 (222 B), 00306760 (911 B of code).
    (MODE, "`00303F00` (~27 B) — `qword[02EBF190]` base load (`00303F14`).\n\n| member | role | interior |\n"
           "| --- | --- | --- |\n| `0017D3A0` | `001D50D0()` →",
     "`00303F00` ~~(~27 B)~~ (342 B, `ret` at `00303F00+0x155`) " + C + "measured)* — `qword[02EBF190]` base load "
     "(`00303F14`).\n\n| member | role | interior |\n| --- | --- | --- |\n| `0017D3A0` | `001D50D0()` →"),
    (MODE, "`00303F00` (~27 B) — `qword[02EBF190]` base load (`00303F14`).\n\n| member | role | interior |\n"
           "| --- | --- | --- |\n| `0017D3A0` | `001D50D0()` then",
     "`00303F00` ~~(~27 B)~~ (342 B, `ret` at `00303F00+0x155`) " + C + "measured)* — `qword[02EBF190]` base load "
     "(`00303F14`).\n\n| member | role | interior |\n| --- | --- | --- |\n| `0017D3A0` | `001D50D0()` then"),
    (MODE, "`001D50D0()` → `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | "
           "[`0017D3AB`](../../_index/ADDRESS-INDEX.md) |\n\n`00304060` (~11 B) —",
     "`001D50D0()` → `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | "
     "[`0017D3AB`](../../_index/ADDRESS-INDEX.md) |\n\n`00304060` ~~(~11 B)~~ (222 B, `ret` at `00304060+0xDD`) " + C
     + "measured)* —"),
    (MODE, "`001D50D0()` then `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | "
           "[`0017D3AB`](../../_index/ADDRESS-INDEX.md) |\n\n`00304060` (~11 B) —",
     "`001D50D0()` then `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | "
     "[`0017D3AB`](../../_index/ADDRESS-INDEX.md) |\n\n`00304060` ~~(~11 B)~~ (222 B, `ret` at `00304060+0xDD`) " + C
     + "measured)* —"),
    (MODE, "`00306760` `BattleAction_UpdateSpecialPresentationSequence` (293 B) —",
     "`00306760` `BattleAction_UpdateSpecialPresentationSequence` (~~293 B~~ 911 B of code, to the `ret` at "
     "`00306760+0x38E`, followed by its switch table up to `00306760+0x3A8`) " + C + "measured)* —"),

    # C-V62: 022C1F50 is an 8-byte source qword, then 32 entries of 16 bytes {unit, HP delta}; 0x208 cleared.
    (MODE, "| `022C1F50` | the accumulated-HP table: 32 entries of 16 bytes (`+8` the target unit, `+0x10` the HP delta), "
           "the source at `+0`,",
     "| `022C1F50` | the accumulated-HP table: ~~32 entries of 16 bytes (`+8` the target unit, `+0x10` the HP delta), "
     "the source at `+0`,~~ the source qword at `+0`, then 32 entries of 16 bytes from `+8`, each the target unit at "
     "its `+0` and the HP delta at its `+8` " + C + "`0030EB10+0x30`–`+0xB7` reads `[base + 8 + 16i]` and "
     "`[base + 0x10 + 16i]` for `i` below 32, and `+0xBF`–`+0xC8` clears `0x208` bytes)*,"),

    # C-V63: 02EAED3C is the TLS AddressOfIndex; no instruction writes it.
    (APP, "TLS-init bracket around a `0018A620` call run; also writes `02EAED3C` |",
     "TLS-init bracket around a `0018A620` call run; ~~also writes `02EAED3C`~~ reads `02EAED3C`, the PE TLS "
     "`AddressOfIndex`, at `00189CE0+0x42` " + C + "no instruction in the image stores to it; the loader writes it)* |"),

    # C-V65: the import is __stdio_common_vsnprintf_s and nothing is dropped.
    (APP, "decoded end to end: `__stdio_common_vsprintf` into a `0x4000` stack buffer, then the",
     "decoded end to end: ~~`__stdio_common_vsprintf`~~ `__stdio_common_vsnprintf_s` " + C + "IAT `008C2DE0`, called "
     "at `005CDAA0+0x68`)* into a `0x4000` stack buffer, then the"),
    (LOG, ">   and the level `cmp` is at `005CDB29`.",
     ">   and the ~~level `cmp` is at `005CDB29`~~ `_Init_thread_epoch` compare against the guard `02CB6158` is at "
     "`005CDAA0+0x89` " + C + "it gates the magic-static init, not a level; §9)*."),
    (LOG, "                        buf, /* size */ 0x4000, fmt, /* locale */ (void *)-1, ap);  /* 008C2DE0 */\n",
     "                        buf, /* size */ 0x4000, fmt, /* locale */ (void *)-1, ap);  /* 008C2DE0 */   // <- "
     "corrected 2026-10-02, OPUS - the import is __stdio_common_vsnprintf_s; r9 = -1 is the count (_TRUNCATE) and the "
     "locale is 0 (005CDAA0+0x4D to +0x68)\n"),
    (LOG, "    return;                                     /* dropped */\n",
     "    return;                                     /* dropped */   // <- corrected 2026-10-02, OPUS - never taken: "
     "the jg at 005CDAA0+0x8F enters the magic-static init, which rejoins the emit at 005CDAA0+0x91\n"),

    # C-V66: 15 functions address the table base; 28 functions hold 49 references into it.
    (EID, "`BattleIdClassD_RefreshPrerequisiteRuntimeFlags` (`0030B270`) — the only code that touches the\n"
          "descriptors at all.",
     "`BattleIdClassD_RefreshPrerequisiteRuntimeFlags` (`0030B270`) — ~~the only code that touches the~~\n"
     "~~descriptors at all.~~ the functions that address the table base; 28 functions hold 49 references into the "
     "table " + C + "rip-relative census over `01EEBCC0`–`01EEC1E7`, fifteen `0x58`-byte rows; "
     "CONTRACT-encoded-id-space-and-class-registry.md, corrected 2026-09-30)*."),

    # C-V67: 00309EC0 always tail-jumps the row's +0x50 query handler with edx = 0.
    (CLS, "which routes by nibble to a record's mutate or query\nhandler rather than validating against a class.",
     "which routes by nibble to a record's ~~mutate or query~~ query\nhandler " + C + "it always tail-jumps the "
     "row's `+0x50` handler with `edx = 0`, `00309EC0+0x51`–`+0x60`; no mutate path)* rather than validating "
     "against a class."),

    # C-V70: 00309440 is a callee of the validator (00322C50+0x31), a leaf.
    (CLS, "*from* `00301AD0`, `00309440`, `00323910`, `00327CB0`;",
     "*from* `00301AD0`, ~~`00309440`,~~ `00323910`, `00327CB0` " + C + "`00309440` runs the other way: "
     "`00322C50+0x31` calls it, and its 30 bytes call nothing)*;"),

    # C-V71: 0031C5D0 is 8,136 B; 0030B270 is 564 B.
    (EID, "`0031C5D0` (~105 B) — six-register body",
     "`0031C5D0` ~~(~105 B)~~ (8,136 B, `ret` at `0031C5D0+0x1FC7`) " + C + "measured)* — six-register body"),
    (EID, "`0030B270` (`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`, ~105 B) —",
     "`0030B270` (`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`~~, ~105 B~~, 564 B) " + C + "`ret` at "
     "`0030B270+0x233`)* —"),

    # C-V73: the validator's class arms (00322C50's 32-entry table).
    (NBR, "every class from 1 to 32 resolves to one registry slot (four slots serve more than one class: `02EBF110` "
          "classes 22..24, `02EBF068` classes 15, 30, 31, `02EBF138` classes 19, 20, `02EBF038` classes 25, 32), class "
          "13 concatenates three slots behind a `0x8000` base,",
     "~~every class from 1 to 32 resolves to one registry slot (four slots serve more than one class: `02EBF110` "
     "classes 22..24, `02EBF068` classes 15, 30, 31, `02EBF138` classes 19, 20, `02EBF038` classes 25, 32), class "
     "13 concatenates three slots~~ classes 2–18, 20, 21 and 24–32 resolve to a registry slot (two slots serve more "
     "than one class: `02EBF068` classes 15, 30, 31 and `02EBF038` classes 25, 32), class 19 is the literal range "
     "`0xE000`..`0xEFFE`, classes 22 and 23 the literal bounds 4 and 9, and class 13 sums the counts of four slots "
     "(`02EBF090`, `02EBF088`, `02EBF080`, `02EBF078`) " + C + "arms `00322C50+0x313` (19), `+0x356`/`+0x35F` (22, 23), "
     "`+0x322` (20, `02EBF138` alone), `+0x368` (24, `02EBF110` alone), `+0x1D8`–`+0x23C` (13); "
     "the-encoded-id-class-registry.md)* behind a `0x8000` base,"),

    # C-V74: the validator reads 02EBF060 in its class-16 arm.
    (EID, "finds only the validator (`00322EBB`), the loader",
     "finds only the validator (~~`00322EBB`~~ `00322C50+0x295`, the class-16 arm " + C + "`00322C50+0x26B` is the "
     "class-15/30/31 arm, which reads `02EBF068`)*), the loader"),

    # C-V75: 002F9920's bucket table is 02EC3D80.
    (EID, "buckets the id into a 28-entry pointer table at `02FDA3D80`",
     "buckets the id into a 28-entry pointer table at ~~`02FDA3D80`~~ `02EC3D80` " + C + "`002F9920+0x47` "
     "`cmp qword [r14+rbp+0x2DA3D80], 0` with `rbp` the image base)*"),

    # C-V76: the empty record is 01CEB638.
    (HUBS, "Returns `01C8B638` (a static empty",
     "Returns ~~`01C8B638`~~ `01CEB638` " + C + "`002F9860+0x1E` `lea rax, [01CEB638]`)* (a static empty"),

    # C-V78: 00323890 reads a 10-entry table at image +0x2038E4.
    (CLS, "indexes a 9-entry jump table at `002038E4` returning 0/1/2/3; outside",
     "indexes a ~~9-entry jump table at `002038E4`~~ 10-entry jump table at image offset `+0x2038E4`, read at "
     "`00323890+0x1A` after `cmp eax, 9` / `ja` at `00323890+0xC`/`+0xF` " + C + "the displacement is image-base "
     "relative)* returning 0/1/2/3; outside"),

    # C-V81: +0x44 pads the saved fourth column; row C's fourth slot is written 1.0f.
    (BASIS, "0062DE6E  mov   dword ptr [rcx + 0x44], eax   ; the scratch fourth slots are zeroed\n",
     "0062DE6E  mov   dword ptr [rcx + 0x44], eax   ; the scratch fourth slots are zeroed   <- corrected 2026-10-02, "
     "OPUS - +0x44 pads the saved fourth column (+0x38..+0x44); +0x54/+0x64 are rows A/B's fourths and row C's +0x74 "
     "is written 1.0f (0062DDE0+0xCC)\n"),

    # C-V82: 003008A0 is the modify entry (it calls the row's +0x48 handler).
    (EID, "slot and falls into `003008A0` - the two-ones-shim into the\nshared query.",
     "slot and falls into `003008A0` - the two-ones-shim into the\n~~shared query.~~ modify entry "
     "`Inventory_ModifyEncodedItemAndUpdateDiscoveryState` " + C + "it calls the row's `+0x48` handler at "
     "`003008A0+0xC0`)*."),
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
