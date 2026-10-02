"""apply_11party.py [--apply] - 11-Party readiness map (cloud-reports/re-readiness/11-party.md), section 3.1
value contradictions C-V1..C-V27 and the section 3.2 stale / banner items, settled on the pages at the bytes (OPUS,
2026-10-02).

Each edit strikes the side the image or the shipped data REFUTES and restates it, tagged *(corrected 2026-10-02, OPUS:
...)* with the deciding address, or marks a stale open claim *(answered: see ...; 2026-10-02, OPUS)*.
Two map items flip against the map's favoured reading: C-V17 (the page's "NOT bit 1" is right, the subtree note's
`ebx & 1` is wrong) and C-V19 (the licence board is granted when LP is NOT 0xFFFF, so the three-to-one majority is
wrong). C-V20 favours the page: the TSV's four extra "roster writers" write the 16-qword array at 0209A210.
C-V10 and C-V12 favour neither side fully; each wrong figure is struck where it is stated.
X1 (map S-3): the `0036FFE0` pair and the `[0208E6B8]` store belong to `0023B200`, not `0023B040`.
X2: CONTRACT-party-focus's `003594D4` is a mid-instruction artefact of `003594D3`.
X3: the battle-state contract repeats C-V24's "descriptors inside the block".
Left out: C-B15 (review dates / template comment), C-B24 (not settled by the image), the field map's front-matter
count (a YAML multi-line scalar; a comment there would end the scalar - the body counts are corrected instead), the
1,115 / 1,114 script-corpus count (C-B19's second half, not settled by the image).
Every ~~ span opens and closes on one line; code-block lines get a trailing `<- corrected` comment instead of a strike
(their OLD includes the line end, so NEW never contains OLD). No front-matter edits; one heading change (AP §2b,
carrying "OPUS").
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "11-Party/"
R = F + "README.md"
RP = F + "party-roster-and-control-suppression.md"
AP = F + "active-party-reserve-and-the-moment-the-leader-changes.md"
FM = F + "the-five-parallel-slot-maps.md"
SS = F + "the-setsavedata-presets-test-battle-scenarios.md"
CS = F + "CONTRACT-party-slot-assignment.md"
CF = F + "CONTRACT-party-focus-and-control-suppression.md"
C5 = F + "CONTRACT-the-five-parallel-slot-maps.md"
FMP = F + "Battle-State-Block/the-battle-state-block-field-map.md"
CB = F + "Battle-State-Block/CONTRACT-battle-state-block.md"
TSV = F + "party-roster-slots-accesses.tsv"

T = "*(corrected 2026-10-02, OPUS: "
ROSTER16 = ("not a roster write - corrected 2026-10-02, OPUS: the store goes through lea [0209A210] with the index "
            "clamped to 0..15, the 16-qword array after the 32-byte roster at 0209A1F0")

EDITS = [
    # C-V1: an out-of-range slot is stored past the array - 00269CDD test ebx, ebx / js is the only guard before
    #       00269CE1 mov [rsi + rbx*8], rdi; the cmp ebx, 3 / ja at 00269C8C, 00269CF6, 00269D1C guard the notices.
    (CS, "steps 2 and 5 are skipped but **step 6 still runs**, so the",
     "~~steps 2 and 5 are skipped but~~ step 2 is skipped, step 5 still stores past the array " + T + "`00269CDD`, "
     "`00269CE1`; below)*, and **step 6 still runs**, so the"),
    (CS, "it holds a slot that does not exist, and no array entry points at it. Nothing reports this.",
     "it holds a slot that does not exist, ~~and no array entry points at it~~ while `roster[slot]`, past the four "
     "entries, points at it " + T + "`00269CDD test ebx, ebx` / `js` is the only guard before the store `00269CE1`; "
     "the `cmp ebx, 3` / `ja` at `00269C8C`, `00269CF6` and `00269D1C` guard only the two notices and the focus "
     "request — §7 step 5)*. Nothing reports this."),
    (CS, "and a slot past the fourth shows the roster is not written there |",
     "~~and a slot past the fourth shows the roster is not written there~~ while a slot past the fourth is stored past "
     "the array " + T + "`00269CDD` `js` is the only guard before `00269CE1`; §7 step 5)* |"),

    # C-V2: the occupant displaced from the NEW slot keeps +0x12 / +0x0F (00269C91-00269CAD only notify it); the reset
    #       at 00269CD5 / 00269CD9 is on the record in the actor's OLD slot.
    (RP, "membership is stored twice — in the roster array and on the actor — and assignment keeps both\n"
         "consistent, clearing the actor's previous slot before taking the new one.",
     "membership is stored twice — in the roster array and on the actor — and assignment ~~keeps both~~\n"
     "~~consistent,~~ keeps them consistent for the actor it moves, clearing the actor's previous slot before taking "
     "the new one; the occupant it displaces keeps its `+0x12` and `+0x0F` while `roster[slot]` names the newcomer "
     + T + "`00269C91`–`00269CAD` only notify that occupant; the reset at `00269CD5`/`00269CD9` hits the record in "
     "the actor's old slot — CONTRACT-party-slot-assignment.md §4)*."),
    (RP, "     -> clear the incoming actor's previous slot, set old occupant +0x12 = 0xFF\n",
     "     -> clear the incoming actor's previous slot, set old occupant +0x12 = 0xFF   <- corrected 2026-10-02, OPUS - "
     "the record reset (+0x12 = 0xFF, +0x0F = 3 at 00269CD5/00269CD9) is the one in the incoming actor's OLD slot; "
     "the occupant displaced from the new slot keeps both bytes\n"),

    # C-V3: only bytes 0x80-0xFE assign - 0026673E jns skips the block before the 0xFF test at 00266740.
    (RP, "(re)initialised with a slot byte `al` other than `0xFF` (`00266740`–`00266792`): it reads the",
     "(re)initialised with a slot byte `al` ~~other than `0xFF`~~ in `0x80`–`0xFE` " + T + "`0026673E jns` skips the "
     "block for a byte without bit 7, before the `0xFF` test at `00266740`)* (`00266740`–`00266792`): it reads the"),
    (CS, "| `al` = slot byte, `0xFF` to skip |",
     "| `al` = slot byte, ~~`0xFF` to skip~~ only `0x80`–`0xFE` assign " + T + "`0026673E jns` skips a byte without "
     "bit 7 before the `0xFF` test at `00266740`; §7)* |"),

    # C-V4: the vacated record also gets +0x0F = 3 (00269CD9); the body continues past the stamp (00269CF6-00269D41).
    (CS, "        if (prev) prev->partySlot = (int8_t)0xFF;           /* 00269CD5 */\n",
     "        if (prev) prev->partySlot = (int8_t)0xFF;           /* 00269CD5 */   /* <- corrected 2026-10-02, OPUS - "
     "00269CD9 also stores prev->+0x0F = 3 */\n"),
    (CS, "    actor->f0F = (uint32_t)slot > 3 ? 3 : 2;                /* 00269CEE-00269CF3 */\n",
     "    actor->f0F = (uint32_t)slot > 3 ? 3 : 2;                /* 00269CEE-00269CF3 */   /* <- corrected 2026-10-02, "
     "OPUS - the body continues: for a slot <= 3 the new occupant's +0x152 = 0 and 002681E0 (00269CF6-00269D17), then "
     "003594B0(003589B0(actor)) when 003590D0() == 0 (00269D1C-00269D41) */\n"),

    # C-V5: the refresher 003266C0 writes maps 1-4 through rdi = block + 0x5A48 (003266D4), 00326717-0032674B and its
    #       mode arms; callers 00233CF0, 003261D0 (003264BF), 003273D0 (003277CF).
    (FM, "> **Within this instrument's reach, nothing writes maps 1–4 after the copy.** Only map 0 has a second",
     "> **~~Within this instrument's reach, nothing writes maps 1–4 after the copy.~~** " + T + "the refresher "
     "`003266C0` writes all four through `rdi = block + 0x5A48` — `00326717`, `00326720`, `0032673E`, `00326747` and "
     "its mode arms; the 2026-09-14 correction below)* Only map 0 has a second"),
    (FM, "**So the claim is not \"no displacement-addressed write\" but \"no write, by any of three encodings\"** —",
     "**~~So the claim is not \"no displacement-addressed write\" but \"no write, by any of three encodings\"~~** "
     + T + "there is a write — `003266C0` holds `block + 0x5A48` in `rdi` (`003266D4 add rdi, 0x5a48`) and stores "
     "into maps 1–4 at `00326717`–`0032674B` and in its mode arms; none of the three instruments keyed on a map-0 base "
     "held in a register)* —"),
    (AP, "initialiser fills before duplicating. **Nothing was found that writes maps 1–4 after the copy**, so\n"
         "\"allowed to drift\" asserted a freedom the evidence does not show.",
     "initialiser fills before duplicating. ~~**Nothing was found that writes maps 1–4 after the copy**, so~~\n"
     "~~\"allowed to drift\" asserted a freedom the evidence does not show.~~ " + T + "the refresher `003266C0` writes "
     "maps 1–4 through `rdi = block + 0x5A48` (`003266D4`), `00326717`–`0032674B` and its mode arms, so the maps do "
     "drift — the five parallel slot maps' 2026-09-14 correction)*"),
    # C-V5 + C-V7 + C-V12 in one table row.
    (AP, "| **6 reads of map 1, 2 of map 3, 0 writes to maps 1–4**; map 0's only two writes are both `0xFFFF` fill "
         "loops in initialisers |",
     "| **6 reads of map 1, ~~2 of map 3, 0 writes to maps 1–4~~** 3 of map 3 (`0031B534`, `00320824`, `00328820`); "
     "~~map 0's only two writes are both `0xFFFF` fill loops in initialisers~~ the writes it could not see are "
     "`003266C0`'s into maps 1–4 through `003266D4 add rdi, 0x5a48`, and map 0 is also written by `00329080` "
     "(`00329122`, `00329176`) " + T + "immediate scan of the five bases; the five parallel slot maps' 2026-09-14 "
     "correction)* |"),
    (AP, "> **Three instruments, three different questions, one answer: nothing writes maps 1–4 after the\n> copy.**",
     "> **~~Three instruments, three different questions, one answer: nothing writes maps 1–4 after the~~\n"
     "> ~~copy.~~** " + T + "`003266C0` writes them — `003266D4 add rdi, 0x5a48`, then `00326717`–`0032674B` and the "
     "mode arms; a register holding map 0's base was a fourth encoding none of the three asked about)*"),
    (C5, "  displacement-addressed route maps 1–4 receive bytes nowhere else — they are the same snapshot\n"
         "  taken at the last refresh, permanently identical to each other, diverging from map 0 only when\n"
         "  `003290BD` runs (the `003266DB` caveat is item 2's).",
     "  displacement-addressed route maps 1–4 ~~receive bytes nowhere else — they are the same snapshot~~\n"
     "  ~~taken at the last refresh, permanently identical to each other, diverging from map 0 only when~~\n"
     "  ~~`003290BD` runs (the `003266DB` caveat is item 2's).~~ " + T + "the refresher `003266C0` writes maps 1–4 "
     "through `rdi` and its mode arms make them differ — SM-5, CON-169, CON-170)*"),

    # C-V6: modes 3 and 5 restore map 4 (003268FD, 003267F3); mode 5 rewrites maps 1 and 2 only; mode 0 nothing.
    (FM, "> per battle runtime mode (`003268BD`–`003268DC`). One branch restores map 4 from a copy taken on entry",
     "> per battle runtime mode (`003268BD`–`003268DC`). ~~One branch restores~~ Modes 3 and 5 restore map 4 from a "
     "copy taken on entry " + T + "restores at `003268FD` (mode 3) and `003267F3` (mode 5); mode 5 rewrites only maps "
     "1 and 2 and mode 0 nothing — CONTRACT-the-five-parallel-slot-maps.md SM-5, CON-169)*"),
    (FMP, "then rewrites selectors `[0..3]` of classes 1, 2 and 4 per mode (`003268BD`–`003268DC`) | 0 / 9 |",
     "then rewrites selectors `[0..3]` of classes 1, 2 and 4 ~~per mode~~ as CONTRACT-the-five-parallel-slot-maps.md "
     "SM-5 tabulates per mode: mode 0 rewrites nothing, mode 5 only classes 1 and 2, and modes 3 and 5 first restore "
     "class 4 from a copy taken on entry " + T + "mode arms `003269D2`, `00326991`, `003268F3`, `0032683F`, "
     "`00326783`; restores `003268FD`, `003267F3`)* (`003268BD`–`003268DC`) | 0 / 9 |"),

    # C-V7: map 0 is written by the reset loop (00237107), 00329CC0 and 00329080 (00329122, 00329176).
    (FM, "**Map 0's only two writes are `0xFFFF` fill loops in two initialisers**, read to confirm rather than",
     "**~~Map 0's only two writes are `0xFFFF` fill loops in two initialisers~~** Map 0 is written by the reset's "
     "`0xFFFF` loop (`00237107`), the initialiser `00329CC0` and `00329080` (`00329122`, `00329176`) " + T
     + "displacement scan of `+0x5A48`–`+0x5A59` and the immediate `0x5A48`; this page's own map-0 row names "
     "`00329080`)*, read to confirm rather than"),
    (C5, "  `00329DF6`–`00329E27`). The only other map write is `003290BD`, which mutates **map 0 only**",
     "  `00329DF6`–`00329E27`). The only other map write is ~~`003290BD`~~ `00329080` " + T + "`003290BD` is an "
     "instruction inside `00329080`; its stores are `00329122` and `00329176`)*, which mutates **map 0 only**"),

    # C-V8: the authored table is 01EED260 (00329CE1, 00329DBB); nothing references 01EC9260.
    (C5, "  table at `0x01EC9260` (nine slots, each gated through `00322C50` kinds `0x17`/`2`, resolving",
     "  table at ~~`0x01EC9260`~~ `01EED260` " + T + "`00329CE1`, `00329DBB`; nothing references `01EC9260` — the "
     "item above)* (nine slots, each gated through `00322C50` kinds `0x17`/`2`, resolving"),

    # C-V9: 003266DB is mov [rsp + 0x68], r12 inside 003266C0; the .rdata records are unwind data (CON-170).
    (C5, "  1–4, and `003290BD`'s indexed writes into map 0 only. But one registered handler escapes that\n"
         "  census: `003266DB` (dispatched via `.rdata` records — two identical `{rva32, aux}` slots — no\n"
         "  direct caller) shuffles a **caller-supplied five-map record** with the identical `0x12` stride\n"
         "  layout (`[rdi]`→`[rdi+0x12]`, `[rdi]`→`[rdi+0x36]`, `[rdi+0x12]`→`[rdi+0x24]`/`+0x48`) while\n"
         "  reading the *block's* map-0/`+0x5AA4` through `*(02EBF190)`. If the dispatch machinery ever\n"
         "  hands it `block+0x5A48`, its writes land in the block's maps 1–4 — the computed-pointer write\n"
         "  the item asks about. What record the dispatch hands it is a runtime-identity question the image\n"
         "  does not answer.",
     "  1–4, and ~~`003290BD`'s~~ `00329080`'s indexed writes into map 0 only. ~~But one registered handler escapes "
     "that~~\n"
     "  ~~census: `003266DB` (dispatched via `.rdata` records — two identical `{rva32, aux}` slots — no~~\n"
     "  ~~direct caller) shuffles a **caller-supplied five-map record** with the identical `0x12` stride~~\n"
     "  ~~layout (`[rdi]`→`[rdi+0x12]`, `[rdi]`→`[rdi+0x36]`, `[rdi+0x12]`→`[rdi+0x24]`/`+0x48`) while~~\n"
     "  ~~reading the *block's* map-0/`+0x5AA4` through `*(02EBF190)`. If the dispatch machinery ever~~\n"
     "  ~~hands it `block+0x5A48`, its writes land in the block's maps 1–4 — the computed-pointer write~~\n"
     "  ~~the item asks about. What record the dispatch hands it is a runtime-identity question the image~~\n"
     "  ~~does not answer.~~ " + T + "`003266DB` is `mov qword ptr [rsp + 0x68], r12` inside `003266C0`, the "
     "`.rdata` records are its unwind data, and `003290BD` is an instruction inside `00329080` — the answer above, "
     "CON-170)*"),
    (C5, "from the selector table `0x01EC9260`; `003290BD` writes map 0 only; `003266DB` (dispatch-registered, no direct "
         "caller) writes a same-layout record through caller-supplied `rdi` | 1 |",
     "from the selector table ~~`0x01EC9260`~~ `01EED260`; ~~`003290BD`~~ `00329080` writes map 0 only; ~~`003266DB` "
     "(dispatch-registered, no direct caller) writes a same-layout record through caller-supplied `rdi`~~ " + T
     + "`00329CE1`/`00329DBB` address `01EED260`; `003290BD` and `003266DB` are instructions inside `00329080` and "
     "`003266C0` — CON-170)* | 1 |"),

    # C-V10: 32 call sites (0031B9F0 direct 1, 0031FE70 1, 00320040 5, 00320AB0 25), 31 constant - class 3 x24,
    #        1 x4 (0030A707, 002F8C4E, 0030C337, 0031117A), 0 x2 (0030FD44, 002738B8), 2 x1 (0035BDBE); computed only
    #        0030A804. The 0050FD1A family passes class 3 (0050FD15 mov edx, 3).
    (AP, "scanning the wrappers' own call sites gives **31 sites, 23 of them passing a constant**:",
     "scanning the wrappers' own call sites gives ~~**31 sites, 23 of them passing a constant**~~ **32 sites, 31 of "
     "them passing a constant** " + T + "`retool.py callers` on `0031B9F0`, `0031FE70`, `00320040` and `00320AB0` "
     "gives 1 + 1 + 5 + 25 sites; only `0030A804` passes a computed class)*:"),
    (AP, "| **0** | `0x5A48` | `Equipment_UnequipEncodedItemFromActiveRoster` (`0030FD10`) |",
     "| **0** | `0x5A48` | `Equipment_UnequipEncodedItemFromActiveRoster` (`0030FD10`) and `00273880` (`002738B8`, "
     "through `0031FE70`) " + T + "`002738B6 xor ecx, ecx` is the class argument of the swapping wrapper)* |"),
    (AP, "| **3** | `0x5A7E` | **fourteen sites**:",
     "| **3** | `0x5A7E` | ~~**fourteen sites**~~ **24 sites** " + T + "20 through `00320AB0`, one of them after "
     "`0050FF39 mov ebx, 3`, and 4 through `00320040`)*:"),
    (AP, "**Class 0 naming itself is the strongest of the three**: its single caller is",
     "**Class 0 naming itself is the strongest of the three**: ~~its single caller is~~ one of its two callers " + T
     + "the other is `00273880` at `002738B8`)* is"),
    (AP, "**Classes 2 and 4 are unreached, not absent.** Eight of the 31 sites pass the class through from their\n"
         "own caller, so a constant for either could exist one level further up; the census establishes that\n"
         "**no site passes 2 or 4 directly**, which is weaker than \"nothing uses them\" and is stated as such.",
     "~~**Classes 2 and 4 are unreached, not absent.** Eight of the 31 sites pass the class through from their~~ "
     "**Class 4 is unreached, not absent; class 2 is passed at `0035BDBE`.** One of the 32 sites, `0030A804`, passes "
     "the class through from its\n"
     "own caller, so a constant for ~~either~~ class 4 could exist one level further up; the census establishes that\n"
     "**no site passes ~~2 or~~ 4 directly** " + T + "the class census above, re-run on all four entries; class 2 is "
     "the battle menu's member map, §2b's row)*, which is weaker than \"nothing uses them\" and is stated as such."),
    (C5, "  `002F8C4E`/`0030C337`/`00311A17`), **2**",
     "  `002F8C4E`/`0030C337`/~~`00311A17`~~`0031117A` " + T + "`00310DB0`'s call is at `0031117A`)*), **2**"),
    (C5, "  ~19 sites through wrappers `00320AB0`/`00320040`, which forward `edx`/`ecx` respectively);",
     "  ~19 sites " + T + "24 — 20 through `00320AB0`, one of them after `0050FF39 mov ebx, 3`, and 4 through "
     "`00320040`)* through wrappers `00320AB0`/`00320040`, which forward `edx`/`ecx` respectively);"),
    (C5, "computed `edx` at `0030A804` and\n  the `0050FD1A` family.",
     "computed `edx` at `0030A804` ~~and~~\n  ~~the `0050FD1A` family~~ " + T + "`0050FD15 mov edx, 3` and its "
     "siblings pass class 3)*."),
    (C5, "class 3 dominant (~19 sites), class 1 ×4, class 0 ×2, class 2 ×1 (`0035BDBE`); class 4 only via computed "
         "`edx` | 1 |",
     "class 3 dominant (~19 sites " + T + "24 constant sites, and class 4's one computed site is `0030A804`, of 32)*), "
     "class 1 ×4, class 0 ×2, class 2 ×1 (`0035BDBE`); class 4 only via computed `edx` | 1 |"),

    # C-V11: 00321100 returns the first index whose byte IS 0xFF (00321139 cmp / 0032113D je 00321158 mov eax, ebx).
    (FM, "index whose `byte[base + rbx*2 + 0x5A86]` is not `0xFF` returns",
     "index whose `byte[base + rbx*2 + 0x5A86]` ~~is not `0xFF`~~ is `0xFF`, or whose class-`0x17` check fails, "
     "returns " + T + "`00321139 cmp byte ptr [rdi + rax], 0xff` / `0032113D je 0x321158`, and `00321158 mov eax, "
     "ebx`; a non-`0xFF` byte continues the loop at `0032113F`)*"),

    # C-V12: the immediate 0x5A5A is indexed at six sites (all reads), 0x5A7E at three.
    (FM, "Seven such sites exist for map 1 alone, in",
     "~~Seven~~ Six " + T + "`0031AC11`, `0031B5CD`, `00326573`, `00326B2F`, `00326BEE`, `00328E0D`)* such sites "
     "exist for map 1 alone, in"),
    (FM, "| register-held-offset scan | is a base loaded as an **immediate** and indexed? | **8 reads, 0 writes** |",
     "| register-held-offset scan | is a base loaded as an **immediate** and indexed? | **~~8 reads, 0 writes~~** 9 "
     "reads, 6 of map 1 and 3 of map 3, and no write through a map 1–4 base; the writes it could not see go through "
     "the map-0 base `003266D4 add rdi, 0x5a48` " + T + "immediate scan of `0x5A5A`, `0x5A6C`, `0x5A7E` and "
     "`0x5A90`; the 2026-09-14 correction above)* |"),

    # C-V13: a guest takes the first free roster index of 3, 2, 1 (0031711A mov ebx, 3; 0031714F-00317157).
    (AP, "selector 7..25   a guest               -> placed at a \"primary\" index\n",
     "selector 7..25   a guest               -> placed at a \"primary\" index   <- corrected 2026-10-02, OPUS - the "
     "first free roster index of 3, 2, 1, never 0 (003170E0: 0031711A mov ebx, 3; 0031714F-00317157), section 9\n"),

    # C-V14: three handle writers on an unbounded scan too (00358B6B, 00358C2F, 003590FD).
    (AP, "four in reality** — because the difference is the finding in §4, not a correction to be tidied away.",
     "~~four in reality~~ and three in reality** " + T + "an unbounded `.text` scan finds only `00358B6B`, `00358C2F` "
     "and `003590FD`; the write the function list misses is to the kind byte `022C7FF8`, at `003594D3` — "
     "CONTRACT-party-focus-and-control-suppression.md PF-1)* — ~~because the difference is the finding in §4, not a "
     "correction to be tidied away~~."),

    # C-V15: 022C7FF8 has seven sites; the unbounded scan adds two (003594C0 read, 003594D3 write).
    (AP, "**An unbounded `.text` scan found a\ntenth site my census had no way to reach**",
     "**An unbounded `.text` scan found ~~a~~\n~~tenth site~~ two more sites, seven in all, my census had no way to "
     "reach** " + T + "`003594C0` reads and `003594D3` writes `022C7FF8`; the other five are `00358BC4`, "
     "`00358C05`, `00358C35`, `00359109` and `003594B6` — CONTRACT-party-focus-and-control-suppression.md PF-1)*"),

    # C-V16: 28 call sites in 25 functions (retool.py callers 003272A0).
    (AP, "> fresh on every one of twenty-five call sites, never stored, never announced. Changing leader is a",
     "> fresh on every one of ~~twenty-five call sites~~ twenty-eight call sites in twenty-five functions " + T
     + "`retool.py callers 003272A0`; CONTRACT-party-focus-and-control-suppression.md PF-2)*, never stored, never "
     "announced. Changing leader is a"),

    # C-V17 + X1: 0023B1E1 shr ebx, 1 / 0023B1E3 not ebx / 0023B1E5 and ebx, 1 publish NOT bit 1; 0023B040 ends at
    #       0023B1FA jmp / 0023B1FF int3, and the 0036FFE0 calls and the [0208E6B8] store are 0023B200's.
    (RP, "`00313F60`/`003592C0`/`00359200`/`0036FFE0` ×2, `[0208E6B8]` store\n"
         "(`0023B22F`–`0023B238`), then tail `0026BD40` publishes `ebx & 1` into",
     "`00313F60`/`003592C0`/`00359200`~~/`0036FFE0` ×2, `[0208E6B8]` store~~\n"
     "~~(`0023B22F`–`0023B238`),~~ then tail `0026BD40` publishes ~~`ebx & 1`~~ the inverse of bit 1 of `ebx` " + T
     + "`0023B1E1 shr ebx, 1` / `0023B1E3 not ebx` / `0023B1E5 and ebx, 1` before the tail; the `0036FFE0` pair and "
     "the `[0208E6B8]` store at `0023B22F`–`0023B238` belong to the next function, `0023B200`, past this one's last "
     "instruction at `0023B1FA` — §2's correction block already says NOT bit 1)* into"),
    (RP, "`00359200`,\n`0036FFE0`.",
     "`00359200`~~,~~\n~~`0036FFE0`~~ " + T + "`0036FFE0` is called by `0023B200` at `0023B204` and `0023B221`, not "
     "by `0023B040`)*."),

    # C-V18: 00359200 writes 022C8000 (00359204) and resolves 022C7FE0 (0035922B).
    (RP, "mask setter itself — `ecx` nonzero sets bit `edx` of `dword[022C6FFC]` via",
     "mask setter itself — `ecx` nonzero sets bit `edx` of ~~`dword[022C6FFC]`~~ `dword[022C8000]` " + T
     + "`00359204` resolves to `022C8000`, as the correction at this section's end says)* via"),
    (RP, "when the mask is nonzero it resolves `003588B0(dword[022C6FF0])` and tails",
     "when the mask is nonzero it resolves ~~`003588B0(dword[022C6FF0])`~~ `003588B0(dword[022C7FE0])` " + T
     + "`0035922B` loads `022C7FE0`)* and tails"),

    # C-V19: the licence board is granted when LP is NOT 0xFFFF and the slot is <= 6 - 00239A8C mov r14d, 0xffff,
    #        00239B64 mov r13d, r14d; 00239C49 cmp r14d, 6 / jg; 00239C4F cmp word [rbp + 0x20], r13w / 00239C54 jne
    #        00239CE1 (the board loop); equal takes 00239C5D call 0016D6A0 (ret 0).
    (SS, "217 of 226 presets carry LP `0xFFFF` (the licence-mask path), 9 carry a number",
     "217 of 226 presets carry LP `0xFFFF` ~~(the licence-mask path)~~ (no licence grant), 9 carry a number " + T
     + "`00239C4F cmp word ptr [rbp + 0x20], r13w` with `r13w = 0xFFFF` (`00239A8C`, `00239B64`), then `00239C54 jne "
     "0x239ce1`, the board loop — it runs when LP is NOT `0xFFFF`; an LP of `0xFFFF` takes `0016D6A0`, a bare `ret "
     "0`)*"),
    (SS, "(`0xFFFF` = grant the board's per-slot mask instead)",
     "(~~`0xFFFF` = grant the board's per-slot mask instead~~ any value but `0xFFFF` grants the board's per-slot "
     "mask, for battle slots ≤ 6 " + T + "`00239C49`–`00239C54`)*)"),
    (SS, "                       u8 zero[16] ; u16 lp (0xFFFF = board mask) ; u8 zero[6] ; u8 mpPercent ; u8 zero[3]\n",
     "                       u8 zero[16] ; u16 lp (0xFFFF = board mask) ; u8 zero[6] ; u8 mpPercent ; u8 zero[3]   "
     "<- corrected 2026-10-02, OPUS - the board mask is granted when lp != 0xFFFF and the slot is <= 6 "
     "(00239C49-00239C54)\n"),
    (SS, "licence grant   = every 02EBF038 row with (row[+7] >> battleSlot) & 1, when lp == 0xFFFF\n",
     "licence grant   = every 02EBF038 row with (row[+7] >> battleSlot) & 1, when lp == 0xFFFF   <- corrected "
     "2026-10-02, OPUS - when lp != 0xFFFF and battleSlot <= 6 (00239C49 cmp r14d, 6 / jg; 00239C4F / 00239C54 jne "
     "00239CE1)\n"),

    # C-V20: the TSV's four extra "roster writers" store into the 16-qword array at 0209A210 (lea at 00266E01,
    #        00269605, 0026AD99 / 0026ADB2, 0026CEF2; index clamped 0..15). The page's five writers stand.
    (TSV, "00266D10\tFUN_00266d10\t00266E1B\t0x0\tw\tmov qword ptr [r8 + rax*8], rsi\tarray 0209A1F0 reg\t\n",
     "00266D10\tFUN_00266d10\t00266E1B\t0x0\tw\tmov qword ptr [r8 + rax*8], rsi\tarray 0209A1F0 reg\t" + ROSTER16
     + " (lea at 00266E01)\n"),
    (TSV, "002695A0\tFUN_002695a0\t00269628\t0x0\tw\tmov qword ptr [r9 + rcx*8], rdx\tarray 0209A1F0 reg\t\n",
     "002695A0\tFUN_002695a0\t00269628\t0x0\tw\tmov qword ptr [r9 + rcx*8], rdx\tarray 0209A1F0 reg\t" + ROSTER16
     + " (lea at 00269605)\n"),
    (TSV, "0026AD90\tFUN_0026ad90\t0026ADA0\t0x0\tw\tmov qword ptr [rcx + rax*8], rdx\tarray 0209A1F0 reg\t\n",
     "0026AD90\tFUN_0026ad90\t0026ADA0\t0x0\tw\tmov qword ptr [rcx + rax*8], rdx\tarray 0209A1F0 reg\t" + ROSTER16
     + " (lea at 0026AD99)\n"),
    (TSV, "0026AD90\tFUN_0026ad90\t0026ADB9\t0x0\tw\tmov qword ptr [rcx + rax*8], rdx\tarray 0209A1F0 reg\t\n",
     "0026AD90\tFUN_0026ad90\t0026ADB9\t0x0\tw\tmov qword ptr [rcx + rax*8], rdx\tarray 0209A1F0 reg\t" + ROSTER16
     + " (lea at 0026ADB2)\n"),
    (TSV, "0026CE60\tActorSystem_InitializeManagerRuntime\t0026CF13\t0x0\tw\tmov qword ptr [r8 + rax*8], rbp\t"
          "array 0209A1F0 reg\t\n",
     "0026CE60\tActorSystem_InitializeManagerRuntime\t0026CF13\t0x0\tw\tmov qword ptr [r8 + rax*8], rbp\t"
     "array 0209A1F0 reg\t" + ROSTER16 + " (lea at 0026CEF2)\n"),
    (RP, "census below is image-wide for the roster's writers: the party verb path, this initialiser, and",
     "census below is image-wide for the roster's writers: the party verb path, this initialiser, ~~and~~ the clears "
     "`002695A0` and `0025BFB0` (bit-0 arm) " + T + "five writers, CONTRACT-party-slot-assignment.md §15 — "
     "`002695AF`/`002695B7` and `0025C017`/`0025C01F` are the other two 32-byte clears)*, and"),

    # C-V21: the published TSV holds 1,135 rows / 215 functions / 166 offsets; 683 / 100 / 105 in +0x8-+0x4747.
    (FMP, "applying at `+8 + d` for record 0. The scan attributes 835 accesses in 130 functions to that range\n"
          "(111 offsets)",
     "applying at `+8 + d` for record 0. The scan attributes ~~835 accesses in 130 functions~~ 683 accesses in 100 "
     "functions to that range\n(~~111 offsets~~ 105 offsets " + T + "counted in the published "
     "`battle-state-block-accesses.tsv`, displacements `0x8`–`0x4747`)*)"),
    (FMP, "(1,145 rows; 91 removed 2026-09-13",
     "(~~1,145 rows~~ 1,135 rows, 215 functions, 166 offsets " + T + "counted in the file)*; 91 removed 2026-09-13"),

    # C-V22: 00313840 clears bits 0 and 1 of +0x5AD0 (0031388B and 0xFFFE, 0031389E and 0xFFFD).
    (FMP, "bit 2 cleared by `00313840`;",
     "~~bit 2 cleared by `00313840`~~ bit 0 cleared by `00313840` with bit 1 " + T + "`0031388B and word ptr [rax + "
     "0x5ad0], cx` with `cx = 0xFFFE`, `0031389E` with `0xFFFD`)*;"),
    (FMP, "`+0x5AD0` bits 1–2 cleared, both timers zeroed)",
     "`+0x5AD0` ~~bits 1–2~~ bits 0 and 1 " + T + "`0031388B`, `0031389E`)* cleared, both timers zeroed)"),

    # C-V23: 120 banks of 0x34 from +0x5B10 end at +0x736F (00327C63-00327C7C).
    (FMP, "and the gambit banks (`+0x5B10`–`+0x7373`).",
     "and the gambit banks (`+0x5B10`–~~`+0x7373`~~`+0x736F` " + T + "`0x5B10 + 120 × 0x34 = 0x7370`, the selection "
     "array's start; `00327C63`–`00327C7C`)*)."),

    # C-V24 + X3: block +0x57C8 is class 7's second region; the descriptors are static at 01EEBCC0 (row 2 field +0x18
    #       = 0x57C8; 0030B702-0030B737 zero 0x200 bytes there).
    (FMP, "inventory descriptors (`+0x53C54` = block `+0x57C8`) and the gambit banks **inside** it; that page's",
     "~~inventory descriptors~~ the inventory region it calls the descriptors (`+0x53C54` = block `+0x57C8`, class 7's "
     "second region, the descriptors themselves being static at `01EEBCC0` " + T + "descriptor row 2 names `+0x57C8` "
     "at its `+0x18`, and `0030B702`–`0030B737` zero `0x200` bytes there; FO-5)*) and the gambit banks **inside** it; "
     "that page's"),
    (FMP, "  +0x57C8  inventory class descriptors         +0x5AE0..+0x5AEF  mode-ladder words\n",
     "  +0x57C8  inventory class descriptors         +0x5AE0..+0x5AEF  mode-ladder words   <- corrected "
     "2026-10-02, OPUS - +0x57C8 is class 7's second region, not the descriptors, which are static at 01EEBCC0; "
     "0030B702-0030B737 zero it\n"),
    (CB, "inventory descriptors — is save state rather than session state.*",
     "~~inventory descriptors~~ inventory count arrays — is save state rather than session state.* " + T + "the class "
     "descriptors are static at `01EEBCC0`; the rebaser `0030B6A0` writes block-relative pointers into them — the "
     "field map §2.8)*"),
    (CB, "The inventory descriptors inside it are rebased\non every bind.",
     "The inventory descriptors ~~inside it~~ that point into it " + T + "they are static at `01EEBCC0`, `0030B6A8`)* "
     "are rebased\non every bind."),

    # C-V25: shipped presets (battle_pack.bin directory +0xF0, bound to 02EBF028 at 00236FBC / 00236FC3): MP % 100 in
    #        220 rows, 80 in four, 70 in two.
    (SS, "(100 in every row). Shipped:",
     "~~(100 in every row)~~ (100 in 220 rows, 80 in four and 70 in two " + T + "re-read from the shipped "
     "`battle_pack.bin` directory `+0xF0`, bound to `02EBF028` at `00236FBC`–`00236FCA`; §10)*). Shipped:"),
    (SS, "- The MP percentage is the only per-preset number every shipped row leaves at 100.",
     "- ~~The MP percentage is the only per-preset number every shipped row leaves at 100.~~ The MP percentage is 100 "
     "in 220 of the 226 shipped rows; four are 80 and two are 70 " + T + "§10, re-read from the shipped "
     "`battle_pack.bin`)*."),

    # C-V26: the block is 0x7410 bytes (002370CD mov r8d, 0x7410).
    (FM, "**Size: bounded, not measured.** `0x4E68C + 0x8004 = 0x56690`, the buffer's end, so `0x8004` is the\n"
         "**maximum extent**. The highest field anyone has read is `+0x5B04`, giving a floor of `0x5B08`. The",
     "**~~Size: bounded, not measured.~~** **Size: `0x7410`, measured** " + T + "the reset `002370C0` clears `mov "
     "r8d, 0x7410` bytes at `002370CD`, and the last field is the selection array `+0x7370`–`+0x740F` — the "
     "battle-state block field map §2.1)*. `0x4E68C + 0x8004 = 0x56690`, the buffer's end, so `0x8004` is the\n"
     "**maximum extent**. ~~The highest field anyone has read is `+0x5B04`, giving a floor of `0x5B08`.~~ The"),
    (FM, "- **`0x8004` is an upper bound**, and the 9,468 bytes above `+0x5B08` are undeclared, as are 3,520\n"
         "  between the `0x1C8` array and the slot maps.",
     "- **`0x8004` is an upper bound**~~, and the 9,468 bytes above `+0x5B08` are undeclared, as are 3,520~~\n"
     "  ~~between the `0x1C8` array and the slot maps.~~ " + T + "the block is `0x7410` bytes, `002370CD`, and the "
     "battle-state block field map places every byte above the records, FO-5)*."),

    # C-V27: the class-0 arm is 0031BAAA (movzx eax, byte ptr [rax + rdi*2 + 0x5a48]).
    (FM, "| `+0x5A48` | 31 | `0031B9F0` |",
     "| `+0x5A48` | 31 | ~~`0031B9F0`~~ `0031BAAA` " + T + "the class-0 arm's load `movzx eax, byte ptr [rax + rdi*2 "
     "+ 0x5a48]`; `0031B9F0` is the entry)* |"),

    # X2: CONTRACT-party-focus's 003594D4 is the tail of the 7-byte 003594D3 store, decoded with its REX prefix dropped.
    (CF, "extra are `003594C0` and `003594D4` —",
     "extra are `003594C0` and ~~`003594D4`~~ `003594D3` " + T + "`003594D3` is the 7-byte `mov byte ptr [rip + …], "
     "r8b`; `003594D4` decodes only as its tail with the REX prefix dropped)* —"),
    (CF, "the two extra being `003594C0`/`003594D4` (PF-1)",
     "the two extra being `003594C0`/~~`003594D4`~~`003594D3` " + T + "the store begins at `003594D3`)* (PF-1)"),
    (CF, "the extra two `003594C0`/`003594D4`;",
     "the extra two `003594C0`/~~`003594D4`~~`003594D3` " + T + "the store begins at `003594D3`)*;"),

    # C-B1: README labels against each page's own front matter, and the seven pages it did not list.
    (R, "  **PARTIAL, tier 1.** The script verb",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** " + T + "the page's front matter says `status: AUDITED`)*. The "
     "script verb"),
    (R, "  **DOCUMENTED, tier 1.** The four-slot roster",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** " + T + "the page's front matter says `status: AUDITED`)*. The "
     "four-slot roster"),
    (R, "  **DOCUMENTED, tier 1.** The 0x7410-byte",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** " + T + "the page's front matter says `status: AUDITED`)*. The "
     "0x7410-byte"),
    (R, "  inventory snapshot and forty members' gambit banks. The access table is published beside it.\n\n"
        "## How to add a system here",
     "  inventory snapshot and forty members' gambit banks. The access table is published beside it.\n\n"
     "- [`active-party-reserve-and-the-moment-the-leader-changes.md`](active-party-reserve-and-the-moment-the-leader-"
     "changes.md) — the nine-entry configuration, the guest ranges and the deferred leader change — **AUDITED**\n"
     "- [`the-five-parallel-slot-maps.md`](the-five-parallel-slot-maps.md) — the five nine-entry maps the resolver "
     "`0031B9F0` selects by class — **AUDITED**\n"
     "- [`CONTRACT-party-slot-assignment.md`](CONTRACT-party-slot-assignment.md) — **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-party-focus-and-control-suppression.md`](CONTRACT-party-focus-and-control-suppression.md) — "
     "**CONTRACT READY**\n"
     "- [`CONTRACT-the-five-parallel-slot-maps.md`](CONTRACT-the-five-parallel-slot-maps.md) — **CONTRACT READY**\n"
     "- [`Battle-State-Block/CONTRACT-battle-state-block.md`](Battle-State-Block/CONTRACT-battle-state-block.md) — "
     "**CONTRACT READY**\n"
     "- *(corrected 2026-10-02, OPUS: six pages this list omitted, added with the status or readiness each page's "
     "own front matter states)*\n"
     "\n## How to add a system here"),

    # C-B2: the roster page's "not read" rows, answered on its own §2 / §9 and on the active-party page.
    (RP, "| `00269C70` | `PartyRoster_AssignActorToSlot` | ✅ read (partial body) |",
     "| `00269C70` | `PartyRoster_AssignActorToSlot` | ✅ read ~~(partial body)~~ whole *(answered: O-6, the tail read "
     "2026-09-12 — §2's tail paragraph; 2026-10-02, OPUS)* |"),
    (RP, "| — | `BattleUnit_GetPartyLeader` | not read |",
     "| — | `BattleUnit_GetPartyLeader` (`003272A0`) | ~~not read~~ read *(answered: see "
     "active-party-reserve-and-the-moment-the-leader-changes.md §4; 2026-10-02, OPUS)* |"),
    (RP, "| — | `PartyFocus_GetCurrentPackedActorHandle` | not read |",
     "| — | `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) | ~~not read~~ read *(answered: `mov eax, "
     "[022C7FE0]` / `ret` — active-party-reserve-and-the-moment-the-leader-changes.md, falsification pass 1; "
     "2026-10-02, OPUS)* |"),
    (RP, "| `0030D9A0` | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | not read |",
     "| `0030D9A0` | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | ~~not read~~ read *(answered: \"The ladder is "
     "now fully read\", §9 — the battle runtime mode ladder page; 2026-10-02, OPUS)* |"),
    (RP, "| `002E8100` / `002681E0` | *(suppression/eviction helpers)* | not read |",
     "| `002E8100` / `002681E0` | *(suppression/eviction helpers)* | ~~not read~~ `002681E0` read, `002E8100` not read "
     "*(answered for `002681E0`: see its own row above, read 2026-09-12; 2026-10-02, OPUS)* |"),

    # C-B3: mode 2 is the chocobo ride (O-4 answered; the ladder read in full).
    (RP, "unit definition and presentation alike. What mode 2 *is*, and the full `0..5` enumeration, is **not\n"
         "established** — registered as **O-4**.",
     "unit definition and presentation alike. ~~What mode 2 *is*, and the full `0..5` enumeration, is **not~~\n"
     "~~established** — registered as **O-4**.~~ *(answered: mode 2 is the chocobo ride and the ladder is read in "
     "full — O-4, the mode ladder page §2c and this page's `00303EC0` row in §3; 2026-10-02, OPUS)*"),
    (CF, "- What mode 2 is — **O-4**, and the gate PF-7's entry test depends on.",
     "- ~~What mode 2 is — **O-4**, and the gate PF-7's entry test depends on.~~ *(answered: the chocobo ride — O-4, "
     "the mode ladder page §2c; 2026-10-02, OPUS)*"),

    # C-B4: a null pBkbi faults at 0023B15E (no second null test after the 0023B152 reload).
    (RP, "        if (leader->pBkbi == NULL\n",
     "        if (leader->pBkbi == NULL   // <- corrected 2026-10-02, OPUS - not an all-suppressed arm: 0023B152 "
     "reloads +0x698 and 0023B15E reads [rax + 0x64] with no null test, so this path faults before publishing (the "
     "correction block below)\n"),

    # C-B5: O-5's answer is no - reserve members are not in a separate structure.
    (AP, "structure\") — they do,\nin the same array, at indices `4..8`.",
     "structure\") — ~~they do,~~ they do not " + T + "O-5's register verdict is no; "
     "party-roster-and-control-suppression.md §7)*: they live\nin the same array, at indices `4..8`."),

    # C-B6: class 2 is passed at 0035BDBE; only class 4 has no constant site.
    (AP, "## 2b. Which of the five maps is which — three named, two unreached",
     "## 2b. Which of the five maps is which — ~~three named, two unreached~~ four named, one unreached (corrected "
     "2026-10-02, OPUS)"),

    # C-B7: what the classes are is answered on the active-party page §2b and by SM-6.
    (FM, "## What the classes are is not established here\n\n**The resolver takes the class as a parameter",
     "## What the classes are is not established here\n\n*(answered elsewhere: classes 0 to 3 are named by their "
     "callers — active-party-reserve-and-the-moment-the-leader-changes.md §2b — and SM-6 of "
     "CONTRACT-the-five-parallel-slot-maps.md makes map 0 the live configuration and maps 1–4 derived from it; "
     "2026-10-02, OPUS)*\n\n**The resolver takes the class as a parameter"),
    (FM, "- This is what the block *is* and where it lives. **What the five classes mean is still not\n"
         "  established** — §\"What the classes are is not established here\" stands unchanged.",
     "- This is what the block *is* and where it lives. ~~**What the five classes mean is still not~~\n"
     "  ~~established** — §\"What the classes are is not established here\" stands unchanged.~~ *(answered: see "
     "active-party-reserve-and-the-moment-the-leader-changes.md §2b; 2026-10-02, OPUS)*"),

    # C-B8: the teardown re-seats camera context 0 (0025A6BE lea rax, [02097D20]; 0025A6CB imul r15, rdi, 0x860).
    (CF, "leader's stats record and its three action fields, the manager record the teardown snapshots.\n"
         "**Written outside the block:** the manager record's two `0xB0` blocks and its `+0x850` float, by the",
     "leader's stats record and its three action fields, ~~the manager record the teardown snapshots~~ camera context "
     "0, which the teardown re-seats.\n"
     "**Written outside the block:** ~~the manager record's~~ camera context 0's two `0xB0` blocks and its `+0x850` "
     "float " + T + "`0025A6BE lea rax, [02097D20]` / `0025A6CB imul r15, rdi, 0x860` — one of two `0x860`-byte "
     "camera contexts; active-party-reserve-and-the-moment-the-leader-changes.md §9)*, by the"),
    (CF, "  addresses the manager's record; PF-5 and PF-6 are about that seam.",
     "  addresses ~~the manager's record~~ camera context 0 " + T + "`0025A6BE`, the `02097D20` contexts)*; PF-5 and "
     "PF-6 are about that seam."),

    # C-B9: the blend is read (active-party §9; the interpolate 00259510 in §17).
    (CF, "  **suggestive and not read**.",
     "  ~~**suggestive and not read**.~~ *(answered: it is a blend — `00259510` is the family's spherical "
     "interpolate, §17 of this page, and active-party-reserve-and-the-moment-the-leader-changes.md §9 reads the five "
     "steps; 2026-10-02, OPUS)*"),

    # C-B10: the secondary handle's consumer is the focus update 00358EE0 (00358F1C, 00358F2F).
    (CF, "- The secondary handle `022C7FE8`: 8 accesses, 3 writers, and no consumer established here.",
     "- The secondary handle `022C7FE8`: 8 accesses, 3 writers~~, and no consumer established here~~ *(answered: the "
     "intervention camera's subject, read by the focus update `00358EE0` at `00358F1C` / `00358F2F` — "
     "active-party-reserve-and-the-moment-the-leader-changes.md §8b; 2026-10-02, OPUS)*."),

    # C-B11: the commit's frame position is answered (once a frame; thunk 00358BB0, seven callers).
    (CF, "  the commit runs is that layer's business and PF-5 asserts nothing about it.** The leader-change\n"
         "  page leaves the frame position open and this contract does not close it.",
     "  the commit runs is that layer's business and PF-5 asserts nothing about it.** ~~The leader-change~~\n"
     "  ~~page leaves the frame position open and this contract does not close it.~~ *(answered: once a frame, from "
     "whichever of the three mode frame bodies runs — active-party-reserve-and-the-moment-the-leader-changes.md §9, "
     "2026-09-18; the thunk `00358BB0` has seven callers; 2026-10-02, OPUS)*"),

    # C-B12 / C-B13 / C-B14: the slot contract's open items answered on the roster page and in its own §4.
    (CS, "- What `[secondaryContext + 0x152] = 1` means, and what `002681E0` does with it.",
     "- ~~What `[secondaryContext + 0x152] = 1` means, and what `002681E0` does with it.~~ *(answered: the roster-role "
     "byte, which `002681E0` turns into the movement body's cell class — O-1, "
     "party-roster-and-control-suppression.md §7; 2026-10-02, OPUS)*"),
    (CS, "7. Continue at `00269CF6` with a further pass over `roster[rbx]` — outside this contract.",
     "7. Continue at `00269CF6` with a further pass over `roster[rbx]` ~~— outside this contract~~ *(answered: the new "
     "occupant's notice and the focus request, read 2026-09-12 — party-roster-and-control-suppression.md §2, the tail "
     "paragraph; 2026-10-02, OPUS)*."),
    (CS, "> one of them has now been read closely. Treat the remaining two as **inherited and unverified**.",
     "> one of them has now been read closely. ~~Treat the remaining two as **inherited and unverified**.~~ "
     "*(answered: all three were disassembled 2026-09-25 and none touches a record's `+0x12` or `+0x0F` — §4; "
     "`002695A0` re-read 2026-10-02: after the two stores `002695AF`/`002695B7` it only calls and fills the 16-qword "
     "array at `0209A210`; 2026-10-02, OPUS)*"),

    # C-B16: the initialiser and both removers were executed (OPUS blocks 338 / 340); the resolver was not.
    (C5, "**None.** No experiment executes this body. S-28's runtime cell is not addressed by this contract.",
     "~~**None.** No experiment executes this body.~~ *(answered: the resolver is not executed, but the initialiser "
     "and both removers were — OPUS blocks 338 and 340, SM-4 and SM-7; 2026-10-02, OPUS)* S-28's runtime cell is not "
     "addressed by this contract."),

    # C-B17 / C-B18 / C-B26: the battle-state contract's stale lines.
    (CB, "counts its invocations and\n  never reads it.",
     "counts its invocations ~~and~~\n  ~~never reads it~~ *(answered: §2 cites it as `00237DF0` and K1 read it, "
     "2026-09-29; 2026-10-02, OPUS)*."),
    (CB, "> **This is the state [the slot-maps contract](../CONTRACT-the-five-parallel-slot-maps.md)'s `SM-7`\n"
         "> describes from the other side** — the derived maps are stale until the refresher runs — and it",
     "> ~~**This is the state [the slot-maps contract](../CONTRACT-the-five-parallel-slot-maps.md)'s `SM-7`~~\n"
     "> ~~describes from the other side** — the derived maps are stale until the refresher runs —~~ *(answered: SM-7 "
     "was corrected 2026-09-25 — a removal rebuilds all five maps in the same call unless the 32-entry pool is full, "
     "so this zero state is not SM-7's; 2026-10-02, OPUS)* and it"),
    (CB, "reads its world position and then tail-jumps into a Movement routine.",
     "~~reads its world position and then tail-jumps into a Movement routine~~ calls a position read whose locals the "
     "frame discards and tail-jumps into `0033CA00` *(answered: FO-6, the field map §7 — `00311E65` writes stack "
     "locals and `00311E6F` pops the frame before `00311E73 jmp 0x33ca00`; 2026-10-02, OPUS)*."),

    # C-B19 / C-B20: the set-save-data path is reached by shipped scripts; FZ-5's verdict cell reads ANSWERED.
    (SS, "Nothing, in the shipped game, unless a script calls the verb: these are developer test sets, and\n"
         "no shipped event needs to.",
     "Nothing, in the shipped game, unless a script calls the verb: these are developer test sets~~, and~~\n"
     "~~no shipped event needs to~~ *(answered: two shipped scripts call it — `naf_b04` selects set 1 and `evt_t0505` "
     "cycles sets 0–3, §7 FZ-5; 2026-10-02, OPUS)*."),
    (SS, "the row's own text is answered, its verdict cell still OPEN)*",
     "the row's own text is answered, ~~its verdict cell still OPEN~~)* *(answered: the register row's verdict cell "
     "reads ANSWERED, verdict set 2026-09-14; 2026-10-02, OPUS)*"),

    # C-B21: the "inventory temporary snapshot" is the item and equipment count arrays (field map §2.3 / §2.8).
    (FMP, "the inventory's temporary snapshot, and",
     "~~the inventory's temporary snapshot~~ the item and equipment count arrays *(answered: §2.3's rows and §2.8; "
     "2026-10-02, OPUS)*, and"),
    (FMP, "the inventory's temporary snapshot and backup",
     "~~the inventory's temporary snapshot~~ the item and equipment count arrays *(answered: §2.8; 2026-10-02, OPUS)* "
     "and backup"),
    (FMP, "  +0x4748  inventory temporary snapshot        +0x5AD8  f32 timer A; +0x5ADC f32 timer B\n",
     "  +0x4748  inventory temporary snapshot        +0x5AD8  f32 timer A; +0x5ADC f32 timer B"
     "   <- corrected 2026-10-02, OPUS - the item (+0x4748) and equipment (+0x47C8) count arrays, section 2.8\n"),

    # C-B22: 00310DB0 is BattleUnit_RunPeriodicCombatMaintenance, whose only caller is 00233F70 (00234001).
    (AP, "**CombatFormula — SERVICE (SWE2-CONTRACT 2026-09-15, 12 edges).** The leader-change path drives the stats "
         "layer:",
     "**CombatFormula — SERVICE (SWE2-CONTRACT 2026-09-15, 12 edges).** ~~The leader-change path drives the stats "
     "layer:~~ The party's bodies drive the stats layer " + T + "`00310DB0` is "
     "`BattleUnit_RunPeriodicCombatMaintenance` (§2b), whose only caller is `00233F70` at `00234001`, not the leader "
     "change)*:"),
    (AP, "`BattleEnmity_UpdatePeriodicDecay` (leader change decays enmity); the other 11 edges are the",
     "`BattleEnmity_UpdatePeriodicDecay` ~~(leader change decays enmity)~~ (the periodic maintenance decays enmity " + T
     + "`00310DB0`'s only caller is `00233F70`)*); the other 11 edges are the"),

    # C-B23: the incoming leader's push is the roster-role notice, which sets the movement body's cell class (O-1).
    (AP, "`002681D0` → `002681E0`, a\n  locomotion-mode push for kind-3 actors driven by the secondary context's byte "
         "`+0x152`",
     "`002681D0` → `002681E0`, ~~a~~\n  ~~locomotion-mode push~~ the roster-role notice, which stores the movement "
     "body's cell class *(answered: O-1, party-roster-and-control-suppression.md §2; 2026-10-02, OPUS)*, for kind-3 "
     "actors driven by the secondary context's byte `+0x152`"),
    (CF, "locomotion path, and an implementation that early-returns on `current == pending` drops that push.*",
     "~~locomotion path~~ roster-role notice, which sets the movement body's cell class, and an implementation that "
     "early-returns on `current == pending` drops that push.* *(answered: the push is the notice `002681E0` — O-1, "
     "party-roster-and-control-suppression.md §2; 2026-10-02, OPUS)*"),

    # C-B25: the active party is four; a guest takes the first free of indices 3, 2, 1 (003170E0).
    (RP, "exactly as documented. **Four is not a mistake for three** — the active party is three, and the\n"
         "fourth slot is what a guest occupies.",
     "exactly as documented. **Four is not a mistake for three** — ~~the active party is three, and the~~\n"
     "~~fourth slot is what a guest occupies.~~ the active party is four, and a guest takes the first free of indices "
     "3, 2 and 1 " + T + "`003170E0` walks map 3 from index 3 down while the index is above 0, `0031711A`–`00317157`; "
     "§1 of this page says four slots)*."),

    # C-B27: +0x5AA4 is the preferred definition selector - the party leader (field map +0x5AA4 row).
    (FM, "**A dword at `+0x5AA4` takes the source table's first byte** and is not part of any map.",
     "**A dword at `+0x5AA4` takes the source table's first byte** and is not part of any map *(answered: it is the "
     "preferred definition selector, the party leader — the battle-state block field map's `+0x5AA4` row; "
     "2026-10-02, OPUS)*."),
    (C5, "  +0x5AA4  u32      the source table's first byte — NOT part of any map (SM-8)\n",
     "  +0x5AA4  u32      the source table's first byte — NOT part of any map (SM-8)   <- corrected 2026-10-02, OPUS - "
     "answered: the preferred definition selector, the party leader (the field map's +0x5AA4 row)\n"),
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
