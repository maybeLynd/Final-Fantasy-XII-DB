"""apply_09ai.py [--apply] - 09-Combat-AI-And-Gambits readiness map (cloud-reports/re-readiness/09-ai.md), section 3.1
value contradictions C-V1..C-V12 checked at the shipping image, and the section 3.2 stale / banner items, settled on
the pages (OPUS, 2026-10-02).

The map was written from a text snapshot without the executable; every value item here was re-decided at the
instructions (retool.py dis / site / callers) or at the image's .data (the order-handler table), and the verdicts with
their deciding addresses are in the scratch verdicts file. Results: C-V1 B, C-V2 B, C-V3 B, C-V4 B, C-V5 both (disjoint
id bands), C-V6 both (by id; the wait 0x4021 is never rolled), C-V7 B, C-V8 B, C-V9 B on layout / A on fill, C-V10 a
label slip only, C-V11 both right (no edit), C-V12 the image side (and the contract's suggested reconciliation refuted).

Each edit strikes the DISFAVOURED words only and restates them, tagged *(corrected 2026-10-02, OPUS: ...)*; stale
claims are tagged *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; no heading changes.
Left out: C-V11 (no wrong side); stale C-S3/C-S4 (front matter), C-S13..C-S20 (already pointed or answered in place),
C-S21 (wording only).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "09-Combat-AI-And-Gambits/"
G = F + "gambit-evaluation-and-enmity.md"
W = F + "which-gambit-set-fires-and-how-a-command-switches-it.md"
CW = F + "CONTRACT-gambit-walk.md"
CE = F + "CONTRACT-enmity.md"
R = F + "README.md"

FLOOR = "`0032191D`–`00321923`"

EDITS = [
    # C-V1: the seed ternary is reversed - ~opcode & 1 is 1 for an EVEN opcode and seeds 0x80000001 (highest):
    #       00301B44 not r12d / 00301B4C and r12d, 1 / 00301BE3 test r12d, r12d / je 00301BF9;
    #       00301BE8 mov [rsp+0x138], 0x80000001; 00301BF9 mov [rsp+0x138], 0x7FFFFFFF. The prose (side B) is right.
    (G, "    best     = seekMin ? 0x7FFFFFFF : 0x80000001;    // seed so the first candidate always wins\n",
     "    best     = seekMin ? 0x7FFFFFFF : 0x80000001;    // seed so the first candidate always wins   <- corrected "
     "2026-10-02, OPUS: reversed - ~opcode & 1 is 1 for an EVEN opcode and then seeds 0x80000001 (highest), 0 for an "
     "odd one and seeds 0x7FFFFFFF (lowest): 00301B44-00301B4C, 00301BE3 test r12d, r12d / je 00301BF9, 00301BE8 "
     "mov [rsp+0x138], 0x80000001, 00301BF9 mov [rsp+0x138], 0x7FFFFFFF\n"),
    (G, "best    = seekMin ? 0x7FFFFFFF : 0x80000001\n",
     "best    = seekMin ? 0x7FFFFFFF : 0x80000001   <- corrected 2026-10-02, OPUS: reversed - the bit is 1 for an even "
     "opcode, which seeds 0x80000001 (00301BE3-00301BF9); the prose below is right\n"),

    # C-V2: the opcode is the HIGH byte of the entry's +2 word (record +9 for entry 0): 00301B14 movzx r12d,
    #       byte [rdx+rdi*2+9] is compared as the opcode (00301C08 == 1, 00301C10-00301C25 52-55, the jump-table index
    #       00301EA3-00301EA8); 00301B1A reads +8 as the sub-selector (00301C45 cmp edi, 3; 00301EF7 cmp edi, 0x11).
    (G, "`u8 opcode` (`+8`), `u8` (`+9`), `s16 parameter` (`+0xA`).",
     "~~`u8 opcode` (`+8`), `u8` (`+9`)~~ `u8` operand, the sub-selector (`+8`), `u8 opcode` (`+9`) *(corrected "
     "2026-10-02, OPUS: `00301B14 movzx r12d, byte ptr [rdx + rdi*2 + 9]` is the byte compared as the opcode — `== 1` at "
     "`00301C08`, 52–55 at `00301C10`–`00301C25`, the jump-table index at `00301EA3`–`00301EA8` — and `00301B1A movzx "
     "ebp, byte ptr [rdx + rdi*2 + 8]` is the sub-selector compared with 3 at `00301C45`; §8b's Z-1 reading, opcode "
     "high byte)*, `s16 parameter` (`+0xA`)."),
    (G, "> six-byte entries `{u16 operand, u8 opcode, u8, s16 parameter}` at `+6`, `+0xC`, `+0x12` — from the reader, the "
        "writer",
     "> six-byte entries ~~`{u16 operand, u8 opcode, u8, s16 parameter}`~~ `{u16 relation, u8 operand, u8 opcode, s16 "
     "parameter}` *(corrected 2026-10-02, OPUS: the opcode is the entry's byte `+3`, `00301B14`; the sub-selector its "
     "byte `+2`, `00301B1A`)* at `+6`, `+0xC`, `+0x12` — from the reader, the writer"),

    # C-V3: 0x414D does not bypass the AI-suspend bit - 00301505-0030150A (0xFFFF) and 00301511 test [02089340], 0x20 /
    #       00301518 jne 0030150A return 0 before 00301576 mov eax, 0x414D; only the later tests fall over to it.
    (G, "   || (DAT_02089340 & 0x20)                                 // global AI suppression\n",
     "   || (DAT_02089340 & 0x20)                                 // global AI suppression   <- corrected 2026-10-02, "
     "OPUS: this test and the 0xFFFF one above are NOT inside the 0x414D exception - 00301505-0030150A and 00301511 "
     "test [02089340], 0x20 / 00301518 jne 0030150A return 0 before 00301576 compares 0x414D; only the later tests "
     "fall over to that compare\n"),
    (G, "**`0x414D` bypasses the entire gate.** The whole condition is `AND action_id != 0x414D`, so that one\n"
        "action id is evaluated even for a unit that fails every eligibility test. What it is, is unknown -",
     "**`0x414D` bypasses ~~the entire gate~~ every gate but the first two.** ~~The whole condition is `AND action_id "
     "!= 0x414D`, so that one~~\n"
     "~~action id is evaluated even for a unit that fails every eligibility test.~~ A `0xFFFF` id and bit `0x20` of "
     "`02089340` return 0 before the id is compared, and every later test fails over to the comparison, so that one "
     "action id is evaluated for a unit that fails any of the later tests, but never while the AI is suspended "
     "*(corrected 2026-10-02, OPUS: `00301505`–`0030150A` and `00301511`–`00301518` return 0 ahead of `00301576 mov "
     "eax, 0x414D`; CONTRACT-gambit-walk.md §4a)*. What it is, is unknown -"),

    # C-V4: propagation also needs, with a direct target, the target's +0x10 in the foe's own +0xBC8 list
    #       (00321A7D-00321AB8); the 2026-09-25 E-5 correction holds.
    (G, "                && table[combatant_id + 1] != 0)                // <-- ONLY IF ALREADY NONZERO\n",
     "                && table[combatant_id + 1] != 0)                // <-- ONLY IF ALREADY NONZERO   <- corrected "
     "2026-10-02, OPUS: and, when source_filter is non-null, only if this foe's own list at +0xBC8 (count +0xBC4, "
     "16-byte entries) holds source_filter's +0x10 (00321A7D-00321AB8); CONTRACT-enmity.md E-5\n"),
    (G, "**There is no distance check.** It walks the **entire BattleUnit slot pool** and filters on three\n"
        "things: foe class, not the direct target, and - decisively - **`table[id + 1] != 0`**.",
     "**There is no distance check.** It walks the **entire BattleUnit slot pool** and filters on ~~three~~ four\n"
     "things: foe class, not the direct target, ~~and - decisively -~~ **`table[id + 1] != 0`**, and, when there is a "
     "direct target, the target's `+0x10` in the foe's own `+0xBC8` list *(corrected 2026-10-02, OPUS: "
     "`00321A7D`–`00321AB8`; the id's class-2 validity, `00321A6A`, is a fifth; CONTRACT-enmity.md E-5)*."),
    (G, "propagates only to foes whose threat toward that character is **already nonzero**.",
     "propagates only to foes whose threat toward that character is **already nonzero** and, when there is a direct "
     "target, whose own `+0xBC8` list holds it *(corrected 2026-10-02, OPUS: `00321A7D`–`00321AB8`; "
     "CONTRACT-enmity.md E-5)*."),
    (G, "| Threat spreads only to foes already holding threat | `003219D0`",
     "| Threat spreads only to foes already holding threat and, with a direct target, listing it in their own "
     "`+0xBC8` list *(corrected 2026-10-02, OPUS: `00321A7D`–`00321AB8`)* | `003219D0`"),

    # C-V5 + C-V6: two roll sites on disjoint id bands, at most one percent draw per evaluation - 003015CB-003015D2
    #       send 0x4000-0x4166 to 00301830 and past the 003014C0 roll (00301608-00301637); in 00301830 only
    #       0x4051-0x4121 (not 0x4091) and 0x414B reach the roll (0030193B-00301962); 0x4021 (<= 0x4050) returns 1
    #       unrolled (0030191D -> 00301A31) and its handler 002FE7D0 reads the word as n x (int)(01DFE0B8 x 30.0)
    #       frames (002FE801-002FE829).
    (G, "read as a **percent chance**, rolled with the shared LCG when non-zero (`00301608`–`00301637`; Z-2); (3)",
     "read ~~as a **percent chance**, rolled with the shared LCG when non-zero (`00301608`–`00301637`; Z-2)~~ by the id "
     "it carries: a **percent chance** rolled with the shared LCG when non-zero, at `00301608`–`00301637` for an "
     "action-row id and at `0030193B`–`00301962` inside `00301830` for an order id `0x4051`–`0x4121` other than "
     "`0x4091`, or `0x414B`; every other order id draws nothing, and the wait `0x4021` reads the same word as its length, "
     "`n × (int)(01DFE0B8 × 30.0)` frames (`002FE801`–`002FE829`) *(corrected 2026-10-02, OPUS: `003015CB`–`003015D2` "
     "send ids `0x4000`–`0x4166` to `00301830` and past the first roll; `0030191D`, `00301929`, `00301935` and "
     "`00301A31` return 1 with no draw; at most one percent draw per evaluation)*; (3)"),
    (CW, "**`chance == 0` is an unconditional match, and otherwise the order fires iff `roll % 100 < chance`.**\n",
     "**`chance == 0` is an unconditional match, and otherwise ~~the order~~ an order that reaches this arm fires iff "
     "`roll % 100 < chance`.** *(corrected 2026-10-02, OPUS: the arm is reached only by `0x4051`–`0x4121` other than "
     "`0x4091` (`00301917`–`00301935`) and by `0x414B` (`00301A1B`–`00301A21`); every other order id takes an arm "
     "without a draw — the wait `0x4021` and the rest up to `0x4050`, `0x4091`, `0x4122`–`0x4123` and most ids above "
     "`0x4124` return 1 at `00301A31`, `0x4022`, `0x4124` and `0x4165` decode a goal, `0x414D` reads the stance — and an "
     "action-row id is rolled instead in `003014C0` at `00301608`–`00301637`, so one evaluation draws at most one "
     "percent roll)*\n"),
    (W, "reaches `30 × n`, where `n` is the order record's\n        second word.",
     "reaches ~~`30 × n`~~ `n × (int)(01DFE0B8 × 30.0)` — `30 × n` frames at FrameLimit 30, `60 × n` at 60, `n` "
     "seconds either way — where `n` is the order record's\n        second word, which `00301830` never rolls as a "
     "chance for this id *(corrected 2026-10-02, OPUS: `002FE801`–`002FE829` multiply the word by "
     "`cvttss2si(01DFE0B8 × 30.0)` and compare `+0x75C`; ids up to `0x4050` leave `00301830` at `0030191D` → `00301A31`, "
     "returning 1 with no draw)*."),

    # C-V7: decay is a -10 delta (mode 0) and every writer floors a positive entry at 1 (0032191D-00321923,
    #       00321C4C-00321C52); the 2026-09-25 E-6 correction holds.
    (G, "that grudge **drains away by 10 a tick** until it forgets you. While you are still engaged, it",
     "that grudge **drains away by 10 a tick** ~~until it forgets you~~ down to 1, and never to 0, so it never quite "
     "forgets you *(corrected 2026-10-02, OPUS: the write floors a positive entry at 1, " + FLOOR + "; "
     "CONTRACT-enmity.md E-6)*. While you are still engaged, it"),
    (G, "**The decay is exactly `-10`, applied to every combatant id at once**, and the interval is a",
     "**The decay is ~~exactly `-10`~~ a `-10` delta, applied to every combatant id at once**, which leaves a positive "
     "entry at 1 at least *(corrected 2026-10-02, OPUS: " + FLOOR + " floor a positive entry at 1; section 7's Z-3 "
     "box)*, and the interval is a"),
    (G, "        for every combatant id:  enmity -= 10\n",
     "        for every combatant id:  enmity -= 10   <- corrected 2026-10-02, OPUS: floored at 1 for a positive entry, "
     "never to 0 (0032191D-00321923)\n"),
    (G, "- **Decay is exactly `-10` to everyone at once**, and only while disengaged. To make enemies hold",
     "- **Decay is ~~exactly `-10`~~ a `-10` delta to everyone at once**, floored at 1 for an entry already positive "
     "*(corrected 2026-10-02, OPUS: " + FLOOR + ")*, and only while disengaged. To make enemies hold"),
    (G, "| Decay is exactly `-10` | `BattleEnmity_WriteAllCombatantIds(unit, -10, 0)` | 1 |",
     "| Decay is ~~exactly `-10`~~ a `-10` delta, floored at 1 *(corrected 2026-10-02, OPUS: " + FLOOR + ")* | "
     "`BattleEnmity_WriteAllCombatantIds(unit, -10, 0)` | 1 |"),
    (R, "that decays by exactly **-10** per interval, held",
     "that decays by ~~exactly **-10**~~ **-10** per interval down to 1, never to 0 *(corrected 2026-10-02, OPUS: "
     + FLOOR + ")*, held"),
    (CE, "disengage and walk away and it loses interest at ten a second. Attacking one foe can make its",
     "disengage and walk away and ~~it loses interest at ten a second~~ its interest drains ten a second down to a "
     "floor of 1, never to none *(corrected 2026-10-02, OPUS: " + FLOOR + "; E-6)*. Attacking one foe can make its"),

    # C-V7 + C-V8: section 7 - a first grudge seeds every zero class-2 entry to 1 in the same write (0032194B-003219A5;
    #       00321B00's twin 00321C77-00321CE3), and no writer takes a positive entry to 0 (0032191D-00321923,
    #       00321C4C-00321C52); only the keep bank's memset (the gambit page's section 8k) zeroes it.
    (CE, "An entry goes `0 → positive` only through a party-class action naming that combatant, `positive →\n"
         "lower` through another action's redistribution or through decay, and `positive → 0` only by decay\n"
         "reaching it. Propagation can move",
     "An entry goes `0 → positive` ~~only through a party-class action naming that combatant~~ through a party-class "
     "action naming that combatant, and every other zero entry valid for class 2 becomes `1` in that same write "
     "(E-6a), `positive →\n"
     "lower` through another action's redistribution or through decay, and ~~`positive → 0` only by decay~~\n"
     "~~reaching it.~~ never to 0 by any write, since every writer floors a positive entry at `1`; only the keep bank's "
     "`memset` on a non-return area entry zeroes it *(corrected 2026-10-02, OPUS: seed `0032194B`–`003219A5`, floor "
     + FLOOR + " and `00321C4C`–`00321C52`; the `memset` is the gambit page's section 8k)*. Propagation can move"),
    (CE, "and assert only the second moved. Hold engagement evidence",
     "and assert only the second moved — provided, when there is a direct target, that the second foe's `+0xBC8` list "
     "holds it; unlisted, neither moves *(corrected 2026-10-02, OPUS: `00321A7D`–`00321AB8`, E-5)*. Hold engagement "
     "evidence"),

    # C-V9: the 0x170 stride holds the 0x20 header and fourteen 24-byte records (00328160 imul r13, rax, 0x170);
    #       the rebuilders walk twelve slots (00328187 lea r15d, [r12 + 0xc]), so at most twelve are filled.
    (CW, "`AiOrderRecord`, 24 bytes, twelve per set.",
     "`AiOrderRecord`, 24 bytes, ~~twelve per set~~ room for fourteen per set (`0x170` = `0x20` + 14 × `0x18`, "
     "`00328160`), of which the rebuilders fill at most twelve (`00328187`) *(corrected 2026-10-02, OPUS)*."),
    (CW, "| `set + 0x20` | `AiOrderRecord[12]` | the records, stride 24 |",
     "| `set + 0x20` | ~~`AiOrderRecord[12]`~~ `AiOrderRecord[14]`, at most 12 filled *(corrected 2026-10-02, OPUS: "
     "`00328160`, `00328187`)* | the records, stride 24 |"),
    (W, "`0x170` bytes, twelve 24-byte order records each",
     "`0x170` bytes, ~~twelve 24-byte order records each~~ room for fourteen 24-byte order records after the `0x20` "
     "header, at most twelve filled by the rebuild *(corrected 2026-10-02, OPUS: `00328160 imul r13, rax, 0x170`, "
     "`00328187 lea r15d, [r12 + 0xc]`)*"),

    # C-V10: the navigation gate starts at 00325D90 (sole caller 00325BB0 at 00325BD0); 00325DF4 is its flag read.
    (G, "`BattleUnit_CanAdvanceCombatNavigation` (`00325DF4`); section 8g's table",
     "`BattleUnit_CanAdvanceCombatNavigation` (~~`00325DF4`~~ `00325D90`, whose `test byte ptr [rax + 4], 4` at "
     "`00325DF4` reads the bit *(corrected 2026-10-02, OPUS: the function starts at `00325D90`, its one caller "
     "`00325BD0`)*); section 8g's table"),

    # C-V12: the image settles the table - 359 qwords at 01EEC460, zero exactly at 0x4025, 0x4036-0x4045, 0x4128;
    #       0x4046/0x4047 = 002FDDA0, 0x4129-0x412F = 002FDC30; and 00301830 returns 1 for 0x4129-0x412F
    #       (00301A1B-00301A36), so the ladder does not account for the finding's second hole.
    (CW, "**The hole lists are not measuring the same thing and neither side can settle it alone.** EXP-095",
     "**The hole lists are not measuring the same thing ~~and neither side can settle it alone~~; the image settles "
     "the table** *(corrected 2026-10-02, OPUS: `01EEC460` re-read whole, below)*. EXP-095"),
    (CW, "`≥ 0x4122` to other arms, which plausibly accounts for `0x4129`–`0x412F` answering 0 with non-zero\n"
         "entries. **What that does not explain",
     "`≥ 0x4122` to other arms, ~~which plausibly accounts for `0x4129`–`0x412F` answering 0 with non-zero~~\n"
     "~~entries.~~ but `00301830` returns 1 for `0x4129`–`0x412F` (`00301A1B`–`00301A36`: above `0x4124` only "
     "`0x414B`, `0x414D` and `0x4165` go elsewhere), so the ladder does not account for the finding's second hole "
     "either *(corrected 2026-10-02, OPUS: all 359 qwords at `01EEC460` re-read — the 18 zero entries are exactly "
     "`0x4025`, `0x4036`–`0x4045` and `0x4128`; `0x4046`/`0x4047` hold `002FDDA0` and `0x4129`–`0x412F` hold "
     "`002FDC30`)*. **What that does not explain"),

    # C-S1 / C-S2: in-body PARTIAL banners against each page's front matter.
    (G, "**PARTIAL.** The selection loop, the enmity decay",
     "~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, owner "
     "re-status 2026-10-01; the paragraph is the state of 2026-09-02, as the note below says)* The selection loop, "
     "the enmity decay"),
    (R, "  **PARTIAL, tier 1.** The gambit walk",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: DOCUMENTED`)*. The gambit walk"),
    (R, "  **PARTIAL, tier 1.** Where the walk's",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. Where the walk's"),

    # C-S5 / C-S6: the evaluator ran from shipped bytes (EXP-095, 13a), the commit in commit_walk.py (section 7's
    #       2026-09-26 correction), and the bit-5 suspension was driven (case G4, section 4a).
    (CW, "- **No evaluation and no commit ran.** Nothing here says",
     "- ~~**No evaluation and no commit ran.**~~ *(answered: the evaluator `003014C0` ran from shipped bytes in EXP-095, "
     "§13a, its selector `00301AD0` scripted per slot, and the commit in `commit_walk.py`, §7's 2026-09-26 correction; "
     "2026-10-02, OPUS)* Nothing here says"),
    (CW, "- **The `02089340` bit-5 suspension (§4a) was not driven.** It sits inside\n"
         "  `AiOrder_EvaluateAndResolveActionTarget`, which is supplied here, so this run says nothing about\n"
         "  it.\n",
     "- ~~**The `02089340` bit-5 suspension (§4a) was not driven.** It sits inside~~\n"
     "  ~~`AiOrder_EvaluateAndResolveActionTarget`, which is supplied here, so this run says nothing about~~\n"
     "  ~~it.~~ *(answered: driven by execution 2026-09-26, case G4 — §4a's correction; 2026-10-02, OPUS)*\n"),

    # C-S7: answered by the 2026-09-26 reachability note directly below it.
    (CW, "Whether the unit arm\nor the slot combiner can still make a real commit refuse is open, so the parity",
     "~~Whether the unit arm~~\n~~or the slot combiner can still make a real commit refuse is open~~ *(answered: "
     "neither can, see the 2026-09-26 reachability note below; 2026-10-02, OPUS)*, so the parity"),

    # C-S8: the player-visible cause is refuted over the shipped table (the same 2026-09-26 note); the control-flow
    #       case stays.
    (CW, "act — the loop moves to the next order. This is why a gambit can visibly do nothing while its\n"
         "condition is plainly true, and a reimplementation that treats",
     "act — the loop moves to the next order. ~~This is why a gambit can visibly do nothing while its~~\n"
     "~~condition is plainly true, and~~ *(answered: not in the game — over the shipped action table a matched line is "
     "never refused by the commit, see the 2026-09-26 reachability note below; 2026-10-02, OPUS)* A reimplementation "
     "that treats"),

    # C-S9: flag 0x0004 has a reader, 00325DF4 test byte ptr [rax + 4], 4 in the gate 00325D90.
    (CW, "   `0x0004` is authored but has no reader, and",
     "   `0x0004` is authored but ~~has no reader~~ is read by the navigation gate `00325D90` at `00325DF4` *(answered: "
     "see the gambit page's section 8g table, corrected 2026-10-01; 2026-10-02, OPUS)*, and"),
    (CW, "`00305D74`; `0x0004` unread, `0x0001`",
     "`00305D74`; ~~`0x0004` unread~~ `0x0004` read at `00325DF4` *(answered: the gambit page's section 8g table; "
     "2026-10-02, OPUS)*, `0x0001`"),

    # C-S10 / C-S11: section 14's three items are answered on the gambit page (loop bound 0x28, clamp 00321E40,
    #       00321B00 read 2026-09-30).
    (CE, "- The vector's exact length; the page records 40 bytes and this contract does not re-derive it.\n"
         "- Whether an entry saturates, and at what value.\n"
         "- What `00321B00` counts as an \"other relevant combatant\" — its 551 bytes are not read here.\n",
     "- ~~The vector's exact length; the page records 40 bytes and this contract does not re-derive it.~~ *(answered: "
     "40 entries, the loop bound `cmp ebx, 0x28` the gambit page reads in section 8k; 2026-10-02, OPUS)*\n"
     "- ~~Whether an entry saturates, and at what value.~~ *(answered: at 255 — the store `00321E40` clamps to 0–255, "
     "the gambit page's `00321850` row; 2026-10-02, OPUS)*\n"
     "- ~~What `00321B00` counts as an \"other relevant combatant\" — its 551 bytes are not read here.~~ *(answered: the "
     "four party slots other than the source unit, by `00321850`'s per-entry rule — the gambit page's `00321B00` row, "
     "read 2026-09-30; 2026-10-02, OPUS)*\n"),

    # C-S12: the Z-7 box - eleven relation modes, and the claim narrowed to Foe: gambits.
    (G, "      eight modes; mode 1 (`Foe:`) excludes un-provoked enemies, which is why gambits never start\n"
        "      fights.",
     "      ~~eight modes~~ eleven modes, 0–10; mode 1 (`Foe:`) excludes un-provoked enemies, ~~which is why gambits "
     "never start~~\n"
     "      ~~fights.~~ so a `Foe:` gambit never starts a fight *(answered: see section 8i's falsification pass, the "
     "eleven-mode table and its narrowed claim; 2026-10-02, OPUS)*."),

    # C-S22: both bodies were read 2026-09-18 (section 3's table rows).
    (W, "re-read; `0030F760` and `003105D0` remain unread here, as § says.",
     "re-read; ~~`0030F760` and `003105D0` remain unread here, as § says.~~ *(answered: both read 2026-09-18 (FABLE), "
     "section 3's table rows; 2026-10-02, OPUS)*"),

    # C-S23: no other writer fills a party set's header bytes.
    (W, "      - **Not read:** whether another writer fills header bytes 1–11 of a party set.",
     "      - ~~**Not read:** whether another writer fills header bytes 1–11 of a party set.~~ *(answered: none does — "
     "bytes 1–31 are born zero and stay zero, CONTRACT-gambit-walk.md §14 item 1, and no instruction outside the three "
     "rebuilders forms an address in the `02089378` array, the gambit page's section 8l status note; 2026-10-02, OPUS)*"),

    # C-S24: UQ-124 answered the two twelves.
    (W, "> config with a sixteen-bit enable mask.** The two twelves agree. **They are recorded as an\n"
        "> agreement, not as an identification**: nothing read here connects a command id to a config slot,\n"
        "> and a matching count is the weakest kind of join.",
     "> config with a sixteen-bit enable mask.** The two twelves agree. ~~**They are recorded as an~~\n"
     "> ~~agreement, not as an identification**: nothing read here connects a command id to a config slot,~~\n"
     "> ~~and a matching count is the weakest kind of join.~~ *(answered: they count different things — UQ-124, "
     "answered 2026-09-14; 2026-10-02, OPUS)*"),

    # C-S25: UQ-126 and Z-14 - the gap ids never reach the dispatcher; 01EEC460[0x14D] = 002FE840 (re-read).
    (W, "are inside the compared range but reach\nthe unhandled arm. **`0x414D` — open question Z-14 — is one of them.**",
     "are inside the compared range but ~~reach~~\n~~the unhandled arm.~~ never reach the dispatcher *(answered: "
     "UQ-126, 2026-09-14 — their order-table slots point to other handlers, and `0x4128`'s is null; 2026-10-02, OPUS)*. "
     "~~**`0x414D` — open question Z-14 — is one of them.**~~ *(answered: Z-14, 2026-09-12 — `01EEC460[0x14D]` is the "
     "stance-flip handler `002FE840`; 2026-10-02, OPUS)*"),
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
