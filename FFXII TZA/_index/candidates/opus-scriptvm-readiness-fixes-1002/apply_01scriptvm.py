"""apply_01scriptvm.py [--apply] - 01-Script-VM-Native-Bridge readiness map (cloud-reports/re-readiness/01-scriptvm.md),
section 3.1 value items C-V1..C-V60 and the section 3.2 stale / banner items, settled on the pages (OPUS, 2026-10-02).

Every value item was decided at the shipping image or the shipped data first (verdict table: the scratch record
verdicts-01.md; the deciding instructions are repeated in each tag). The map's favoured sides were treated as claims:
C-V5 (the footer word's name), C-V27 (stamp width), C-V29 (bind family), C-V30 (requestMask), C-V31 (record size),
C-V36 (movement context) and C-V59 (transition sites) turned out "both partly" or not a contradiction at the bytes and
get no edit; C-V11, C-V54 likewise. C-V34, C-V41, C-V50, C-V56, C-V57, C-V58 are undecidable statically and get no
edit. C-V60 sits in a multi-line YAML value and is left for its owner.
Each edit strikes the side the bytes REFUTE only and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*; stale
"not read / open" lines answered elsewhere get *(answered: see ...; 2026-10-02, OPUS)*; in-body banners are aligned
with the page's own front matter. Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment (their OLD includes the line end, so NEW never contains OLD);
front-matter lines a trailing `# <- corrected` comment on single-line values only. No heading changes.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "01-Script-VM-Native-Bridge/"
README = F + "README.md"
DT = F + "scriptvm-native-dispatch-table.md"
WAIT = F + "verbs-that-only-wait-and-verbs-that-do-nothing.md"
NAMES = F + "how-a-script-names-a-thing-in-the-world.md"
CINT = F + "CONTRACT-interpreter-core.md"
CNCL = F + "CONTRACT-native-command-lifecycle.md"
CBR = F + "CONTRACT-script-to-native-bridge.md"
INT = F + "Interpreter-Core/worldactor-scriptvm-interpreter.md"
RES = F + "Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md"
REQ = F + "Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md"
BIND = F + "Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md"
VARS = F + "Interpreter-Core/script-variables-and-their-storage-classes.md"
ATEL = F + "ATEL-Control-Modules/the-ctrl-module-debug-companions.md"
NCL = F + "Native-Command-Lifecycle/native-command-lifecycle.md"
VD = F + "Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md"
CVD = F + "Verb-Dispatch/CONTRACT-verb-dispatch-abi.md"
POP = F + "Verb-Dispatch/the-shape-of-the-verb-population.md"
REACH = F + "Verb-Dispatch/what-each-script-verb-touches.md"
CC = F + "Spawn-Verbs/the-script-to-native-calling-convention.md"
BP = F + "Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md"
READIN = F + "Party-Presentation-Verbs/the-party-read-in-state-machine.md"
STDM = F + "Party-Presentation-Verbs/the-party-standard-motion-verbs.md"
LOOKS = F + "Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md"

C = "*(corrected 2026-10-02, OPUS: "
A = "; 2026-10-02, OPUS)*"
TBL = ("the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll "
       "`+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`)")
PHASE = ("`00262248`–`0026224F` branch on `+0x15`: 0 runs `begin`, 1 `poll`, anything else jumps to `00262255` and "
         "calls `result` directly")

EDITS = [
    # C-V1: the default arm 0025E60A sets the stop request (0025E555 ebp = 1; 0025E60A-0025E611; loop head
    #       0025E586-0025E596 exits when the stack is empty).
    (INT, "path — but they carry no behaviour of their own.",
     "path — ~~but they carry no behaviour of their own.~~ and that pair is their behaviour: with `ebp = 1` "
     "(`0025E555`) it sets the stop request, which the loop head turns into an exit when the stack is empty "
     + C + "checked at `0025E555`, `0025E60A`–`0025E611` and `0025E586`–`0025E596`; the same arm as RES §6's stop "
     "entry)*."),
    (INT, "**Six of one hundred opcodes are inert in the shipped interpreter** — by their corrected names,",
     "**Six of one hundred opcodes ~~are inert in the shipped interpreter~~ have no handler of their own in the "
     "shipped interpreter and request a stop through the shared arm** " + C + "`0025E60A`–`0025E611` set `edi = 1`; "
     "no shipped script uses them, BF-5)* — by their corrected names,"),
    # C-V2: arithmetic is typed by its operands (0x12 0025ECBA-0025ECD8, 0x13 0025EEA0 / 0025EF6B).
    (INT, "coerce to float32* — so the bytecode is integer-encoded and the arithmetic is float, which is the",
     "coerce to float32* — ~~so the bytecode is integer-encoded and the arithmetic is float~~ but the arithmetic is "
     "typed by its operands: two int32 add and subtract as integers, anything with a float as float32 " + C +
     "`0x12` takes its integer path when both tags are 1, `0025ECBA`–`0025ECD8`; `0x13` `0025EEA0 sub ecx, ebx` "
     "against `0025EF6B subss`; and the pop counted here pops an int32 and truncates a float, `00267E42 cvttss2si`)*, "
     "which is the"),
    # C-S3: the in-body REOPENED line against the front matter.
    (INT, "interpretations are superseded. This page is REOPENED, preserving its older audit receipts.",
     "interpretations are superseded. ~~This page is REOPENED,~~ *(answered: the front matter says `status: "
     "DOCUMENTED` — the reopening resolved, accepted non-author 2026-09-29, OV-18" + A + " preserving its older "
     "audit receipts."),
    # C-S18: the unstruck first copy of the modding note that section 6 itself strikes below.
    (INT, "- **`0x00261DF8` is the single point of control over the whole scripting language.** Repointing one",
     "- ~~**`0x00261DF8` is the single point of control over the whole scripting language.**~~ " + C + "two coupled "
     "tables: the handler comes from `0x00261DF8` (`0025E5DD`) and the instruction length from the descriptor table "
     "`0x01EFEA60` (`0025E631`), as the struck repeat below says)* Repointing one"),
    # C-S20: the claims row names the caller as the entry.
    (INT, "| The interpreter has one entry, `0025DF00`, ticked per frame |",
     "| The interpreter ~~has one entry, `0025DF00`, ticked per frame~~ `0025E4C0` has one caller, `0025DF00` " + C +
     "`0025DF00` is the caller, not the entry; this page's final section and `CONTRACT-interpreter-core.md` "
     "`entries`)* |"),
    # C-S19: r8 is the selected wait slot, not a request entry.
    (INT, "on at `0025E0D0`–`0025E0D3` with the actor record in `rdx` and the actor's request entry in `r8`. So",
     "on at `0025E0D0`–`0025E0D3` with the actor record in `rdx` and ~~the actor's request entry~~ the actor's "
     "selected wait slot `*(actor+0xA8) + sx(actor+0x11)*0x28` in `r8` " + C + "`0025E0CA mov r8, rsi`, `rsi` built "
     "at `0025DFB6`–`0025DFBF`; the 0x14-byte request entries are a different record)*. So"),
    # C-S17: the +0x201 byte is the manager's skip mask.
    (INT, "| `+0x201` | — | the dispatch head (`0025E5C5`) | a byte fed into every handler in `edx` |",
     "| `+0x201` | — | the dispatch head (`0025E5C5`) | a byte fed into every handler in `edx` *(answered: the "
     "manager's skip mask, OV-15 in the-script-from-bytecode-through-wait-and-resume.md" + A + " |"),

    # C-S7 / C-S15 on the resume specification.
    (RES, 'local_production_status: "Locally validated; independent acceptance pending"\n',
     'local_production_status: "Locally validated; independent acceptance pending"  # <- corrected 2026-10-02, '
     'OPUS - OV-18 closed NOT A QUESTION 2026-09-29 (section 8); the SECTION-11 package was accepted non-author '
     '2026-09-29 (SWE2-AUDIT-SEM)\n'),
    (RES, "remaining opcode/service semantics are still separate obligations.",
     "remaining ~~opcode/service~~ service semantics are still separate obligations *(answered for the opcodes: "
     "BF-1 read all 100 handlers, OV-13 in section 8" + A + "."),

    # C-V3: the start path reads the ACTOR's +0x11 (003DBDD4, rcx = the actor).
    (REQ, "the slot is `[actor+0xA8] + byte[entry+0x11]·0x28`",
     "the slot is `[actor+0xA8] + ~~byte[entry+0x11]~~ sx(byte[actor+0x11])·0x28` " + C + "`003DBDD4 movsx rax, "
     "byte ptr [rcx + 0x11]` with `rcx` the actor (`003DBDE7 mov rax, [rcx + 0xa8]`); the entry is `rsi`, whose "
     "`+0x11` is the run state written 3 at `003DBE68`)*"),

    # C-S7 / C-S15 / C-S16 on the interpreter contract (overlay carrier).
    (CINT, 'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"\n',
     'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected '
     '2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the interpreter page records\n'),
    (CINT, "| Bytecode/labels/pools | Caller-bound synthetic inputs in these tests. Full resource lifetime not established. |",
     "| Bytecode/labels/pools | Caller-bound synthetic inputs in these tests. Full resource lifetime not established "
     "*(answered: OV-17 — every shipped operand in range, tables live as long as the bound payload" + A + ". |"),
    (CINT, "- Remaining opcode semantics, variable/reference forms, actor-call/return stacks and other wait kinds.",
     "- Remaining opcode semantics, variable/reference forms, actor-call/return stacks and other wait kinds *(answered "
     "in part: opcode semantics and actor-call/return BF-1 / OV-13, other wait kinds OV-14 — "
     "the-script-from-bytecode-through-wait-and-resume.md section 8" + A + "."),
    (CINT, "- Authored operand/index bounds and resource lifetime for bytecode, label tables and constant pools.",
     "- Authored operand/index bounds and resource lifetime for bytecode, label tables and constant pools *(answered: "
     "OV-17, same section 8" + A + "."),
    (CINT, "- Meaning/producer scope of the actor-indexed control byte; it is not commandPhase by displacement.",
     "- Meaning/producer scope of the actor-indexed control byte; it is not commandPhase by displacement *(answered: "
     "the target manager's skip mask `+0x201`, OV-15; `00267310` reads `02099011 + sx(idx)*0x288`" + A + "."),

    # C-S7 / C-S26 / C-V42 / C-V53 on the lifecycle contract.
    (CNCL, 'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"\n',
     'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected '
     '2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the lifecycle page records\n'),
    (CNCL, "is `AO-1` and is not settled here.*\n",
     "is `AO-1` and is not settled here.* *(answered: AO-1, 2026-09-12 — the shared table is family 2's and the other "
     "eleven are verb-less fallbacks, native-command-lifecycle.md section 7" + A + "\n"),
    (CNCL, "every one of the 1,155 single-callback commands take three frames instead of none.",
     "every one of the ~~1,155~~ single-callback commands take three frames instead of none " + C + "family 0 has "
     "1,288 single-callback records (1,189 `result` only, 73 `begin` only, 26 `poll` only), and all five tables "
     "1,571 commands with a real `result` alone; " + TBL + ")*."),
    (CNCL, "— three-visit phasing is the natural design and it would make 1,155 instantaneous commands take",
     "— three-visit phasing is the natural design and it would make ~~1,155~~ 1,571 " + C + "the `result`-only "
     "commands of all five tables, " + TBL + ")* instantaneous commands take"),
    (CNCL, "Area initialisation is where the sixteen family-table pointers at `02B57EF0` are (re)built, so the world",
     "Area initialisation is where the sixteen family-table pointers at `02B57EF0` are ~~(re)built~~ built, once "
     + C + "`003DC2D0` is their only writer and is reached only through `00266D10` ← `0022A0B0` (`0022A3F7`) ← "
     "`0017D4C0` (`0017D5CC`) ← the start-up job `0017D000`, posted at `0017CF8C`; static)*, so the world"),

    # C-V12 / C-V19 / C-V20 / C-V22 / C-V52 / C-S7 on the bridge contract (overlay carrier).
    (CBR, 'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"\n',
     'local_production_status: "SECTION-11 locally validated; formal independent acceptance pending"  # <- corrected '
     '2026-10-02, OPUS - accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18), as the interpreter page records\n'),
    (CBR, "                            selector. Do not equate those fields; the complete enum is unresolved.\n",
     "                            selector. Do not equate those fields; the complete enum is unresolved.   <- corrected "
     "2026-10-02, OPUS: the enum is two-valued in practice - 75 push sites and PUSHV store 6 (the resolver always "
     "sets its out-record +0x00 = 6, 00262667; PUSHV copies it, 00268090/002680C2); only PUSHP stores the "
     "descriptor's width nibble 0..5 (00268118-00268150, 00268185); one reader, 00263450 (from 00353D10)\n"),
    (CBR, "The verb ids and their handlers are the 1,224-row dispatch table",
     "The verb ids and their handlers are the ~~1,224-row~~ 1,493-row " + C + "the file's header and data rows, "
     "extended 2026-09-19 and 2026-09-26)* dispatch table"),
    (CBR, "the calling convention every one of them obeys.\n",
     "~~the calling convention every one of them obeys.~~ the calling convention their `result` callbacks obey "
     + C + "`begin` also receives the manager as a fifth argument, `002622C4`–`002622CD`, and `poll` only three "
     "registers, `002622EE`–`002622F8` — as §2 says)*.\n"),
    (CBR, "> writes only 0 (interpreter clear), 2 and 3 (§14 item 2).",
     "> writes ~~only 0 (interpreter clear), 2 and 3~~ 0, 1, 2 and 3 " + C + "`0026230B mov byte ptr [rdi + 0x15], "
     "1` in the lifecycle, on the wait slot the interpreter passes, and `00261B97 mov word ptr [rsi + 0x14], 0x107`)* "
     "(§14 item 2)."),
    (CBR, "| `+0x15` writer population is exactly {clear 0, int 2, float 3} |",
     "| `+0x15` writer population ~~is exactly {clear 0, int 2, float 3}~~ includes {clear 0, busy 1, int 2, float 3} "
     + C + "`0026230B` writes 1 on a busy poll and `00261B97` writes 1 with wait kind 7)* |"),
    (CBR, "one of the four paths the depth word at `[rcx]` is left untouched, so a refusal is not a pop.",
     "one of the four paths ~~the depth word at `[rcx]` is left untouched, so a refusal is not a pop~~ the empty "
     "paths leave the depth word alone, but both unknown-tag paths have already stored the decremented depth " + C +
     "`00267E1F mov dword ptr [rcx], eax` before the tag test `00267E21`, `00267DBF` before `00267DC1`)*."),
    (CBR, "1. The complete enum of the source-kind byte and purpose of the +84 array. Existing type-row",
     "1. The complete enum of the source-kind byte *(answered: 6 from every push and from PUSHV, the width nibble "
     "0..5 from PUSHP — `00262667`, `00268090`, `00268185`" + A + " and purpose of the +84 array. Existing type-row"),

    # C-V4 / C-V7 / stale items on the binding page (held: an ACTIVE SWE2-CONTRACT task edits this page).
    (BIND, "`003DBDC0` `ActorResource_StartEntryScriptExecution` (41 B) — the",
     "`003DBDC0` `ActorResource_StartEntryScriptExecution` (~~41 B~~ 210 B " + C + "its last `ret` is `003DBE91`, "
     "followed by `int3` at `003DBE92`; `003DBE68` is inside it)*) — the"),
    (BIND, "`dword[r8]` bound (`00358A04`), `eax = dword[r8+rax*8+8]` (`00358A0F`), then `dword[022C7FE0]` + `003588B0` "
           "(`00358A24`/`00358A37`) |",
     "`dword[r8]` bound (`00358A04`), `eax = dword[r8+rax*8+8]` (`00358A0F`)~~, then `dword[022C7FE0]` + `003588B0` "
     "(`00358A24`/`00358A37`)~~ " + C + "the 21 bytes end with `ret` at `00358A14`; `00358A24`/`00358A37` belong to "
     "the next function `00358A20`, called from `003594E0`)* |"),
    (BIND, "`00268850` (`ScriptVM_SubmitActorRuntimeRequest`, ~250 B) — the submit",
     "`00268850` (`ScriptVM_SubmitActorRuntimeRequest`, ~~~250 B~~ 545 B " + C + "its last `ret` is `00268A70`)*) — "
     "the submit"),
    (BIND, "`00226BE0`, an Input-layer helper that builds a per-channel bitmask (`movsxd rax, ecx`; `r13d = 1 << cl`",
     "`00226BE0`, ~~an Input-layer helper that builds a per-channel bitmask~~ the system-stop registry's request start "
     "for channel 6, which builds a per-channel bitmask " + C + "it ORs the bit into `01FD46D4` (`00226C7A`), raises "
     "`01FD46D0` (`00226C87`) and marks every actor's stop masks (`00226CFC`–`00226D80`); the call at `002632AD` "
     "passes `ecx = 6`)* (`movsxd rax, ecx`; `r13d = 1 << cl`"),
    (BIND, "at `00226BFA`–`00226C03`): the entry-start path consults the input channel state. (edge: `edges.tsv`)",
     "at `00226BFA`–`00226C03`): the entry-start path ~~consults the input channel state~~ raises a system stop "
     "request " + C + "it writes the stop state, it does not read input)*. (edge: `edges.tsv`)"),
    (BIND, "state-1 entry to 2 was not found in the functions read (the wait resolver `0025DF00` is the",
     "state-1 entry to 2 was not found in the functions read *(answered: RC-14, 2026-09-30 — image-wide exactly three "
     "stores reach an entry's `+0x11`, plus the insert; section 7" + A + " (the wait resolver `0025DF00` is the"),
    (BIND, "sites read other slots of the same footer; which special type each site asks for is not read here\n",
     "sites read other slots of the same footer; which special type each site asks for is not read here *(answered on "
     "ORACLE's record: RC-12, 2026-09-30, section 7 — FABLE's adjudication of the numbering is still pending" + A + "\n"),
    (BIND, "`StartEntryScriptExecution` → `WorldActorScriptVM_InterpretBytecode`.",
     "`StartEntryScriptExecution` ~~→ `WorldActorScriptVM_InterpretBytecode`~~ (sets the PC and wait kind 1) " + C +
     "`003DBE09`/`003DBE0C`; the interpreter's only caller is `0025DF00`, `0025E0D3`)*."),
    (BIND, "**Not claimed:** the other seven kinds remain unnamed — this pass adds one value to the enum, not a",
     "**Not claimed:** the other seven kinds remain unnamed *(answered: wait kinds 0–7 are enumerated, OV-14 — "
     "the-actor-request-from-arming-through-start-and-return.md section 5" + A + " — this pass adds one value to the "
     "enum, not a"),
    (BIND, "this correction reopens the mechanism pending review rather than silently retaining AUDITED.",
     "this correction reopens the mechanism pending review rather than silently retaining AUDITED *(answered: the "
     "review is done — the 2026-09-30 reconciliation below" + A + "."),

    # C-V12 / C-V23 / C-V55 on the variables page.
    (VARS, "resolver: **`+0x200`–`+0xCF4` of the persistent payload is the script-global variable space**, 0xAF5",
     "resolver: **`+0x200`–`+0xCF4` of the persistent payload is the script-global variable space**, ~~0xAF5~~ 0xAF6 "
     + C + "the last declared global is a `u16` at `+0xCF4` in 101 shipped scripts, "
     "[`script-global-variables-by-offset.tsv`](script-global-variables-by-offset.tsv), so the space runs to "
     "`+0xCF5`)*"),
    (VARS, "- Array indices are clamped, not checked: an out-of-range read returns the edge element silently.",
     "- Array indices are clamped, not checked: an out-of-range read returns the edge element silently ~~.~~ when the "
     "dimension is 1 or more; a dimension of 0 reads one element before the array " + C + "`0026250A`–`00262518` "
     "clamp with a signed `cmovl`, §2)*."),
    (VARS, "> value came from. **What the other values of that byte are is still unknown.**",
     "> value came from. **~~What the other values of that byte are is still unknown.~~** " + C + "`PUSHV`'s value "
     "is always 6 — the resolver writes `+0x00 = 6` at `00262667` on its only exit — and the one other value source is "
     "`PUSHP`, which stores the descriptor's width nibble 0..5 there (`00268118`–`00268150`, `00268185`); one reader, "
     "`00263450`, called from `00353D10`)*"),

    # C-V44 / C-V45 / C-S10 on the debug-companion page.
    (ATEL, "full pages are `{u16 lineOff[32]; u16 chunkEnd; u16 0}` with `chunkEnd` the file-absolute last byte of the "
           "page's text chunk",
     "full pages are ~~`{u16 lineOff[32]; u16 chunkEnd; u16 0}` with `chunkEnd` the file-absolute last byte of the "
     "page's text chunk~~ `{u16 lineOff[32]; u32 nextPageBase}` " + C + "88 of the 312 trailers in the shipped "
     "`.sbn` files have a non-zero high half, read through `vbf_read_entry`)*"),
    (ATEL, "The header is three `(offset, size)` pairs (`0x8478, 0x78`;",
     "The header is three ~~`(offset, size)`~~ `(section offset, table offset)` " + C + "the second words are "
     "`0x78`/`0x7C`, `0x6C` and `0x160`..`0x280` in the four shipped `.dbg` files, front-region offsets, while slot "
     "1's section runs to the end of the file)* pairs (`0x8478, 0x78`;"),
    (ATEL, "five `(offset,size)` header slots (three used)",
     "five ~~`(offset,size)`~~ `(section offset, table offset)` " + C + "as §2; the second word `0x6C` is the same in "
     "all four files)* header slots (three used)"),
    (ATEL, "leaves that unproven. S2 is a 0-terminated `u32` offset array (65 entries for ctrl/evctrl/btlctrl, 301 for",
     "leaves that unproven. S2 is ~~a 0-terminated `u32` offset array (65 entries for ctrl/evctrl/btlctrl, 301 for~~ "
     "`{u32 count = 0x40; u32 offs[64]}` in all four modules " + C + "the count word at S2 is `0x40` in the shipped "
     "`ctrl`, `evctrl`, `btlctrl` and `mapctrl` `.dbg`; §2's 64-slot directory)*"),
    (ATEL, "`btlctrl` it runs `0x1CD7D..~0x41F4F` (≈150 KiB, essentially to EOF) and additionally contains the full",
     "`btlctrl` it runs ~~`0x1CD7D..~0x41F4F`~~ `0x1CA20..~0x41F4F` " + C + "the heap starts at header `+0x08` = "
     "`0x1CA20`, whose first bytes are `btlctrl.src` and the `systemctrl.ath` path; `0x1CD7D` lies inside it)* "
     "(≈150 KiB, essentially to EOF) and additionally contains the full"),
    (ATEL, "## 6. Falsification pass\n\nNot yet run.\n",
     "## 6. Falsification pass\n\n~~Not yet run.~~ *(answered: falsification pass 1 ran 2026-09-13, §9" + A + "\n"),
    (ATEL, "`003306E0` (~351 B) — six-register ctrl-module body",
     "`003306E0` (~~~351 B~~ 3,882 B " + C + "its last `ret` is `00331609`, the size the SN-1 answer above gives)*) — "
     "six-register ctrl-module body"),

    # C-V8 / C-V9 / C-V10 / C-V51 / C-V52 / C-S2 / C-S31..C-S35 on the dispatch-table page.
    (DT, "**DOCUMENTED.** The table is the **`result` callback column** of a three-callback native command",
     "~~**DOCUMENTED.**~~ **AUDITED.** " + C + "the front matter says `status: AUDITED`)* The table is the **`result` "
     "callback column** of a three-callback native command"),
    (DT, "(Verb-Dispatch/scriptvm-dispatch.tsv) (1,224 rows).",
     "(Verb-Dispatch/scriptvm-dispatch.tsv) (~~1,224~~ 1,493 rows " + C + "the file's own header and its data rows, "
     "extended 2026-09-19 and 2026-09-26)*)."),
    (DT, "fact** — the index mapping is known wrong in at least one region. Verify a handler's argument",
     "fact** — the index mapping ~~is known wrong in at least one region~~ is the call id exactly *(answered: "
     "CORRECTED 2026-09-07, §2 — the `0x048C`/`0x048D` step was a column confusion, I-6 closed" + A + ". Verify a "
     "handler's argument"),
    (DT, "**`scriptvm-dispatch.tsv` has the two callbacks one call id early.** Over its 1,224 rows the `handler` column "
         "equals",
     "*(answered: the TSV's begin / poll columns were re-framed 2026-09-19 (OPUS) and the 259 asynchronous ids added "
     "the same day — see its header" + A + " ~~**`scriptvm-dispatch.tsv` has the two callbacks one call id "
     "early.**~~ Over its 1,224 rows the `handler` column equals"),
    (DT, "Record layout (interpretation UNPROVEN beyond field +0)\n",
     "Record layout (interpretation UNPROVEN beyond field +0)   <- corrected 2026-10-02, OPUS: settled by §2 (restored "
     "2026-09-19): begin +0, poll +8, unused +0x10, result +0x18 from tbl + 8 + 0x20n (003DC28E, 003DC25E, 003DC2BA)\n"),
    (DT, "those 3 is a named catalog verb. The other **259 implement `begin` and `poll`**: they are",
     "those 3 is a named catalog verb. The other ~~**259 implement `begin` and `poll`**~~ **259** lack a `result`: "
     "160 have `begin` and `poll`, 73 `begin` only and 26 `poll` only " + C + "family 0 under " + TBL + ")*: they are"),
    (DT, "**Why this is PARTIAL rather than DOCUMENTED.** Every aggregate check passed cleanly, and the",
     "**Why this is PARTIAL rather than DOCUMENTED.** *(answered: the off-by-one was a column confusion, I-6 closed "
     "2026-09-07, and the front matter says `status: AUDITED`" + A + " Every aggregate check passed cleanly, and the"),
    (DT, "**The four tables abut exactly**, which is why a contents walk cannot find their edges: the default's",
     "~~**The four tables abut exactly**~~ **Three of the four joins abut exactly; the default's end leaves eight zero "
     "bytes before family 3** " + C + "records run to `base + 8 + 0x20×count`: `01F281A8`..`01F281B0` is zero, "
     "family 3 ends at `01F29418` and family 5 at `01F29440`)*, which is why a contents walk cannot find their edges: "
     "the default's"),
    (DT, "the same 36 bytes at a different field offset. So:",
     "~~the same 36 bytes at a different field offset~~ 39 and 41 bytes " + C + "`003DC270` (0x27 bytes) and "
     "`003DC2A0` (0x29 bytes); the result accessor has no field displacement, `003DC2BA inc rax / shl rax, 5`)*. So:"),
    (DT, "`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2F0`) is nine instructions and installs\n",
     "~~`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2F0`) is nine instructions and installs~~ "
     "`VMNativeCommandDispatch_InitializeFamilyTables` starts at `003DC2D0` (89 B): a `rep stosq` puts the default "
     "`01F26720` into all sixteen slots, then nine instructions from `003DC2F0` install " + C + "`003DC2D5`–`003DC2E8`; "
     "`003DC2F0` is an interior address)*\n"),
    (DT, "| **0** | `02B57EF0` | `01EED700` | **1496** | `01EED700`..`01EF9200` |",
     "| **0** | `02B57EF0` | `01EED700` | **1496** | ~~`01EED700`..`01EF9200`~~ `01EED700`..`01EF9208` " + C +
     "records start at `tbl + 8`, `003DC28E`)* |"),
    (DT, "| **3** | `02B57F08` | `01F281B0` | **147** | `01F281B0`..`01F29410` |",
     "| **3** | `02B57F08` | `01F281B0` | **147** | ~~`01F281B0`..`01F29410`~~ `01F281B0`..`01F29418` " + C +
     "as row 0)* |"),
    (DT, "| **5** | `02B57F18` | `01F29418` | **1** | `01F29418`..`01F29438` |",
     "| **5** | `02B57F18` | `01F29418` | **1** | ~~`01F29418`..`01F29438`~~ `01F29418`..`01F29440` " + C +
     "as row 0)* |"),
    (DT, "| **7** | `02B57F28` | `01F29440` | **104** | `01F29440`..`01F2A140` |",
     "| **7** | `02B57F28` | `01F29440` | **104** | ~~`01F29440`..`01F2A140`~~ `01F29440`..`01F2A148` " + C +
     "as row 0)* |"),
    (DT, "**Families 1, 2, 4 and 6 are never installed** — which is why the accessor null-checks the table",
     "~~**Families 1, 2, 4 and 6 are never installed** — which is why~~ **Families 1, 2, 4, 6 and 8–15 all get the "
     "default `01F26720`** " + C + "the `rep stosq` at `003DC2E8`)*; the accessor still null-checks the table"),
    (DT, "`0x5D8` (the count) · `0034CF90` · `0034DCC0` · `0` — so record 0's `+0` slot holds the count and its",
     "`0x5D8` (the count) · `0034CF90` · `0034DCC0` · `0` — ~~so record 0's `+0` slot holds the count and its~~ so "
     "the count is a header and the next two qwords are command 0's `begin` and `poll`; record 0 starts at "
     "`tbl + 8` " + C + "`003DC28E` reads begin at `[tbl + 0x20n + 8]`)*; its"),
    (DT, "That is the shape of a fifth table of the same format, **not installed by `003DC2F0`**, which",
     "That is the shape of a fifth table of the same format, ~~**not installed by `003DC2F0`**~~ installed in every "
     "slot first by `003DC2D0`'s `rep stosq` " + C + "`003DC2D5`–`003DC2E8`)*, which"),
    (DT, "`familyArray` is BSS, so whatever writes that slot is the answer, and it is not `003DC2F0`.",
     "`familyArray` is BSS, so whatever writes that slot is the answer, ~~and it is not `003DC2F0`~~ and it is "
     "`003DC2D0` itself " + C + "`003DC2E1 lea rdi, 02B57EF0` / `003DC2E8 rep stosq`, sixteen qwords)*."),
    (DT, "| default | `01F26720` | `01F281A0` | `01F281B0` (family 3) | **16 B** |",
     "| default | `01F26720` | ~~`01F281A0`~~ `01F281A8` | `01F281B0` (family 3) | ~~**16 B**~~ **8 B** " + C +
     "records start at `tbl + 8`)* |"),
    (DT, "| family 3 | `01F281B0` | `01F29410` | `01F29418` (family 5) | **8 B** |",
     "| family 3 | `01F281B0` | ~~`01F29410`~~ `01F29418` | `01F29418` (family 5) | ~~**8 B**~~ **0 B** " + C +
     "as above)* |"),
    (DT, "| family 5 | `01F29418` | `01F29438` | `01F29440` (family 7) | **8 B** |",
     "| family 5 | `01F29418` | ~~`01F29438`~~ `01F29440` | `01F29440` (family 7) | ~~**8 B**~~ **0 B** " + C +
     "as above)* |"),
    (DT, "So the tables are adjacent but **not contiguous** — 16, 8 and 8 bytes of slack. They are still",
     "So the tables are adjacent but **not contiguous** — ~~16, 8 and 8 bytes of slack~~ 8, 0 and 0 bytes of slack "
     + C + "the extents end at `base + 8 + 0x20×count`)*. They are still"),
    (DT, "**Left open:** the **26 records with a `poll` callback and nothing else**, which the catalog calls",
     "**Left open:** *(answered: CE-1 is closed — a poll-only record waits for work an earlier verb started, "
     "verbs-that-only-wait-and-verbs-that-do-nothing.md" + A + " the **26 records with a `poll` callback and nothing "
     "else**, which the catalog calls"),

    # C-V24 / C-V25 / C-V26 / C-S55 / C-S56 on the waits page.
    (WAIT, "| `unkCall_5c7` | — | — | `0016D6A0` | — takes **2** arguments |",
     "| `unkCall_5c7` | — | — | `0016D6A0` | — ~~takes **2** arguments~~ the catalogue declares 2 arguments; the "
     "handler (`ret 0`) consumes none " + C + "`0x05C7` has only the result `0016D6A0`; the CONFLICT note in §7)* |"),
    (WAIT, "| `0034E3E0` | poll shared by `summonreadsync` and `summontopartyreadsync` |",
     "| `0034E3E0` | poll shared by `summonreadsync` and `summontopartyreadsync` " + C + "and by `partyallread` "
     "`0x3EB` and `partyallread2` `0x46F` — four records under " + TBL + ")* |"),
    (WAIT, "  five ATRAC3 verbs the same way, with a result callback only, and exactly one of them is the folded "
           "`ret 0`. There\n",
     "  ~~five ATRAC3 verbs the same way, with a result callback only, and exactly one of them is the folded "
     "`ret 0`. There~~\n"),
    (WAIT, "  is no two-shape split to explain. Why that one verb is stubbed is intent, which no shipped artefact "
           "carries.)*\n",
     "  ~~is no two-shape split to explain. Why that one verb is stubbed is intent, which no shipped artefact "
     "carries.~~)* " + C + "the two-shape split is in the bytes: `0x04AB` and `0x04AD` carry only the poll "
     "`005C5230`, `0x04AE` begin `0016D6A0` + poll `005C5230`, `0x04AA` and `0x04AC` a result only, under " + TBL +
     ")*\n"),
    (WAIT, "**Not claimed.** `CR-2` and `CR-3` stand. What `00314D40`, `003B6F60`, `003B7D30`, `003B7180` and",
     "**Not claimed.** `CR-2` and `CR-3` stand *(answered: CR-3 dissolved 2026-09-26, UQ-65 / CR-2 closed 2026-09-30, "
     "§5; `003B7180` read, below" + A + ". What `00314D40`, `003B6F60`, `003B7D30`, `003B7180` and"),
    (WAIT, "`003B7180` (129 B) is a wait/do-nothing verb body - `0030AA00`/`00263750`/`003589B0`/`0036E750`/`0026DC60`.",
     "`003B7180` (129 B) is ~~a wait/do-nothing verb body~~ the shared tail of two result callbacks, `0x0209` "
     "`changetonormalparty`'s `00350F30` and `0x02A4`'s `0034D330` " + C + "`00350F3D` and `0034D33D` jump to it; "
     "it is in no dispatch record; for each ready slot it calls `0036E750(.., 9)` and `0026DC60(actor, 1)`, "
     "`003B71D9`, `003B71E6`)* - `0030AA00`/`00263750`/`003589B0`/`0036E750`/`0026DC60`."),
    (WAIT, "`0030AA00` (179 B) is the four-slot readiness poll `003B7180` runs for the wait verbs:",
     "`0030AA00` (179 B) is the four-slot readiness poll `003B7180` runs ~~for the wait verbs~~ for those two result "
     "callbacks " + C + "`003B718D` is its only call site)*:"),

    # C-S58 / C-S59 / C-S60 / C-S61 / C-V28 on the names page.
    (NAMES, "UQ-60's open half: **the fourteen keyed values land in the actor's `+0xB8` steering record, the",
     "UQ-60's open half: **~~the fourteen keyed values land~~ thirteen of the fourteen keyed values land " + C +
     "`0x09042A2E` is fetched at `002E2EE5` and its result is never used before the next call, `002E2EEA`–`002E2EF2`; "
     "UQ-60's answer)* in the actor's `+0xB8` steering record, the"),
    (NAMES, "| `+0x1E` | `0xFFFF` in all 128 | unknown, uniform |",
     "| `+0x1E` | `0xFFFF` in all 128 | ~~unknown, uniform~~ the sub-record index, `0xFFFF` none *(answered: "
     "`002EB625`–`002EB63D` index the 0x120-byte table at `02161DA0` with it; the 2026-09-18 declaration below" + A +
     " |"),
    (NAMES, "      `.rdata` constant `30.0f` at `008F8D80`.",
     "      `.rdata` constant `30.0f` at `008F8D80` *(answered: only on the render-record fallback path, "
     "`002E2B0A`–`002E2B3B`; the three frame counts use `50.0f` at `008F3130`, `002E2F06`" + A + "."),
    (NAMES, "      bullet stays open until the fourteen destinations are read.",
     "      bullet stays open until the fourteen destinations are read *(answered: read by §4c and the UQ-60 answer "
     "above" + A + "."),
    (NAMES, "| eleven users, five of them named verbs | `edges.tsv` with EH callers excluded, joined to the verb table |",
     "| eleven users, ~~five of them named verbs~~ seven named verbs over twenty sites " + C + "`retool.py callers "
     "002E97C0`: eleven functions, twenty sites, ten of them verb callbacks; §9)* | `edges.tsv` with EH callers "
     "excluded, joined to the verb table |"),
    (NAMES, "| what a record holds with a map loaded | **not established** | — | UNKNOWN |",
     "| what a record holds with a map loaded | **not established** *(answered: UQ-58, 2026-09-17, §6" + A +
     " | — | UNKNOWN |"),
    (NAMES, "| any runtime observation | **none exists** | — | UNKNOWN |",
     "| any runtime observation | **none exists** *(answered: the title-screen read of all 128 records, two rows above, "
     "tier 10" + A + " | — | UNKNOWN |"),
    (NAMES, "remain unread. Whether the other bind verbs decode a placement: the **decoder** still has one caller,",
     "remain unread *(answered: the stamp increments, UQ-59 2026-09-14; `002E28E0` read by §4c and UQ-60; the other "
     "three read in §6" + A + ". Whether the other bind verbs decode a placement: the **decoder** still has one "
     "caller,"),

    # C-V11 (no edit) / C-V13 / C-V14 / C-V16 / C-V17 / C-V18 / C-V46..C-V49 / stale items on the verb-dispatch page.
    (VD, "agree **1,209 times** (§10, §12).",
     "agree **1,209 times** (§10, §12) *(answered: BQ-9, 2026-09-27, measured the other 90; the TSV now carries an "
     "arity on all 1,960 rows and agrees with the catalogue on 1,269 of 1,270" + A + "."),
    (VD, "script until they are done. That is not a convention the script authors invented — it is built into",
     "script until they are done *(answered: not all — 77 verbs with a `begin` and no `poll` return at once, CY-4 "
     "below" + A + ". That is not a convention the script authors invented — it is built into"),
    (VD, "                                                   /* phase 0 and 1 both fall through to poll */\n",
     "                                                   /* phase 0 and 1 both fall through to poll */  /* <- corrected "
     "2026-10-02, OPUS: phase >= 2 skips begin AND poll and calls result directly, 00262248-00262255 */\n"),
    (VD, "  why 1,573 of the 1,960 commands are instantaneous even though the phase byte starts at 0.",
     "  why ~~1,573~~ 1,571 of the 1,960 commands are instantaneous even though the phase byte starts at 0 " + C +
     "1,571 carry a real `result` and nothing else; `0x0297` and `0x20B5` also carry a `poll` and can block, CZ-1)*."),
    (VD, "Every callback receives the same four things, in the Microsoft x64 convention:",
     "Every callback receives ~~the same four things~~ these things, in the Microsoft x64 convention — `begin` a fifth, "
     "the manager, on the stack " + C + "`002622C4 mov rcx, [rsp + 0x70]` / `002622CD mov [rsp + 0x20], rcx` before "
     "`002622DB call rax`)*:"),
    (VD, "- **`guard` names the early-out** where there is one: `fsmenu` for the 33 fullscreen-menu verbs that",
     "- **`guard` names the early-out** where there is one: `fsmenu` for the ~~33~~ 42 fullscreen-menu verbs " + C +
     "42 rows carry `guard = fsmenu`, 33 of them with operands; the guard `call 0x280120` also opens `0x7036`'s poll "
     "`005113D0`)* that"),
    (VD, "- **327 verbs are durative, 1,573 are instantaneous.** If you need a verb that takes time, it needs",
     "- **327 verbs are durative, ~~1,573~~ 1,571 are instantaneous** " + C + "plus `0x0297` and `0x20B5`, which "
     "carry a `poll` and can block, CZ-1)*. If you need a verb that takes time, it needs"),
    (VD, "- **Family 3's seven are `0x3086`–`0x308F`** in a family spanning `0x3000`–`0x3092` (147 rows):",
     "- **Family 3's seven are ~~`0x3086`–`0x308F`~~ `0x3086`–`0x3089` and `0x308D`–`0x308F`** " + C + "the "
     "catalogue names `0x308A`–`0x308C`; all ten ids have a result callback)* in a family spanning "
     "`0x3000`–`0x3092` (147 rows):"),
    (VD, "        is `0016D6A0`, the folded three-byte `ret 0` — the terminator the dispatch falls closed onto,",
     "        is `0016D6A0`, the folded three-byte `ret 0` ~~— the terminator the dispatch falls closed onto,~~ " + C +
     "that is its `begin`; its `poll` is `005C5230` and its `result` NULL, and an out-of-range command gets NULL from "
     "the count check `003DC283`/`003DC285`, it does not land here)*"),
    (VD, "- [x] The **90 rows still without a measured arity**: 33 command slots with no callback at all,",
     "- [x] The **90 rows still without a measured arity**: 33 command slots with ~~no callback at all~~ no `begin` or "
     "`result` " + C + "29 of them carry a `poll`; 4 — `0x0330`, `0x0356`, `0x03B0`, `0x203E` — have no callback "
     "at all, §2's 2026-09-15 count)*,"),
    (VD, "  neither pop primitive touches it. Left open rather than explained away.",
     "  neither pop primitive touches it. Left open rather than explained away *(answered: BQ-1, 2026-09-13 — 78 "
     "stores, all zero, no reader" + A + "."),
    (VD, "| slot has no callback at all | 33 |",
     "| slot has ~~no callback at all~~ no `begin` or `result` " + C + "29 poll-only, 4 with no callback)* | 33 |"),
    (VD, "is unusual, and each is a small, bounded read. **BQ-7** stays open on those four categories.",
     "is unusual, and each is a small, bounded read. **BQ-7** stays open on those four categories *(answered: BQ-7 "
     "closed 2026-09-02 and BQ-9 2026-09-27, §7" + A + "."),
    (VD, "path-dependent arity on the 33 records that have operands to read; the rest read none either way.\n",
     "path-dependent arity on the 33 records that have operands to read; the rest read none either way. " + C + "the "
     "65 include `0x7036`'s guarded poll `005113D0`)*\n"),
    (VD, "Family 7's records come in exactly four shapes:",
     "Family 7's records come in ~~exactly four shapes~~ these four shapes and a fifth, `poll` only, on 3 records — "
     "`0x7036` (guarded `005113D0`), `0x705F` (`00511FB0`), `0x7060` (`00512010`) " + C + "20 + 22 + 54 + 5 + 3 = "
     "104 under " + TBL + ")*:"),
    (VD, "> (no `openmenu` anywhere in the file), is in the **unguarded** half of the family (62 of 104",
     "> (no `openmenu` anywhere in the file), is in the **unguarded** half of the family (~~62~~ 61 " + C + "43 "
     "records carry the guard, `0x7036`'s poll among them)* of 104"),
    (VD, "**What is honestly left (BQ-9):** 33 slots with no callback, 31 whose operand reads sit inside a loop",
     "**What is honestly left (BQ-9):** 33 slots with ~~no callback~~ no `begin` or `result` " + C + "29 poll-only, "
     "4 with none)*, 31 whose operand reads sit inside a loop *(answered: BQ-9, 2026-09-27, §7" + A),
    (VD, "`DOCUMENTED`, three falsification passes survived, against snapshot",
     "~~`DOCUMENTED`, three falsification passes survived,~~ `AUDITED` " + C + "the front matter says `status: "
     "AUDITED`)*, against snapshot"),
    (VD, "label.** Neither handler is read. `CZ-1`.",
     "label.** ~~Neither handler is read.~~ *(answered: both read 2026-09-14, CZ-1 below" + A + " `CZ-1`."),

    # C-V14 / C-V15 / C-S40 / C-S41 on the dispatch ABI contract.
    (CVD, "Microsoft x64, and the same four things every time:",
     "Microsoft x64, and ~~the same four things every time~~ these four things, with `begin` taking a fifth on the "
     "stack " + C + "`002622C4`–`002622CD`; added below 2026-09-13)*:"),
    (CVD, "| `cmdState` | ≥ `0x28` | `+0x08` bound actor id (u16) ·",
     "| `cmdState` | ≥ `0x28` | `+0x08` bound actor id ~~(u16)~~ (u32) " + C + "written as a dword, `002619AE`, "
     "`002619FD`, `00261ABF`, and read as one, `00262225`)* ·"),
    (CVD, "§2.2 reproduces, and one table holds a **single** command. `VA-1` — what that slot was for — stays",
     "§2.2 reproduces, and one table holds a **single** command. `VA-1` — what that slot was for — ~~stays~~ "
     "*(answered: resolved 2026-09-22 as dead space in the 32-byte stride, the `VA-1` line above" + A),
    (CVD, "open; what is now closed is that it is empty",
     "~~open;~~ what is now closed is that it is empty"),
    (CVD, "**Not claimed:** the lifecycle half is still unexecuted and nothing here is a live observation; §13",
     "**Not claimed:** ~~the lifecycle half is still unexecuted and~~ *(answered: the lifecycle half was executed, "
     "the 2026-09-16 correction in §13" + A + " nothing here is a live observation; §13"),

    # Stale items on the lifecycle page (overlay carrier).
    (NCL, "Whether that is deliberate aliasing or a fallback for unimplemented families is **not established**\n",
     "Whether that is deliberate aliasing or a fallback for unimplemented families is **not established** *(answered: "
     "AO-1, 2026-09-12, §7" + A + "\n"),
    (NCL, "      `005114F0`), so it is not a distinct feature. Family **3** is **spawn**",
     "      `005114F0`), so it is not a distinct feature. Family **3** is ~~**spawn**~~ *(answered: the battle-actor "
     "set, not only spawn — AO-4, 2026-09-27, below" + A),
    (NCL, "on it is open, but \"family 5 does something singular and important\" is **refuted**.",
     "on it is open *(answered: AO-6 closed 2026-09-12, §7" + A + ", but \"family 5 does something singular and "
     "important\" is **refuted**."),
    (NCL, "Family 3's commands `0x3001` and `0x3003` carry **`_guard_check_icall`** as their `result` callback —",
     "Family 3's commands `0x3001` and `0x3003` carry ~~**`_guard_check_icall`**~~ the folded no-op " + C + "it is "
     "the `/OPT:ICF` merge of `ret`-only functions, not the CFG stub — the variables page, 2026-09-13)* as their "
     "`result` callback —"),
    (NCL, "        return FUN_00267310(actorState[0x15]) == 0;   /* still running? */\n",
     "        return FUN_00267310(actorState[0x15]) == 0;   /* still running? */  /* <- corrected 2026-10-02, OPUS: the "
     "argument is a manager index and 00267310 reads 02099011 + sx(idx)*0x288, the skip mask (CE-5 below) */\n"),
    (NCL, "| `003DC240` (39 B) | `GetPollCallback` — bounds-checks `family` against `dword[02B57EF0]` (`003DC253`),",
     "| `003DC240` (39 B) | `GetPollCallback` — ~~bounds-checks `family` against `dword[02B57EF0]`~~ bounds-checks "
     "the command against the table's own count " + C + "`003DC24A mov rcx, [rcx + rax*8]` then `003DC253 cmp edx, "
     "dword ptr [rcx]`; the family index is never bounded)* (`003DC253`),"),

    # C-V19 / C-V20 / C-V21 / C-S49 / C-S50 / C-S52 / C-S53 on the calling-convention page.
    (CC, "> **calling convention every native verb in the game uses** — how a script's arguments arrive, in",
     "> ~~**calling convention every native verb in the game uses**~~ calling convention of the native `result` "
     "callbacks " + C + "`begin` also receives the manager as a fifth argument, `002622C4`–`002622CD`, and `poll` "
     "only three registers, `002622EE`–`002622F8`)* — how a script's arguments arrive, in"),
    (CC, "| `002640C0`, `002650B0` | — | the handle resolution in `00510620` — **not read** |",
     "| `002640C0`, `002650B0` | — | the handle resolution in `00510620` — **not read** *(answered: EF-3, "
     "2026-09-11, §6" + A + " |"),
    (CC, "| `+0x15` | result entry | type tag; `0` none, `1` armed, **`2` = int32**, `3` = float32 |",
     "| `+0x15` | result entry | ~~type tag; `0` none, `1` armed,~~ phase and result type: `0` begin pending, `1` "
     "poll pending, **`2` = int32**, `3` = float32 " + C + "`00262248`–`0026224F` branch on 0 / 1, `0026230B` writes "
     "1 on a busy poll, the result writers 2 / 3, `00262382` resets 0)* |"),
    (CC, "- **Hook the verb, not the native function**, if the intent is to change what scripts can do — five of",
     "- **Hook the verb, not the native function**, if the intent is to change what scripts can do — ~~five~~ three "
     + C + "`00510370+0x1B`, `0051042E`, `0051065A`; three others tail-jump `0026B4E0` and `00510160` ends in `ret` — "
     "\"Three, three and one\" below)* of"),
    (CC, "| What any other result tag means | **not established** | — | UNKNOWN |",
     "| What any other result tag means | **not established** *(answered: EF-1 — `3` is float32, `0026B4C0`" + A +
     " | — | UNKNOWN |"),
    (CC, "| Which script opcode reaches these verbs | **not traced** | — | UNKNOWN |",
     "| Which script opcode reaches these verbs | **not traced** *(answered: UQ-55 / EF-5, §6" + A +
     " | — | UNKNOWN |"),
    (CC, "Across all six, `+0x15` takes **`0`, `1`, `2`, `3`** and nothing else. **`1` is written exactly once",
     "Across all six, `+0x15` takes **`0`, `1`, `2`, `3`** and nothing else. ~~**`1` is written exactly once~~ " + C +
     "`1` is also written as a byte, by the lifecycle: `0026230B mov byte ptr [rdi + 0x15], 1`)*"),
    (CC, "in the EXE, and not as a byte:**\n",
     "~~in the EXE, and not as a byte:**~~ **The interpreter's own write is a word:**\n"),
    (CC, "So the legend \"`1` armed\" is right, but it is reachable only through a **fused 16-bit store that",
     "So the legend \"`1` armed\" is right, but it is reachable ~~only~~ through a **fused 16-bit store that"),
    (CC, "pairs it with wait kind 7** — a byte-level search for `mov byte ptr […+0x15], 1` finds nothing and",
     "pairs it with wait kind 7** — ~~a byte-level search for `mov byte ptr […+0x15], 1` finds nothing and~~ " + C +
     "and through `0026230B`'s byte store)*"),
    (CC, "would conclude the value is unused. The interpreter also writes `+0x14` = `3` (`00261596`) and `5`",
     "~~would conclude the value is unused.~~ The interpreter also writes `+0x14` = `3` (`00261596`) and `5`"),
    (CC, "**Not claimed:** `EF-2` (a negative slot index) is untouched — nothing bounds-checks it and nothing",
     "**Not claimed:** `EF-2` (a negative slot index) is untouched *(answered: UQ-54, 2026-09-25 — no producer emits a "
     "negative channel, §6" + A + " — nothing bounds-checks it and nothing"),
    (CC, "here shows what one would do. The meaning of `+0x44` and `+0x84` on the stack, and of slot `+0x10`,\n",
     "here shows what one would do. The meaning of `+0x44` and `+0x84` on the stack, and of slot `+0x10`, *(answered: "
     "the bridge contract's slot layout names the slot fields; `+0x44` is 6 or `PUSHP`'s width nibble, "
     "`00268185`" + A + "\n"),
    (CC, "*(Read by OPUS 2026-09-14. `EF-2` stays open on the producer side and is narrowed on the reader",
     "*(Read by OPUS 2026-09-14. `EF-2` stays open on the producer side *(answered: UQ-54, 2026-09-25, §6" + A +
     " and is narrowed on the reader"),

    # C-V38 / C-S68 on the battle-party page (FABLE leads it).
    (BP, "world-tick page reads with `0xF`; the setter itself was not read here) before it touches the party. The two "
         "`set` verbs",
     "world-tick page reads with `0xF`; the setter itself was not read here *(answered: `003601B0` / `003601C0` set "
     "and clear bit `cl` of `022CB720`, falsification pass 1 row B1" + A + ") before it touches the party " + C + "`setbattlemember` raises "
     "it before its first pop, `0034D542` then `0034D558`)*. ~~The two `set` verbs~~ `setbattlemember`, "
     "`setbattlememberone` and `addguestbattlemember` " + C + "slot loops `0034D520`–`0034D53B`, `00350CF5`–`00350D10`, "
     "`003521A6`–`003521C1`; `setbattlememberlock` has none)*"),
    (BP, "`setbattlememberlock` ends in; the flag setter and clearer keyed `0x13`; the",
     "`setbattlememberlock` ends in; the flag setter and clearer keyed `0x13` *(answered: falsification pass 1 row "
     "B1" + A + "; the"),
    (BP, "per-actor routine the two `set` verbs call first.",
     "per-actor routine ~~the two `set` verbs~~ the three preamble verbs " + C + "as §2)* call first."),

    # C-V31 (no edit) / C-V32 / C-V33 / C-V35 / C-V39 / C-S62 on the read-in page.
    (READIN, "> 2. release what the old definition loaded and request what the new one needs, in four part slots;",
     "> 2. release what the old definition loaded and request what the new one needs, in ~~four part slots~~ the "
     "element slots *(answered: six elements, one enum, UQ-49 2026-09-16" + A + ";"),
    (READIN, "  +0x04  u32   pending handle   the requested entry's handle (002EAE20 -> 002E9810), written by states 1 "
             "(0037B720) and 19 (0037BEA8)\n",
     "  +0x04  u32   pending handle   the requested entry's handle (002EAE20 -> 002E9810), written by states 1 "
     "(0037B720) and 19 (0037BEA8)   <- corrected 2026-10-02, OPUS: also by states 7, 10 and 13 (0037B95F, 0037BA5A, "
     "0037BB62) and at 0037BDF9, 0037BE31, 0037BE6B, 0037BEC9\n"),
    (READIN, "| `partyallread2` `0x46F` begin `0034D8B0` → `0037CA00` | `02EBF3F0` |",
     "| `partyallread2` `0x46F` begin `0034D8B0` → `0037CA00`; also `summontopartyread` `0x207` result `0034FE80` "
     "(`0034FE99`) " + C + "`0037CA00`'s second caller)* | `02EBF3F0` |"),
    (READIN, "`entryId` (`+0x00`, −1 sentinel / low word = index into the `0x740` record pool at `022C6F28`), the bound",
     "`entryId` (`+0x00`, −1 sentinel / low word = index into the `0x740` record pool ~~at `022C6F28`~~ whose base "
     "pointer is held at `022C6F28` " + C + "`003EC3F0 add rbx, qword ptr [022C6F28]`)*), the bound"),
    (READIN, "`+8`/`+9`/`+0xA`/`+0xB` come from the `002DEBD0`/`002DEB90` pair\n",
     "~~`+8`/`+9`/`+0xA`/`+0xB` come from the `002DEBD0`/`002DEB90` pair~~ `+8` = 0, `+9` = the param, `+0xA` = 0, "
     "`+0xB` = `002DEBD0()` " + C + "`0037CEC3`, `0037CEBF`, `0037CEBB`, `0037CED1`; `002DEB90(1)`'s result is "
     "discarded)*\n"),
    (READIN, "under the `0016D6A0` gate, `[rdi+0x23]` is cleared, and `+8` gains",
     "~~under the `0016D6A0` gate,~~ " + C + "`0016D6A0` is called, `0037CED9`, and nothing tests its result)* "
     "`[rdi+0x23]` is cleared, and `+8` gains"),

    # C-V37 / C-V40 / C-S11 / C-S63 / C-S64 on the standard-motion page.
    (STDM, "00263750's bound 0..3 and base 0209A1F0 both resolve from its 23 bytes\n",
     "00263750's bound 0..3 and base 0209A1F0 both resolve from its 23 bytes  # <- corrected 2026-10-02, OPUS - the "
     "2026-09-14 killer tests (FABLE, section 7) refuted one claim of this pass: the extra argument of 0540/0541 is "
     "the float, kept at 00350077 / 003507D7\n"),
    (STDM, "| `00350050` | `partystdmotionplay_540` handler | 157 B | verb `0540`; leading discard, third push = 1 |",
     "| `00350050` | `partystdmotionplay_540` handler | 157 B | verb `0540`; leading ~~discard~~ float pop, kept and "
     "pushed as the blend " + C + "`00350077 movaps xmm6, xmm0`, `003500A9`)*, third push = 1 |"),
    (STDM, "| `003507B0` | `partystdmotionplaywithoutsame_541` handler | 154 B | verb `0541`; leading discard, third push "
           "= 0 |",
     "| `003507B0` | `partystdmotionplaywithoutsame_541` handler | 154 B | verb `0541`; leading ~~discard~~ float pop, "
     "kept " + C + "`003507D7 movaps xmm6, xmm0`)*, third push = 0 |"),
    (STDM, "pops the `-1.0f` inside `003580C0`, and the discarded extra argument of `0540`/`0541` |",
     "pops the `-1.0f` inside `003580C0`, and the ~~discarded~~ extra argument of `0540`/`0541`, which they keep and "
     "push as the blend " + C + "`00350077`, `003507D7`; §2's 2026-09-14 refutation)* |"),
    (STDM, "> `1`/`0`\"*. It is **not a push** — it is `edx`, the second integer argument in the Win64 register",
     "> `1`/`0`\"*. It is ~~**not a push** — it is `edx`,~~ a push: `edx` carries it into `VMValueStack_PushInt32` "
     + C + "`003500B4 mov edx, 1` / `003500BC call 0x267f90`; §7's later note)* `edx` is the second integer argument "
     "in the Win64 register"),
    (STDM, "[`002E9C1C`](../../_index/ADDRESS-INDEX.md) — the signed definition byte the",
     "[`002E9C1C`](../../_index/ADDRESS-INDEX.md) — the signed ~~definition byte~~ runtime byte of the actor's "
     "secondary context " + C + "`002E9C05 mov rax, [rcx + 0xc0]` loads the context the planter puts at record "
     "`+0x350`; UQ-51 on the read-in page)* the"),
    (STDM, "(`0037C730`) at [`0037CAA3`](../../_index/ADDRESS-INDEX.md); three sibling",
     "(`0037C730`) at [`0037CAA3`](../../_index/ADDRESS-INDEX.md); ~~three sibling~~ " + C + "the four resets are "
     "fields of the one task record `[02EBF400]`, `0037CAB0`–`0037CAD2`)*"),
    (STDM, "globals get field resets (`+8` = 0, `dword` = 0, `+4` = 4, `+0x1C` = 0) and",
     "~~globals get field resets~~ that record gets resets (`+8` = 0, `dword` = 0, `+4` = 4, `+0x1C` = 0) and"),
    (STDM, "two flag bytes, then it tails `00233CF0`. The null arm returns silently.",
     "~~two flag bytes~~ three byte globals are written, `02EBF3FC` = 0, `02EBF3FE` = 0, `02EBF3FD` = 1 " + C +
     "`0037CA90`, `0037CAD6`, `0037CADC`)*, then it tails `00233CF0`. The null arm returns silently."),

    # C-V35 / C-S67 on the appearance page.
    (LOOKS, "render-record array at `020FB7xx` (`imul rcx, rax, 0x740` at",
     "render-record array ~~at `020FB7xx`~~ whose base pointer is held at `022C6F28` " + C + "`002E90FB` and "
     "`002E913D add rcx, qword ptr [022C6F28]`)* (`imul rcx, rax, 0x740` at"),
    (LOOKS, "`cx == -1` exits; `sx(cx) * 0x740 + 022C6F28` resolves the record",
     "`cx == -1` exits; `sx(cx) * 0x740 + ~~022C6F28~~ [022C6F28]` " + C + "`003EC3F0 add rbx, qword ptr "
     "[022C6F28]`, a pointer read through)* resolves the record"),
    (LOOKS, "  > membership the player sees following them — remains open.",
     "  > membership the player sees following them — ~~remains open~~ *(answered: RC-18, 2026-09-30, below — map 1 "
     "is the engine's own follower source" + A + "."),
    (LOOKS, "**Not claimed.** What the four setters do — **none of their bodies was read here**, only their",
     "**Not claimed.** What the four setters do — **none of their bodies was read here** *(answered: read since, the "
     "setter rows above" + A + ", only their"),

    # C-S5 / C-S47 / C-S48 on the reach map.
    (REACH, "> **It covers 616 of the 1,960 verbs, and it is a lead, not a verdict.** `status: PARTIAL` is the",
     "> **It covers 616 of the 1,960 verbs, and it is a lead, not a verdict.** ~~`status: PARTIAL` is the~~ " + C +
     "the front matter says `status: DOCUMENTED`, every register row closed 2026-09-30)*"),
    (REACH, "> honest state.",
     "> ~~honest state.~~"),
    (REACH, "  the call graph and owner tags, which is why its tier is 3 and its status `PARTIAL`. `CY-3`.",
     "  the call graph and owner tags, which is why its tier is 3 ~~and its status `PARTIAL`~~ " + C + "the front "
     "matter says `status: DOCUMENTED`)*. `CY-3`."),
    (REACH, "- The depth-1 table is reproducible in method and stale in detail: five of its fourteen rows drift at the "
            "current\n",
     "- The depth-1 table is reproducible in method and stale in detail: five of its fourteen rows drift at the "
     "current *(answered: RC-21, 2026-09-30 — the rows do not drift with the snapshot; the generator breaks ties in "
     "hash-seed order" + A + "\n"),
    (REACH, "| `Save_Load_Settings` appears only at depth ≥ 2 | the three-depth comparison | 3 |",
     "| `Save_Load_Settings` appears ~~only at depth ≥ 2~~ at depth 1 once and rises from depth 2 " + C + "§2's "
     "corrected depth table: from 1 at depth 1)* | the three-depth comparison | 3 |"),
    (REACH, "| Five of fourteen depth-1 rows drift at the current snapshot | falsification pass 1, the owner-tag control "
            "drifting the same way | 3 |",
     "| Five of fourteen depth-1 rows drift at the current snapshot *(answered: RC-21 — they do not; a hash-seed draw of "
     "the same census" + A + " | falsification pass 1, the owner-tag control drifting the same way | 3 |"),

    # C-S44 / C-S45 / C-S46 on the verb-population page.
    (POP, "> **The helpers are not new; the distribution is.** *\"240 of 583 single-call verb handlers are",
     "> **The helpers are not new; the distribution is.** *\"~~240 of 583~~ 238 of 584 *(answered: the 2026-09-13 "
     "regeneration in §4" + A + " single-call verb handlers are"),
    (POP, "entry) is what separates them; the eight verb handlers above all satisfy it, which is the positive",
     "entry) is what separates them; the ~~eight~~ verb handlers above *(answered: ten, not eight — the adjudication "
     "below" + A + " all satisfy it, which is the positive"),
    (POP, "**[`scriptvm-verb-shapes.tsv`](scriptvm-verb-shapes.tsv) is unchanged.** The four rows still",
     "**[`scriptvm-verb-shapes.tsv`](scriptvm-verb-shapes.tsv) is unchanged.** *(answered: regenerated 2026-09-13; "
     "the four rows now carry the corrected family" + A + " The four rows still"),

    # C-S1 / C-S2 / C-V46 / C-V52 on the category README.
    (README, "  **DOCUMENTED, tier 1.** How a 16-bit call id in the bytecode reaches a native handler: the 4-bit",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* "
     "How a 16-bit call id in the bytecode reaches a native handler: the 4-bit"),
    (README, "  arity**, agreeing with the authored catalog 1,209 times out of 1,210. Carries",
     "  arity**, agreeing with the authored catalog 1,209 times out of 1,210 *(answered: BQ-9 measured the other 90 on "
     "2026-09-27; all 1,960 now carry one, 1,269 of 1,270 agree" + A + ". Carries"),
    (README, "  **DOCUMENTED, tier 2.** The predecessor: family 0's `result` column, 1,224 catalog rows mapped",
     "  ~~**DOCUMENTED, tier 2.**~~ **AUDITED, tier 2.** " + C + "the page's front matter says `status: AUDITED`; its "
     "TSV now holds 1,493 rows)* The predecessor: family 0's `result` column, 1,224 catalog rows mapped"),
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
