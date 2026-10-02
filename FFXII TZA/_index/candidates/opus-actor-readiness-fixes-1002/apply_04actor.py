"""apply_04actor.py [--apply] - 04-Actor-Entity readiness map (cloud-reports/re-readiness/04-actor.md), section 3.1
value items C-V1..C-V52, the section 3.2 counts the bytes or the files decide, and the section 3.3 / 3.4 stale and
banner items, settled on the pages (OPUS, 2026-10-02).

Every value verdict was taken at the shipping image (retool.py dis / refs / site; family_prover.load_image for
constants) or at the shipped battle_pack.bin; the map's "favoured" sides were treated as claims. The verdicts and their
deciding addresses are in OPUS's scratch verdicts-04.md.
Each edit strikes the side the bytes REFUTE only, and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*; a stale
"not read / open" claim the pages answer elsewhere is tagged *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment in the block's own comment syntax (their OLD includes the line
end, so NEW never contains OLD); front-matter lines get `# <- corrected ...` after a single-line value.
One heading changes (the shake-table refinement in the manager field map) and it names OPUS.
Left out (no refuted side, or not decidable at the bytes): C-V40 (both sides are the same two-step seeding:
00266530 clears the nibble at 002666F8 and its call 0026681B -> 00265FF0 sets 4 / 5), C-V49 (00265B11 is the `and`,
00265B13 the store of one clear); C-N3 / C-N5 / C-N6 / C-N14..C-N20 (census-generation drift or script / trace counts;
see the reply); C-S15 (bits 16 / 28 are named, bits 5 / 31 are not - no contradiction); C-S44 (register stamps; both
rows are SUPERSEDED in the register); C-S50 (an HTML comment); B-3..B-13 (front-matter metadata, dates and numbering).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "04-Actor-Entity/"
R = F + "README.md"
SR = F + "Actor-Storage-Record/the-record-behind-every-actor.md"
SF = F + "Actor-Storage-Record/the-actor-storage-record-field-map.md"
PC = F + "CONTRACT-actor-record-pool-and-region-map.md"
IC = F + "CONTRACT-actor-storage-record-initialisation.md"
MF = F + "Actor-Manager-Record/the-actor-manager-record-field-map.md"
MC = F + "CONTRACT-manager-slot-entry-tables.md"
BP = F + "battleunit-slot-pool-and-actor-class.md"
BU = F + "Battle-Unit/the-battle-unit-field-map.md"
HB = F + "Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md"
CB = F + "Unit-Definition/CONTRACT-battle-unit-construction.md"
DR = F + "Unit-Display-Record/the-record-00329220-builds.md"
KB = F + "Battle-Record-Kind/battle-record-kind-byte.md"
TI = F + "Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md"
NM = F + "Actor-Names/the-npc-name-dictionary.md"
FC = F + "CONTRACT-field-runtime-pass.md"
FP = F + "the-field-runtime-pass.md"
CX = F + "Actor-Contexts/the-movement-and-secondary-context-censuses.md"
FL = F + "the-definition-record-flag-pair.md"

C = "*(corrected 2026-10-02, OPUS: "
A = "*(answered: see "
E = "; 2026-10-02, OPUS)*"
STUB = "`005C5230` is `xor eax, eax` / `ret`"

EDITS = [
    # C-V1: record[+3] = (TAB[i].byte0 << 5) | (i & 0x1F) - kind HIGH 3, the 01E0C328 row LOW 5 (002679F0:
    #       00267AE1-00267AE8 r9b = i & 0x1F, 00267B0A-00267B13 TAB[i].byte0 << 5); i runs 0-7 across the table.
    (SF, "per record at `00267B04` / `00267B13`: `(old & 0xE0) | (kind & 0x1F)`, then `| (sequenceByte << 5)`\n"
         "  — the packed kind (low 5 bits) and sequence (high 3) the 78 readers consume",
     "per record at `00267B04` / `00267B13`: ~~`(old & 0xE0) | (kind & 0x1F)`, then `| (sequenceByte << 5)`~~ "
     "`(old & 0xE0) OR (row & 0x1F)`, then `OR (kind << 5)`\n"
     "  — the packed ~~kind (low 5 bits) and sequence (high 3)~~ row of `01E0C328` (low 5 bits) and kind (high 3) "
     + C + "`00267AE1`–`00267AE8` `r9b = i & 0x1F` with `i` the table row, `00267B0A`–`00267B11` `TAB[i].byte0 << 5`)* "
     "the 78 readers consume"),
    (SR, "record[+0x03] = (kindCode << 5) | (sequenceWithinKind & 0x1F)\n",
     "record[+0x03] = (kindCode << 5) | (sequenceWithinKind & 0x1F)   // <- corrected 2026-10-02, OPUS - the low "
     "field is the row i of 01E0C328 (00267AE1-00267AE8 r9b = i & 0x1F), counted 0-7 across the table, not restarted "
     "per kind\n"),

    # C-V2: sub == 1 gives 0xA0 (00266B8C mov eax, 0xC8 / 00266B91 jne / 00266B93 mov eax, 0xA0); rows 2, 4, 7 carry
    #       sub 1 (01E0C328 bytes); the sequence-7 record is 0x668 (01E0C344 size 1,640).
    (SR, "then `00266B8C` loads **`0xC8`** if it matches and `00266B93` **`0xA0`** if it does not, before",
     "then ~~`00266B8C` loads **`0xC8`** if it matches and `00266B93` **`0xA0`** if it does not~~ `00266B8C` loads "
     "`0xC8` and `00266B93` replaces it with `0xA0` when the byte is 1 " + C + "`00266B91 jne 00266B98` skips the "
     "`0xA0` load when the byte is not 1; rows 2, 4 and 7 of `01E0C328` carry 1)*, before"),
    (SR, "and **8 × `0x14` wherever that byte is not 1** - which moves `waitSlotArray` to `+0x578` and makes the whole "
         "record **`0x6B8`, not `0x6E0`**.",
     "and **8 × `0x14` wherever that byte is ~~not~~ 1** - which moves `waitSlotArray` to `+0x578` and makes the "
     "sequence-7 record ~~**`0x6B8`, not `0x6E0`**~~ **`0x668`** " + C + "the table's size word for row 7 at "
     "`01E0C344` is 1,640 = `0x668`, with six wait slots, `0x578 + 6 × 0x28`)*."),
    (SR, "variant only. *I did not read the table at `01CEC329` to say which sequences take which branch.*",
     "variant only. ~~*I did not read the table at `01CEC329` to say which sequences take which branch.*~~ *(answered: the table is "
     "`01E0C328` — `r9` holds the image base, so `[r9 + rax*4 + 0x1CEC329]` is `01E0C329`, the `+1` byte — and rows 2, "
     "4 and 7 take the `0xA0` branch; 2026-10-02, OPUS)*"),

    # C-V3: the slot-index store is 002665EB (mov word ptr [rbx], r10w in 00266530); 0026656B is no instruction start.
    (SR, "| `+0x00` is the slot index | `0026656B mov word ptr [rbx], r10w` |",
     "| `+0x00` is the slot index | ~~`0026656B mov word ptr [rbx], r10w`~~ `002665EB mov word ptr [rbx], r10w` " + C +
     "`0026656B` is not an instruction boundary)* |"),

    # C-V4: 002666F1 and dword [rbx+0x1C], 0xFFFFDEFF is in the initialiser 00266530; 00265AC3 and 0026A003 also.
    (SR, "**So `EH-4`'s `&0xFFFFDEFF` is not an\n      initialiser mask at all** — the route-proven census puts it at "
         "`00265AC3`, in\n      `ActorSystem_BindBattleUnitsForEligibleRecords`, and the second copy is `0026A003`.",
     "**So `EH-4`'s `&0xFFFFDEFF` ~~is not an~~\n      ~~initialiser mask at all~~ is an initialiser mask too** "
     + C + "`002666F1 and dword ptr [rbx + 0x1C], 0xFFFFDEFF` is inside `00266530`, the initialiser — three sites in "
     "all)* — the route-proven census puts ~~it~~ a copy at `00265AC3`, in\n"
     "      `ActorSystem_BindBattleUnitsForEligibleRecords`, and ~~the second copy is~~ another at `0026A003`."),

    # C-V5: the initialiser fills +0xC8..+0xEB with 0xFFFF itself (0026689A-002668B0 rep stosw, ecx = 0x12).
    (IC, "are ~~simply not\ntouched by the initialiser~~ **not touched by `00266530`'s own stores**.",
     "are ~~simply not~~\n~~touched by the initialiser~~ ~~**not touched by `00266530`'s own stores**~~ not touched "
     "by `00266530`'s own stores, except `+0xC8`–`+0xEB`, which it fills with `0xFFFF` " + C + "`0026689A`–`002668B0` "
     "`rep stosw` with `rdi = rbx + 0xC8`, `ecx = 0x12`)*."),
    (IC, "| S4 | AR-5 | **survives**: the body's own stores end at `0x11C` and touch neither `+0x60`-`+0xB7` nor "
         "`+0xC0`-`+0xEB`;",
     "| S4 | AR-5 | ~~**survives**~~ **refuted in part**: the body's own stores end at `0x11C` and touch ~~neither "
     "`+0x60`-`+0xB7` nor `+0xC0`-`+0xEB`~~ no byte of `+0x60`-`+0xB7`, but do fill `+0xC8`-`+0xEB` " + C +
     "`002668B0` `rep stosw`, eighteen words of `0xFFFF`)*;"),

    # C-V6: the table's +0x01 is the sub flag (00266B83 cmp byte [r9+rax*4+0x1CEC329], 1), not padding.
    (IC, "`0x1E0C328` — 4-byte entries `{u8 classByte, u8 pad, u16 stride}`",
     "`0x1E0C328` — 4-byte entries `{u8 classByte, ~~u8 pad~~ u8 subFlag, u16 stride}` " + C + "`00266B83` reads "
     "`+1`: 1 selects the `0xA0` resource step, set on rows 2, 4 and 7)*"),

    # C-V7: the jump table is at 00266BA4 (00266AE7 is lea r9, image base); +0xB8 = NULL (row 0) or rec+0x120,
    #       +0xC0 = rec+0x350 (rows 5-7) or NULL; +0x80 / +0x20 are +0xA0's offsets (rows 1-2 / 3-4).
    (SF, "  jump table at `00266AE7`) and points `+0xB8` / `+0xC0`",
     "  jump table at ~~`00266AE7`~~ `00266BA4` " + C + "`00266AE7` is `lea r9, [00120000]`, the image base)*) and "
     "points `+0xB8` / `+0xC0`"),
    (SF, "(`+0x120`, `+0x120 + 0x80`, `+0x120 + 0x20`, `+0x120 + 0x230` by kind; `00266AFB`–`00266B68`)",
     "(~~`+0x120`, `+0x120 + 0x80`, `+0x120 + 0x20`, `+0x120 + 0x230` by kind~~ `+0xB8` NULL for row 0 and "
     "`rec + 0x120` for rows 1–7, `+0xC0` `rec + 0x350` (`+0x120 + 0x230`) for rows 5–7 and NULL otherwise; `+0x80` "
     "and `+0x20` are `+0xA0`'s offsets from `+0x120` for rows 1–2 and 3–4 " + C + "the four arms the table at "
     "`00266BA4` selects, `00266AFB` / `00266B15` / `00266B36` / `00266B54`)*; `00266AFB`–`00266B68`)"),

    # C-V8: start +0x1DE, count +0x1D6 (00225D36 / 00225D3D; 0035A7C6 / 0035A7CD; 0046BEA0 / 0046BEAC); the allocator
    #       writes per-kind counts at slot +0x1D0 (00267AD4) and starts at +0x1D8 (00267B53).
    (SR, "        `+0x1D6`…`+0x1D6 + 0x1DE`, **skipping active party members**",
     "        ~~`+0x1D6`…`+0x1D6 + 0x1DE`~~ `[+0x1DE]`…`[+0x1DE] + [+0x1D6]` " + C + "`0035A7C6 movzx edi, word ptr "
     "[rax + 0x1DE]` is the start and `0035A7CD movzx esi, word ptr [rax + 0x1D6]` the count)*, **skipping active "
     "party members**"),
    (MF, "iterates slots `[+0x1D6] .. +0x1D6+[+0x1DE]` of the",
     "iterates slots ~~`[+0x1D6] .. +0x1D6+[+0x1DE]`~~ `[+0x1DE] .. [+0x1DE] + [+0x1D6]` " + C + "`0046BEA0` loads "
     "the start from `+0x1DE`, `0046BEAC` the count from `+0x1D6`)* of the"),
    (SF, "— and `+0x08` (word)\n  at `00267B53`.",
     "— and ~~`+0x08` (word)~~\n  ~~at `00267B53`~~ the manager slot's per-kind start words `+0x1D8 + kind × 2` at "
     "`00267B53` " + C + "there `rax = r15 + 0x1D0`, the slot, not the record; the counts are at `+0x1D0 + kind × 2`, "
     "`00267AD4`)*."),

    # C-V9: +0x08 after 00266530: bit 0 set, bits 5, 6, 7 cleared, bit 4 by condition.
    (SR, "`+0x08` keeps its prior value with only bit 7 cleared (`002665BA`, `0026667A`); and",
     "~~`+0x08` keeps its prior value with only bit 7 cleared (`002665BA`, `0026667A`)~~ `+0x08` comes out with bit 0 "
     "set, bits 5, 6 and 7 cleared and bit 4 set or cleared by a condition " + C + "`002665E8 and dl, 0xBF`, "
     "`002665FA or dl, 1`, `00266607 and dl, 0xDF`, `0026664F` / `00266657`, `0026667A and byte ptr [rbx + 8], "
     "0x7F`)*; and"),

    # C-V10: 003DF73A test dword [rbx+0x1C], 0x2100 reads bit 8 with bit 13.
    (SR, "| **which indices the engine reads for itself** | 0, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 16, 17 —",
     "| **which indices the engine reads for itself** | ~~0, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 16, 17~~ 0, 2, 3, 4, 5, "
     "6, 7, 8, 10, 11, 13, 14, 16, 17 " + C + "`003DF73A test dword ptr [rbx + 0x1C], 0x2100` reads bit 8 with bit "
     "13)* —"),

    # C-V11: the bank elements are int16 - 003211C2 / 003211D7 / 003211EC movsx ecx, ax (kind 9 movzx, 0032125C).
    (SR, "- What the bank's `u16` entries *mean* is still unknown",
     "- What the bank's ~~`u16`~~ `int16` " + C + "`003211C2` / `003211D7` / `003211EC` `movsx ecx, ax` on kinds 1–3, "
     "§24)* entries *mean* is still unknown"),

    # C-V12: 00265FF0 is 1,339 B (ends 00266526 jmp), 00265B60 is 1,067 B (ends 00265F8A ret).
    (SR, "`00265FF0` (~97 B) — frame record op",
     "`00265FF0` ~~(~97 B)~~ (1,339 B) " + C + "the body runs to the 5-byte `jmp` at `00266526`)* — frame record op"),
    (SR, "`00265B60` (~90 B) — `qword[rcx+0xC0]` null-gate",
     "`00265B60` ~~(~90 B)~~ (1,067 B) " + C + "the body runs to the `ret` at `00265F8A`)* — `qword[rcx+0xC0]` "
     "null-gate"),

    # C-V13: the game's slot is 0x288 (002630AB imul r14, rax, 0x288 over 02098E10); 0x200 is the harness image.
    (MC, "argument of 250 writes at `slot + 0x20C`, outside the `0x200` slot.",
     "argument of 250 writes at `slot + 0x20C`, ~~outside the `0x200` slot~~ inside the game's `0x288` slot and "
     "outside only the harness's `0x200` image " + C + "`002630AB imul r14, rax, 0x288` over `02098E10`)*."),
    (MC, "a store at `+0xF4`, inside the `0x200` slot.",
     "a store at `+0xF4`, inside the ~~`0x200`~~ `0x288` slot " + C + "the slot stride, `002630AB`)*."),
    (MC, "which writes at `slot + 0x20C` — outside the `0x200` slot and into planted guard bytes |",
     "which writes at `slot + 0x20C` — ~~outside the `0x200` slot and~~ inside the game's `0x288` slot, outside the "
     "harness's `0x200` image and into its planted guard bytes " + C + "`002630AB`)* |"),
    (MC, "Reproducing that faithfully reproduces an\n   out-of-slot write;",
     "Reproducing that faithfully reproduces ~~an~~\n   ~~out-of-slot write~~ writes past the lookup words into the "
     "slot's later fields, and past the `0x288` slot only from subscript 312 " + C + "a subscript of 250 lands at "
     "`+0x20C`, inside the slot)*;"),

    # C-V14: side A tests twice - 003DA417 movsxd r8, edx; 003DA42C test edx, edx / js; 003DA434 cmp r8d, [rcx+4] / jae.
    (MC, "| **the two sides validate the record index differently** | **re-read 2026-09-12**: side A uses one unsigned "
         "compare, `003DA434 cmp r8d, [rcx+4]` / `jae`, which rejects negatives by itself;",
     "| **the two sides validate the record index ~~differently~~ the same way** | ~~**re-read 2026-09-12**: side A "
     "uses one unsigned compare, `003DA434 cmp r8d, [rcx+4]` / `jae`, which rejects negatives by itself;~~ side A "
     "also uses two, `003DA42C test edx, edx` / `js` then `003DA434 cmp r8d, [rcx+4]` / `jae` " + C + "both are in "
     "`003DA400`, with `r8` from `003DA417 movsxd r8, edx`)*;"),

    # C-V15: after the field writes side A calls 00257230 (003DA4A2), side B 0037DCF0 (003DD2D5).
    (MC, "    call 00257230(slot->0x28)\n",
     "    call 00257230(slot->0x28)   # <- corrected 2026-10-02, OPUS - side A only (003DA4A2); side B calls "
     "0037DCF0(slot->0x28) (003DD2D5)\n"),

    # C-V16: 005C5230 is xor eax, eax / ret, so side B's negative fifth argument becomes 0, side A's clamp 0.
    (MC, "**executed** with the same negative value on both sides — the entry's `+0x04` and the call trace both "
         "differ |",
     "**executed** with the same negative value on both sides — ~~the entry's `+0x04` and the call trace both "
     "differ~~ only the call trace differs; the entry's `+0x04` is 0 on both " + C + STUB + "; side A `003DA45A xor "
     "ecx, ecx` / `003DA46E cmovns ecx, eax`)* |"),
    (MC, "in *when* they resolve the fifth\n   argument, in *what* they resolve it to, in whether",
     "in *when* they resolve the fifth\n   argument, ~~in *what* they resolve it to,~~ " + C + "both resolve a negative "
     "one to 0 — " + STUB + ")* in whether"),
    (MC, "**Side B calls out before it validates.** A refused bind is not side-effect-free on the B side.",
     "**Side B calls out before it validates.** ~~A refused bind is not side-effect-free on the B side.~~ On a "
     "refused bind its one extra effect is the call itself, visible only in a call trace " + C + STUB + ")*."),

    # C-V17: 003DD1FB / 003DA2DB store entry +0x10 ((ch + 0x10) * 24), not slot +0x000 - census artefacts.
    (MF, "| 2 / 10 / 5 | `003DD1F0` (`003DD1FB`); `003DA2D0` (`003DA2DB`) |",
     "| 2 / 10 / 5 | ~~`003DD1F0` (`003DD1FB`); `003DA2D0` (`003DA2DB`)~~ " + C + "census artefacts — both store an "
     "entry's `+0x10` rate, `movss [rcx + (ch + 0x10) × 24]`, `003DD1F0`–`003DD1FB`, `003DA2D0`–`003DA2DB`)* |"),

    # C-V18: one table at 02ADD980, stride 0x3D0: 0037D243 lea r9, [02ADD980] reads each record's header qwords
    #        (0037D25F / 0037D267); 02ADD990 = +0x10, driver 0; 0037DCFA uses 02ADD980.
    (MF, "### Refinement — the record table is at `02ADD990`, and `+0x28` indexes it",
     "### Refinement — the record table is at ~~`02ADD990`~~ `02ADD980` (corrected 2026-10-02, OPUS), and `+0x28` "
     "indexes it"),
    (MF, "0037D212  lea    rax, [rip + 0x2760777]  ; 02ADD990  <- THE BASE\n",
     "0037D212  lea    rax, [rip + 0x2760777]  ; 02ADD990  <- THE BASE   <- corrected 2026-10-02, OPUS - not the "
     "base: 02ADD990 = 02ADD980 + 0x10, driver block 0; the same function's 0037D243 lea r9, [02ADD980] reads each "
     "record's header qwords (0037D25F, 0037D267), and 0037DCFA uses 02ADD980\n"),
    (MF, "`02ADDA34` is `+0xA4` inside record 0 — a field of the table, not its base.",
     "`02ADDA34` is ~~`+0xA4`~~ `+0xB4` inside record 0, driver 0's `+0xA4` " + C + "the record base is "
     "`02ADD980`, its sixteen-byte header first)* — a field of the table, not its base."),

    # C-V19: the 0x860 array is two elements at 02097D20 / 02098580 (002593D0, 00259470 copy 0x860 bytes between them),
    #        ending 02098DE0 before 02098E10; 02098428 / 02098378 are interior cursors (+0x708 / +0x658).
    (MF, "is the loop bound of a foreign `0x860`-stride array at `02098428` (`cmp rdi,rbp` at `002597B9`)",
     "is the loop bound of a foreign `0x860`-stride array ~~at `02098428`~~ whose cursor starts at `02098428`, "
     "element 0's `+0x708`; the array is two elements at `02097D20`, ending `02098DE0` before the slot array " + C +
     "`002593D0` / `00259470` copy `0x860` bytes between `02097D20` and `02098580`)* (`cmp rdi,rbp` at `002597B9`)"),
    (R, "two `0x860`-byte presentation slots based at `02098378`:",
     "two `0x860`-byte presentation slots based at ~~`02098378`~~ `02097D20`, `02098378` being slot 0's `+0x658` "
     + C + "`002593D0` / `00259470` copy `0x860` bytes between `02097D20` and `02098580`; the two end at `02098DE0`, "
     "before the manager array at `02098E10`)*:"),

    # C-V20: 002E9B80 -> 003588B0 returns an ACTOR RECORD (00358909 from the slot's pool [slot+8], generation-checked
    #        at 00358913); 002E9B8E reads that record's +0xC0, the SecondaryContext pointer, not the slot's +0xC0.
    (MF, "context record this map's own `+0xC0` entries describe —",
     "context record ~~this map's own `+0xC0` entries describe~~ an actor record's `+0xC0` points at (`rec + 0x350`), "
     "not this slot's `+0xC0` " + C + "`003588B0` returns an actor record — `00358909 mov rax, [rcx + rbx*8 + 8]` "
     "out of the slot's pool `[slot + 8]`, generation-checked at `00358913` — and `002E9B8E` reads its `+0xC0`)* —"),

    # C-V21: +0x1E0 is a dword counter (002630B7 dec dword [r14+0x1E0]); the bind's qword store 0026CB1F zeroes +0x1E4 too.
    (MF, "| `+0x1E0` | 4 | u64 | **zeroed at bind (`0026CB1F`)** |",
     "| `+0x1E0` | 4 | ~~u64~~ u32 " + C + "a dword counter — `002630B7 dec dword ptr [r14 + 0x1E0]`; the bind's "
     "qword store `0026CB1F` zeroes `+0x1E4` with it)* | **zeroed at bind (`0026CB1F`)** |"),
    (MF, "  +0x1E0 u64 zeroed at bind                 +0x200 u8 (bit 2 cleared at bind)   +0x201 u8 sub-step opt-in\n",
     "  +0x1E0 u64 zeroed at bind                 +0x200 u8 (bit 2 cleared at bind)   +0x201 u8 sub-step opt-in   "
     "<- corrected 2026-10-02, OPUS - +0x1E0 is a u32 counter (002630B7 dec dword); the bind's qword store 0026CB1F "
     "zeroes +0x1E0 and +0x1E4\n"),

    # C-V22: +0x68..+0x8F is written by the bind (0026CB43 / 0026CB4E / 0026CB6B / 0026CB59 / 0026CAE6) and +0x68 /
    #        +0x70 are read by the interpreter (00261855 / 0026187D).
    (MF, "The ones of 32 bytes or more: `+0x68`–`+0x97` (48 B), `+0x244`–`+0x287` (68 B).",
     "The ones of 32 bytes or more: ~~`+0x68`–`+0x97` (48 B),~~ `+0x244`–`+0x287` (68 B) " + C + "`+0x68`–`+0x8F` "
     "is written by the bind — `0026CB43`, `0026CB4E`, `0026CB6B`, `0026CB59`, `0026CAE6` — and `+0x68` / `+0x70` are "
     "read by the interpreter at `00261855` / `0026187D`; whether `+0x90`–`+0x97` is reached is not settled here)*."),

    # C-V23: the channel table is 02EBF1A0 (002369E5 lea rdi, [02EBF1A0] / 002369F6 mov ecx, 0xC / 00236A01 rep stosq;
    #        00233E0D); nothing references 02EFF1A0. The float is 009146E4 (002369DD).
    (BP, "  12-qword channel table at `02EFF1A0` (`rep stosq`, 0xC qwords), stores",
     "  12-qword channel table at ~~`02EFF1A0`~~ `02EBF1A0` " + C + "`002369E5 lea rdi, [02EBF1A0]`; nothing references "
     "`02EFF1A0`)* (`rep stosq`, 0xC qwords), stores"),
    (BP, "  `float[008A46E4]` to `0208935C`,",
     "  ~~`float[008A46E4]`~~ `float[009146E4]` " + C + "`002369DD movss xmm0, [009146E4]`)* to `0208935C`,"),
    (BP, "channel-capacity probe — `cl > 0xB` → 0; `02EFF1A0[cl]` already set → 1;",
     "channel-capacity probe — `cl > 0xB` → 0; ~~`02EFF1A0[cl]`~~ `02EBF1A0[cl]` " + C + "`00233E0D lea rcx, "
     "[02EBF1A0]`)* already set → 1;"),

    # C-V24: 0208E6A0 is the slot count, 0x20 (002368EB / 002368FE); 0xEA7900 = 0xF50 x 0xF50, not a pool extent, and
    #        002342AB jae 002342C3 sends every slot at or above the base to the memset.
    (BU, "| `0208E688` | the unit pool base; `0208E6A0` the slot count factor (`0xEA7900` per bank) |",
     "| `0208E688` | the unit pool base; `0208E6A0` ~~the slot count factor (`0xEA7900` per bank)~~ the slot count, "
     "`0x20` (`002368EB`–`002368FE`), which the release check multiplies by `0xEA7900` = `0xF50` × `0xF50` " + C +
     "`002342AD`–`002342B4`; no bank is involved)* |"),
    (BP, "002342B4  imul    rcx, rax, 0xEA7900       ; the pool extent\n",
     "002342B4  imul    rcx, rax, 0xEA7900       ; the pool extent   <- corrected 2026-10-02, OPUS - not the pool "
     "extent: 0xEA7900 = 0xF50 x 0xF50, and 002342AB jae 002342C3 sends every slot at or above the base straight to "
     "the memset; this bound is tested only for a pointer below the base\n"),
    (BP, "**The clear is guarded by a pool bounds check** — the slot must lie between the base and\n"
         "`base + count × 0xEA7900` — so a pointer that is not a pool slot is not scrubbed.",
     "~~**The clear is guarded by a pool bounds check** — the slot must lie between the base and~~\n"
     "~~`base + count × 0xEA7900` — so a pointer that is not a pool slot is not scrubbed.~~ **The clear is not "
     "bounded above:** `002342A8 cmp rbx, rdx` / `002342AB jae 002342C3` takes every slot at or above the base "
     "straight to the memset, and `base + count × 0xEA7900` is compared only for a pointer below the base " + C +
     "`002342A1`–`002342CE`)*."),

    # C-V25: the allocator writes actor +0x30 = unit (002344E7 -> 002134A0 mov [rcx+0x30], rdx) and unit +0x10 = actor
    #        (002344EF); "no back-pointer" holds only inside the scanned span.
    (BP, "the span; **the binder writes no back-pointer**, which closes",
     "the span; ~~**the binder writes no back-pointer**~~ **the binder writes no back-pointer inside the span** — its "
     "two back-pointers, unit `+0x10` = actor (`002344EF`) and actor `+0x30` = unit (`002344E7` → `002134A0`), lie "
     "outside it " + C + "`00234480`)*, which closes"),

    # C-V26: bit 21 is cleared at the slot bind (00234503 and dword [rbx], 0xFFDFFFFF in 00234480).
    (BU, "| 21 | `0x200000` | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` (`002398D1`) |  |",
     "| 21 | `0x200000` | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` (`002398D1`) | `00234480` (`00234503`) " + C
     + "the slot allocator's `and dword ptr [rbx], 0xFFDFFFFF` at bind)* |"),

    # C-V27: 00233AD0 sets bit 3 (00233B4B or dword [rbx], 8) and clears bit 26 (00233AFB); bit 1's setter is 00300F2A.
    (BU, "flag-word writes set `ACTIVATION_COMMITTED` (bit 1) as documented",
     "flag-word writes ~~set `ACTIVATION_COMMITTED` (bit 1)~~ clear bit 26 (`00233AFB`) and set bit 3 (`00233B4B or "
     "dword ptr [rbx], 8`) " + C + "bit 1's setter is `00300F2A`)* as documented"),

    # C-V28: unit +0x52 = the class row's word +6 (0023A910 -> 0023A936 [rsp+0x80] -> 0023AC14), -1 on the party path
    #        (0023AB73 / 0023AB98); 0031B9A0 reads the class row's +0x52 through [unit+0xE68] (0031B9CE-0031B9D5).
    (HB, "the installer copies it to unit `+0x52`\n> (§2.4), and `0031B9A0` returns it as",
     "~~the installer copies it to unit `+0x52`~~ the installer does not copy it — unit `+0x52` is the class row's "
     "word `+6`, `-1` on the party path " + C + "`0023A910` → `0023A936` → `0023AC14`; `0023AB73` / `0023AB98`)*\n"
     "> ~~(§2.4), and~~ `0031B9A0` reads it from the class row `[unit + 0xE68]` (`0031B9CE`–`0031B9D5`) and returns "
     "it as"),
    (BU, "(`003021F3`). Which definition field feeds the stack slot is not traced.",
     "(`003021F3`). ~~Which definition field feeds the stack slot is not traced.~~ *(answered: the class row's word "
     "`+6` on the enemy path, `0023A910` → `0023A936`, and `-1` on the party path, `0023AB73` → `0023AB98`" + E),

    # C-V29: bit 43 is read - 0031FDA0: 0031FDAD movabs rax, 0x80000000000 / 0031FDB7 test qword [rcx], rax.
    (HB, "the same scan does find bit 40 (byte `+5` bit 0) and the dword's other bits — so the installer's\n"
         "register-path write is the only known access and the bit is, as far as the image shows, unread.",
     "the same scan does find bit 40 (byte `+5` bit 0) and the dword's other bits — so the installer's\n"
     "~~register-path write is the only known access and the bit is, as far as the image shows, unread.~~ "
     "register-path write is not the only access: `0031FDA0` reads the bit through a register mask " + C +
     "`0031FDAD movabs rax, 0x80000000000` / `0031FDB7 test qword ptr [rcx], rax`)*."),
    (HB, "bit 43 has no immediate accessor anywhere in the image (§2.9).",
     "bit 43 has no immediate accessor anywhere in the image (§2.9), but it has a register-mask reader " + C +
     "`0031FDA0`, `0031FDAD` / `0031FDB7`)*."),

    # C-V30: 00329220 also reads the spawn record's +0x12 (003298B1-003298C6 -> view +0x88).
    (HB, "the `+0x12` copy is read once, by",
     "the `+0x12` copy is read ~~once,~~ " + C + "twice — `00329220` also reads it through `+0x6A0`, "
     "`003298B1`–`003298C6`, into StatusView `+0x88`)* by"),

    # C-V31 + C-S28: at the cap the word becomes 1 (0023A819 mov edx, r13d with r13d = 1 from 0023A78B; threshold 0x34
    #        from 00254A40); 0208D454 is the bank selector.
    (HB, "`if (c < threshold) counters[k] = c + 1`;",
     "~~`if (c < threshold) counters[k] = c + 1`~~ `counters[k] = c < threshold ? c + 1 : 1` " + C + "`0023A819 mov "
     "edx, r13d` with `r13d = 1` (`0023A78B`), `0023A81E jae`, store at `0023A838`; the threshold is `0x34`, "
     "`00254A40`)*;"),
    (HB, "the word becomes `bx + 1`; **record `+0x12 = (u8)bx`** — a per-area (the byte at `0208D454`), per-row-byte-2 "
         "counter of 64 words each, incremented on every fresh spawn until the wrap threshold,",
     "the word becomes `bx + 1`, else 1 " + C + "`0023A819`–`0023A838`)*; **record `+0x12 = (u8)bx`** — ~~a per-area "
     "(the byte at `0208D454`)~~ a per-bank *(answered: see \"The spawn counter, corrected\" below — the byte at "
     "`0208D454` is a bank selector" + E + ", per-row-byte-2 counter of 64 words each, incremented on every fresh "
     "spawn ~~until the wrap threshold~~ and set back to 1 at the wrap threshold `0x34`,"),

    # C-V32: the party table's row size is its descriptor's word +8 (0023AA95 movzx esi, word [rdx+8] / imul esi, r12d);
    #        shipped battle_pack.bin +0x44 st2e: 40 rows x 128 B.
    (HB, "the party table (the registry page records its 456-byte rows and declines to name it) |",
     "the party table (the registry page records ~~its 456-byte rows~~ rows of the descriptor's word `+8` bytes — 40 "
     "rows of 128 in the shipped `battle_pack.bin` " + C + "`0023AA95 movzx esi, word ptr [rdx + 8]` / `0023AA99 "
     "imul esi, r12d`; the `st2e` header at blob `+0x44` gives count 40, row size 128)* and declines to name it) |"),

    # C-V33: 02EC1380 is two 24-byte entries (00328FF3 lea r9, [rax+rax*2] / [rax+r9*8]; 003221B0 clears to 02EC13AF).
    (HB, "`02EC1380`–`02EC13A8`: head/tail pointers + two `-1` id dwords;",
     "`02EC1380`–`02EC13A8`: ~~head/tail pointers + two `-1` id dwords~~ the two 24-byte tracked-HP entries "
     "(`02EC1380`–`02EC13AF`), each `+0` set to `-1` and the rest zeroed " + C + "`003221B2`–`003221F5`; stride 24 at "
     "`00328FF3`)*;"),

    # C-V34: the old id is 0xFFFF when the unit is null or flag bit 2 is clear; the +0x698 pointer is not tested.
    (HB, "`0xFFFF` when the unit has no record), and",
     "~~`0xFFFF` when the unit has no record~~ `0xFFFF` when the unit is null or its flag bit 2 is clear — the "
     "pointer itself is not tested " + C + "`0023A597`–`0023A5AE`, read before the reset at `0023A5B0`)*), and"),

    # C-V35: on a match the rekey stores a DWORD at [02EBF190] + 0x5AA4 (pointer dereferenced) = stats byte +4 or 0xFF.
    (HB, "`0032212E`), re-points the leader selector at `02EBF190 + 0x5AA4` to the re-keyed unit's type byte",
     "`0032212E`), ~~re-points the leader selector at `02EBF190 + 0x5AA4` to the re-keyed unit's type byte~~ stores "
     "a dword at `[02EBF190] + 0x5AA4` — the pointer is dereferenced — holding the re-keyed unit's stats byte `+4`, "
     "or `0xFF` " + C + "`0032215E`–`00322173`, `movzx ecx, al` / `mov dword ptr [rax + 0x5AA4], ecx`)*"),

    # C-V36: 0030C4B1 stores r8b (the third argument); 0030C650 skips the per-level stat growth for kind != 0
    #        (0030C6D9 cmp byte [rdi+5], 0 / jne 0030C7A7) and only advances +0x1C2.
    (HB, "| **`+0x88 = kind` (u8)** — the third argument, stored on the enemy branch only — then straight to the "
         "growth |",
     "| ~~**`+0x88 = kind` (u8)**~~ **`+0x88 = r8b` (u8)** — the third argument (`0030C4B1`), stored on the enemy "
     "branch only — then ~~straight to the growth~~ straight to `0030C650`, which for kind ≠ 0 skips the per-level "
     "stat growth and only advances `+0x1C2` " + C + "`0030C6D9`–`0030C6DD` → `0030C7A7`–`0030C7BB`)* |"),

    # C-V37: 003266C0 passes the word from its four-id array (00326A7B / 00326B04), not 0.
    (HB, "`BattleGroup_RefreshFourActorDefinitions` with 0) — bounded at",
     "`BattleGroup_RefreshFourActorDefinitions` ~~with 0~~ with the word from its four-id array " + C + "`00326A7B "
     "movzx esi, word ptr [r15]` / `00326B04 movzx edx, si`; an id with high byte 0 takes the party path)*) — "
     "bounded at"),

    # C-V38: 00329210 is a 14-byte setter (dword [0208D328 + ecx*4] = edx); the other sites are 00329220's; 00861EC0 is
    #        the memset thunk jmp [008C2A60].
    (HB, "| `00329210` | recompute battery — `lea 0208D328` (`00329213`), `00861EC0` free, `00236850`",
     "| `00329210` | ~~recompute battery —~~ a 14-byte setter, `dword [0208D328 + ecx × 4] = edx` — `lea 0208D328` "
     "(`00329213`) " + C + "every site after `00329213` in this cell lies in `00329220`, and `00861EC0` is the "
     "memset thunk `jmp [008C2A60]`)*; ~~`00861EC0` free,~~ then, in `00329220`: `00236850`"),
    (BU, "frees the slot through `00861EC0` with stride `0xF50` (`002342CE`) —",
     "~~frees~~ zeroes the slot through `00861EC0` " + C + "a `memset` thunk — `002342C3 xor edx, edx` / "
     "`002342C5 mov r8d, 0xF50`)* with stride `0xF50` (`002342CE`) —"),

    # C-V39: 00236124 js tests a zero-extended byte (0023611F movzx eax, dl), so ids 0x00-0xFE all resolve.
    (KB, "    if (id == 0xFF || (int8)id < 0)     return NULL;   /* 0xFF marks an empty slot */\n",
     "    if (id == 0xFF || (int8)id < 0)     return NULL;   /* 0xFF marks an empty slot */   /* <- corrected "
     "2026-10-02, OPUS - the sign test reads a zero-extended byte (0023611F movzx eax, dl; 00236122 test eax, eax; "
     "js), so it never rejects: ids 0x00-0xFE all resolve */\n"),

    # C-V41: row 6 (Reks) is inside the <= 6 span the LP test accepts (002F90EF cmp al, 6 / 002F90F1 jbe).
    (KB, "Penelo; 6–16 the guests (Reks, Amalia,",
     "Penelo; ~~6–16 the guests (Reks,~~ 6 Reks, inside the roster span " + C + "`002F90EF cmp al, 6` / `002F90F1 "
     "jbe` accept row 6 with rows 0–5)*; 7–16 the guests (Amalia,"),

    # C-V42: 00282DF0 reads qword [0209AC30] (00282DF0-00282DFA), not the dictionary; the npcdic block is 02B5E0D8.
    (NM, "whole body loads the dictionary base `qword[0209AC30]`,",
     "whole body loads ~~the dictionary base~~ the base `qword[0209AC30]` " + C + "not the dictionary — the npcdic "
     "block is `02B5E0D8`, stored at `003EAC58`, and `00282DF0` never reads it)*,"),
    (NM, "An unbounded pointer-table getter over the dictionary's",
     "An unbounded pointer-table getter over ~~the dictionary's~~ that object's " + C + "see above)*"),

    # C-V43: the ordinal is the signed word at +0x50 of the slot's payload *(void **)b (0025DB2B / 0025DB31).
    (FC, "    rec = ActorManager_GetRecordByOrdinal(b, *(uint16_t *)(actor + 0x50));\n",
     "    rec = ActorManager_GetRecordByOrdinal(b, *(uint16_t *)(actor + 0x50));   /* <- corrected 2026-10-02, OPUS - "
     "the ordinal is the signed word at +0x50 of the slot's payload *(void **)b: 0025DB2B mov rax, [rbx]; 0025DB31 "
     "movsx edx, word [rax+0x50] */\n"),
    # C-V44: exit A stores 0 (0025DA98 xor edi, edi; 0025DB2E mov r12d, edi; 0025DB79 mov [rbx+0x12], r12b).
    (FC, "        b[0x12] = (uint8_t)conj;\n",
     "        b[0x12] = (uint8_t)conj;   /* <- corrected 2026-10-02, OPUS - stores 0: r12d = edi = 0 (0025DA98, "
     "0025DB2E), written at 0025DB79 */\n"),
    (SR, "| `+0x14` | 6 | the field pass's running conjunction, published into slot `+0x12` —",
     "| `+0x14` | 6 | the field pass's running conjunction, ~~published into slot `+0x12`~~ returned in `eax` " + C +
     "`0025DEAB and r12d, eax` folds it, `0025DEE0 mov eax, r12d` returns it; the settled exit stores 0 into slot "
     "`+0x12`, `0025DB79`)* —"),
    # C-V45: both designated-drive exits go to the tail 0025DECB (0025DB54, 0025DB82); the roster loop and the folds
    #        (0025DE7A-0025DEC6) are the other branch.
    (FC, "    /* ... the roster loop and the two folds, both bounded by *(uint32_t *)(b + 0x20) ... */\n",
     "    /* ... the roster loop and the two folds, both bounded by *(uint32_t *)(b + 0x20) ... */   /* <- corrected "
     "2026-10-02, OPUS - not after the designated drive: exit A jumps to the tail 0025DECB (0025DB82) and exit B too "
     "(0025DB54); the roster loop and folds (0025DE7A-0025DEC6) are the other branch */\n"),
    # C-V46: the request is issued with slot argument 1 (0025DA86 mov r12d, 1; 0025DAE1 mov ecx, r12d; 0025DAE8 mov
    #        edx, 0xD4), so 0032FC30's slot-0 branch (0032FC3E-0032FC40) is not taken.
    (FC, "Resource side: slot 0 issues `WorldSimulation_ProcessDeferredModeRequest(0, 0xD4)` **once**,",
     "Resource side: slot 0 issues ~~`WorldSimulation_ProcessDeferredModeRequest(0, 0xD4)`~~ "
     "`WorldSimulation_ProcessDeferredModeRequest(1, 0xD4)` " + C + "the slot argument is 1 — `0025DA86 mov r12d, 1`, "
     "`0025DAE1 mov ecx, r12d`, `0025DAE8 mov edx, 0xD4` — so the callee's slot-0 branch, `0032FC3E`–`0032FC40`, is "
     "not taken)* **once**,"),
    (FP, "The runtime pass issues it **once for slot 0 with\n      index `0xD4` = 212** (`0025DACC`–`0025DAF2`):",
     "The runtime pass issues it **once ~~for slot 0~~ from slot 0's pass with\n      index `0xD4` = 212** "
     "(`0025DACC`–`0025DAF2`) " + C + "with the slot argument 1 — `0025DA86 mov r12d, 1`, `0025DAE1 mov ecx, r12d` — "
     "so `0032FC30`'s slot-0 branch, `0032FC3E`–`0032FC40`, is not taken for it)*:"),
    # C-V47: 0025DB5A is mov rcx, rdi; the call is at 0025DB5D.
    (FC, "0025DB5A  call 003DB280                    ; (dead: the nibble is never set)\n",
     "0025DB5A  call 003DB280                    ; (dead: the nibble is never set)   <- corrected 2026-10-02, OPUS - "
     "0025DB5A is mov rcx, rdi; the call is at 0025DB5D\n"),
    # C-V48: eight table entries at 0025E3CC for kinds 0-7; kind 0 shares the ja default 0025E127 (0025DFF4-0025E008).
    (FC, "kind dispatch is `cmp eax, 7 / ja`, with kinds 0–8 all armed;",
     "kind dispatch is `cmp eax, 7 / ja`, ~~with kinds 0–8 all armed~~ with eight table entries for kinds 0–7, kind 0 "
     "sharing the `ja` default `0025E127` " + C + "the table at `0025E3CC`, `0025DFF4`–`0025E008`)*;"),

    # C-V50: the floor is 0.01 (008F30E4, maxss at 0026B37D).
    (CX, "the turn/blend scalar `max(0.05, (x·scaleX + y·scaleZ)·0.5)` → `+0xFC`,",
     "the turn/blend scalar ~~`max(0.05, (x·scaleX + y·scaleZ)·0.5)`~~ `max(0.01, (x·scaleX + y·scaleZ)·0.5)` " + C +
     "`008F30E4` holds 0.01, `maxss` at `0026B37D`)* → `+0xFC`,"),
    # C-V51: the binder's k = 3 arm addresses ctx + (r8 + 4) * 0x30 (002E31F8-002E3207): the array runs past +0xC0.
    (CX, "SecondaryContext's first 192 bytes are a **4 × 0x30 element array** (proven 2026-09-16,",
     "~~SecondaryContext's first 192 bytes are a **4 × 0x30 element array**~~ SecondaryContext opens with an array of "
     "`0x30`-byte elements that does not end at `+0xC0` " + C + "the binder `002E3110`'s `k = 3` arm addresses `ctx + "
     "(r8 + 4) × 0x30`, `002E31F8`–`002E3207`; how many elements exist is not settled here)*; the first four "
     "(proven 2026-09-16,"),

    # C-V52: .text is 7,996,981 virtual / 7,997,440 raw; the idiom ORs two dwords into one 32-bit register
    #        (003868F1 / 003868F4), so 22 of 32 positions are untested.
    (FL, "corpus_validated: \"229 OR-sites across 162 functions, scanned over all 8,001,280 bytes of .text, "
         "2026-09-06\"\n",
     "corpus_validated: \"229 OR-sites across 162 functions, scanned over all 8,001,280 bytes of .text, 2026-09-06\"  "
     "# <- corrected 2026-10-02, OPUS - .text is 7,996,981 bytes virtual / 7,997,440 raw by the section table; "
     "8,001,280 matches neither\n"),
    (FL, "| `.text` scanned | **8,001,280 bytes**, every byte |",
     "| `.text` scanned | ~~**8,001,280 bytes**~~ **7,996,981 bytes** virtual, 7,997,440 raw " + C + "the PE section "
     "table; 8,001,280 matches neither)*, every byte |"),
    (FL, "**Twenty-two bits of the 64 available are never tested by this idiom at all.**",
     "**Twenty-two bits of the ~~64~~ 32 available are never tested by this idiom at all.** " + C + "the idiom ORs "
     "two dwords into one 32-bit register, `003868F1 mov eax, [rdi + 0x64]` / `003868F4 or eax, [rdi + 0x3C]`, so "
     "ten tested positions leave 22 of 32)*"),

    # Section 3.2 counts the bytes or the files decide (measured 2026-10-02).
    # C-N1: the storage census on disk: 1,130 rows, 271 functions, 94 displacements (90 in the 0x120 header).
    (SF, "every offset any reached function touches — 81 of them, from 272 functions — with",
     "every offset any reached function touches — ~~81 of them, from 272 functions~~ 94 displacements from 271 "
     "functions in the census on disk, 90 of them inside the `0x120` header *(answered: see the §2.1 table; "
     "measured on `actor-storage-record-accesses.tsv`" + E + " — with"),
    (R, "A companion to the record page: 81 touched offsets from 272 functions",
     "A companion to the record page: ~~81 touched offsets from 272 functions~~ 94 touched displacements from 271 "
     "functions *(answered: the census on disk, measured" + E),
    # C-N2: the 41 is superseded by the page's own re-measure (34, each with a store row).
    (SF, "- **41 touched offsets have no store row**, each with cited sites to start from.",
     "- ~~**41 touched offsets have no store row**, each with cited sites to start from.~~ *(answered: see the "
     "2026-09-27 re-measure directly below — 34 flagged, each now with a store row" + E),
    # C-N4: the battle-unit census on disk: 2,205 rows, 345 functions, 168 displacements.
    (BU, "> touches — 163 of them, from 328 functions — with writers and readers, the name a page\n"
         "> established, and the 3206 bytes on 41 ranges that nothing enumerated reaches.",
     "> touches — ~~163 of them, from 328 functions~~ 168, from 345 functions in the census on disk — with writers "
     "and readers, the name a page\n"
     "> established, and the ~~3206 bytes on 41 ranges~~ 3,174 bytes on 35 ranges that nothing enumerated reaches "
     "*(answered: see §2.1 and §2.3, re-counted 2026-09-11; measured on `battle-unit-accesses.tsv`" + E + "."),
    (R, "seeded by the pool and the three unit-returning accessors: 144 offsets across 310 functions with\n"
        "  writers and readers, the names the store and the pages established, and the 45 ranges nothing",
     "seeded by the pool and the three unit-returning accessors: ~~144 offsets across 310 functions~~ 168 offsets "
     "across 345 functions with\n"
     "  writers and readers, the names the store and the pages established, and the ~~45~~ 35 ranges *(answered: "
     "the census on disk and the page's §2.3 re-count" + E + " nothing"),
    # C-N7: the file now holds 32 0023A570 rows.
    (BU, "holds two rows for it (displacements `0x0` and `0x698`) while the function touches twenty distinct",
     "~~holds two rows for it (displacements `0x0` and `0x698`)~~ held two rows for it before the generation-3 re-run "
     "*(answered: see §10.1, FZ-16; the file now holds 32 `0023A570` rows, measured" + E + " while the function "
     "touches twenty distinct"),
    (BU, "`battle-unit-accesses.tsv` carries thirty `0023A570` rows).",
     "`battle-unit-accesses.tsv` carries ~~thirty~~ thirty-two `0023A570` rows *(answered: measured on the file" + E
     + ")."),
    # C-N8: the store now carries 85 ActorStorageRecord rows (+0x00 to +0x5A0, 81 inside the 0x120 header).
    (SR, "as `ActorStorageRecord` — 41 fields,",
     "as `ActorStorageRecord` — ~~41 fields~~ 85 rows on 2026-10-02, 41 at import *(answered: measured on "
     "`_types/fields.tsv`" + E + ","),
    (SR, "**41 fields, `+0x00` to `+0x11C`.** The full table",
     "~~**41 fields, `+0x00` to `+0x11C`.**~~ **85 rows, `+0x00` to `+0x5A0`, 81 of them inside the `0x120` header** "
     "*(answered: `_types/fields.tsv`, measured; 41 at import" + E + ". The full table"),
    # C-N9: actor-record-offsets-observed.tsv has 56 rows, highest 0x118.
    (SR, "Full table, all 70 offsets with their function/read/write counts:",
     "Full table, all ~~70~~ 56 offsets *(answered: the file holds 56 rows, the highest `0x118`, measured" + E +
     " with their function/read/write counts:"),
    (SR, "are each seen in **one** function only and are recorded in the TSV, **not**",
     "are each seen in **one** function only and ~~are recorded in the TSV~~ are not in the TSV " + C + "the file's "
     "highest row is `0x118`)*, **not**"),
    # C-N10: 33 rip-relative stores to 02099D70 in 16 functions, the bind 0026C8C0 among them.
    (MF, "A RIP-relative census gives 33 stores in 17 functions.",
     "A RIP-relative census gives 33 stores in ~~17~~ 16 functions " + C + "the stores to `02099D70`, the bind "
     "`0026C8C0` among them; no image-base-relative form exists)*."),
    # C-N11: the file holds 204 rows on 2026-10-02.
    (MF, "`actor-manager-record-accesses.tsv` holds **194** rows today, not 167.",
     "`actor-manager-record-accesses.tsv` holds ~~**194** rows today~~ **194** rows at this pass (204 on 2026-10-02, "
     "measured), not 167 " + C + "the file on disk)*."),
    # C-N12: movement 708 rows / 101 displacements / 92 functions; secondary 309 / 42 / 91 (int-parsed).
    (CX, "> what it finds: 313 accesses at 58 offsets of the movement context, 302 at 40 of the secondary. It",
     "> what it finds: ~~313 accesses at 58 offsets of the movement context, 302 at 40 of the secondary~~ 708 accesses "
     "at 101 offsets of the movement context, 309 at 42 of the secondary *(answered: the files on disk, measured" + E
     + ". It"),
    (R, "through the pointers: 313 and 302 accesses at 58 and 40 offsets,",
     "through the pointers: ~~313 and 302 accesses at 58 and 40 offsets~~ 708 and 309 accesses at 101 and 42 offsets "
     "*(answered: the files on disk, measured" + E + ","),
    # C-N13: the page's own note adds the creator's store 002E3546 as a third writer.
    (CX, "| `+0x138` | 8 | 2 / 20 |",
     "| `+0x138` | 8 | ~~2 / 20~~ 3 / 20 *(answered: see the note above — `002E3546` is the third writer" + E + " |"),

    # Section 3.3 stale claims.
    # C-S1
    (SR, "> ends. No allocation site was read, so the record may be larger. The type store says so.",
     "> ends. ~~No allocation site was read, so the record may be larger.~~ *(answered: see \"Records are 720 to "
     "1,760 bytes, by kind\" below — the allocation site `002679F0` was read" + E + " The type store says so."),
    (SR, "| The record's true size | **not established** — `0x11C` is a lower bound | — | UNKNOWN |",
     "| The record's true size | ~~**not established** — `0x11C` is a lower bound~~ 720 to 1,760 bytes by kind "
     "*(answered: see \"Records are 720 to 1,760 bytes, by kind\"" + E + " | — | UNKNOWN |"),
    (SR, "**Not claimed:** the record's true size stays `UNKNOWN` (`0x11C` remains a lower bound), and no field's",
     "**Not claimed:** ~~the record's true size stays `UNKNOWN` (`0x11C` remains a lower bound), and~~ *(answered: "
     "the size was settled later — \"Records are 720 to 1,760 bytes, by kind\"" + E + " no field's"),
    (IC, "The extent is where the highest field this routine touches ends; **no allocation site was read**.",
     "The extent is where the highest field this routine touches ends; ~~**no allocation site was read**~~ *(answered: "
     "see the record's true size, CLOSED 2026-09-23, §14" + E + "."),
    # C-S2
    (SR, "| Same type as the movement actor | two offsets agree with complementary masks | 3 | **PROBABLE** |",
     "| Same type as the movement actor | two offsets agree with complementary masks; the carve loop writes `+0x03` "
     "itself *(answered: see \"`EH-1` answered — PROVEN, not probable\"" + E + " | 3 | ~~**PROBABLE**~~ PROVEN |"),
    (IC, "**This contract does not claim\n  the two types are one**, which is precisely §14's point.",
     "**This contract does not claim\n  the two types are one**, which is precisely §14's point *(answered: §14's "
     "`EH-1` item is CLOSED 2026-09-23 — the owning page resolved it PROVEN" + E + "."),
    # C-S3
    (SR, "| `00266AD0`, `00266BD0`, `00268EA0`, `003DB580` | 211/96/439/183 B | `ActorEntity` callees — **not read** |",
     "| `00266AD0`, `00266BD0`, `00268EA0`, `003DB580` | 211/96/439/183 B | `ActorEntity` callees — ~~**not read**~~ "
     "read later on this page *(answered: see the region map, §12–§13, and the `+0x1C` passes" + E + " |"),
    (SR, "| `00265FF0`, `00268380` | 1,339/420 B | `Movement` callees — **not read** |",
     "| `00265FF0`, `00268380` | 1,339/420 B | `Movement` callees — ~~**not read**~~ *(answered: `00265FF0` is read "
     "on the-movement-and-secondary-context-censuses.md, UQ-91; `00268380` in "
     "CONTRACT-actor-storage-record-initialisation.md's pass-22 section" + E + " |"),
    # C-S4: 00266530 calls the planter 00266AD0 at 002665A9.
    (SR, "- **`+0xB8` is not initialised here.** Whatever sets the context pointer runs elsewhere; a record\n"
         "  fresh from this routine still points at the previous occupant's context until it does.",
     "- ~~**`+0xB8` is not initialised here.** Whatever sets the context pointer runs elsewhere; a record~~\n"
     "  ~~fresh from this routine still points at the previous occupant's context until it does.~~ *(answered: see "
     "§16's table, \"`00266B54` plants the pointer\" — `00266530` calls the planter `00266AD0` at `002665A9`" + E),
    # C-S5
    (SR, "| lifetime / destruction | **no destructor identified.** The pool is carved once",
     "| lifetime / destruction | ~~**no destructor identified.**~~ *(answered: see \"RETRACTED 2026-09-21 (OPUS): the "
     "pool IS released\"" + E + " The pool is carved once"),
    (SR, "proves records are never destroyed | **NOT answered** |",
     "proves records are never destroyed | ~~**NOT answered**~~ answered *(answered: RETRACTED 2026-09-21" + E + " |"),
    (SR, "remains is the runtime confirmation, and that is blocker 1.\n",
     "remains is the runtime confirmation, and that is blocker 1. *(answered: the absence claim is retracted — see "
     "\"RETRACTED 2026-09-21 (OPUS): the pool IS released\"" + E + "\n"),
    # C-S6
    (SR, "`+0x14` bit 5 (`FRP-1` owns it as not\n      established).",
     "`+0x14` bit 5 (~~`FRP-1` owns it as not~~\n      ~~established~~ the script enable flag *(answered: `FRP-1`, "
     "2026-09-18, in the bit table above" + E + ")."),
    (SF, "bit 5 set at init (meaning open),",
     "bit 5 set at init (~~meaning open~~ the script enable flag *(answered: `FRP-1`, 2026-09-18, "
     "the-field-runtime-pass.md §4" + E + "),"),
    (FC, "bit 5 is read by seven sites and unexplained,",
     "bit 5 is read by seven sites and ~~unexplained~~ is the script enable flag *(answered: see open item 1, `FRP-1`, "
     "2026-09-18" + E + ","),
    # C-S7
    (SR, "      to `SWE2-DATA` as an argument census, and the preserved-bit pattern",
     "      to `SWE2-DATA` as an argument census *(answered: see the 2026-09-27 correction above, \"the engine does "
     "set all eight\"" + E + ", and the preserved-bit pattern"),
    # C-S8
    (SR, "      > through verb `03DF` `seteventwakerect` and read by a shared predicate `talktreasure`,",
     "      > through verb `03DF` `seteventwakerect` and read by ~~a shared predicate~~ the request-bit clearer "
     "*(answered: see the 2026-09-16 correction, \"the request-bit clearer\"" + E + " `talktreasure`,"),
    # C-S9
    (SR, "`+0x64`–`+0x88`. `ActorStorageRecord` declares 1,662 of 1,760 bytes, not 1,698.",
     "`+0x64`–`+0x88` *(answered: CLOSED 2026-09-12 — the script VM's register file, four `int32` at `+0x64`–`+0x70` "
     "and four `float` at `+0x74`–`+0x80`; see §2's `+0x64` row" + E + ". `ActorStorageRecord` declares 1,662 of "
     "1,760 bytes, not 1,698."),
    # C-S10: the census now carries 96 ctor rows for 00266530 (002666F1 / 00266A3A / 00266A4E / 0026670D among them);
    #        002679F0's +0x03 stores are still absent.
    (SF, "`00266A4E`) are not in the TSV.",
     "`00266A4E`) ~~are not in the TSV~~ were not in the TSV when this was written *(answered: the TSV now carries 96 "
     "`ctor` rows for `00266530`, these among them; `002679F0`'s `+0x03` stores are still absent — measured" + E +
     "."),
    (SF, "`actor-storage-record-accesses.tsv`**, so the table above reports",
     "`actor-storage-record-accesses.tsv`** *(answered: it is now — a `ctor` row of `00266530`, measured" + E +
     ", so the table above reports"),
    # C-S11
    (PC, "- **Nothing here has been observed in a running game.** The check below still stands.",
     "- ~~**Nothing here has been observed in a running game.**~~ *(answered: the region map was observed live "
     "afterwards in `EXP-026`, §13's opening" + E + " The check below still stands."),
    (PC, "executed** (§13), so no row claims more than static evidence.\n",
     "executed** (§13), so no row claims more than static evidence. *(answered: §13 — executed 2026-09-12 as the "
     "region-map pilot and observed live in `EXP-026`" + E + "\n"),
    # C-S12
    (PC, "entries: [\"00267A20\", \"00266AD0\", \"00266530\"]\n",
     "entries: [\"00267A20\", \"00266AD0\", \"00266530\"]  # <- corrected 2026-10-02, OPUS - 00267A20 is an interior "
     "address of 002679F0 (section 7)\n"),
    (PC, "- **The pool allocation `00267A20` and the record initialiser",
     "- **The pool allocation ~~`00267A20`~~ `002679F0` *(answered: §7 — `00267A20` is an interior address of it" + E
     + " and the record initialiser"),
    # C-S13: the interpreter loads +0x68 / +0x70 (00261855 / 0026187D).
    (PC, "  > pointer — in the binder's family or anywhere else, so the five copies are **dead stores** that\n"
         "  > the register file overwrites as soon as a script pops a register.",
     "  > pointer — in the binder's family or anywhere else, so the five copies are ~~**dead stores** that~~\n"
     "  > ~~the register file overwrites as soon as a script pops a register.~~ *(answered: see \"CORRECTED 2026-09-20 "
     "(SWE2-CONTRACT)\" below — the stores land on the slot, and the interpreter loads `+0x68` / `+0x70` at "
     "`00261855` / `0026187D`" + E),
    # C-S14
    (FL, "ordinary reading and this sheet does not choose between them",
     "ordinary reading and ~~this sheet does not choose between them~~ *(answered: a per-unit copy — CB-7, "
     "2026-09-12, below" + E),
    # C-S16
    (BU, "`+0x158`, `+0x6C0`, `+0x74C`, `+0x758`, `+0xB90` —",
     "`+0x158`, `+0x6C0`, `+0x74C`, `+0x758`, ~~`+0xB90`~~ *(answered: `+0xB90` has a reader — operand-store kind 10, "
     "corrected 2026-09-30 above" + E + " —"),
    # C-S17
    (BU, "(§2.3) — and, for the twelve tunables, the FCP property catalogue (FW-1).",
     "(§2.3) — and, for the twelve tunables, the FCP property catalogue (FW-1, *answered by consumer 2026-09-26 — "
     "see the tunables row* *(answered: see the `+0x164` row" + E + ")."),
    (BU, "  twelve tunables' properties (**FW-1**) and",
     "  twelve tunables' properties (**FW-1**, *(answered: by consumer, 2026-09-26, the `+0x164` row" + E + ") and"),
    # C-S18
    (BU, "| What the untouched ranges and the unnamed fields are | **not established** | — | UNKNOWN |",
     "| What the untouched ranges and the unnamed fields are | ~~**not established**~~ *(answered in part: "
     "`+0x298`–`+0x68F` is the navigation path record's waypoint table, FF-2, 2026-09-26" + E + " | — | UNKNOWN |"),
    (BU, "`+0x200`–`+0x297` the\n  navigation path state,",
     "~~`+0x200`–`+0x297`~~ `+0x200`–`+0x68F` *(answered: see the 2026-09-26 answer below" + E + " the\n"
     "  navigation path state,"),
    # C-S19
    (BP, "meaning**, and the span stays `DISCOVERED` / `UNKNOWN`.",
     "meaning**, and the span ~~stays `DISCOVERED` / `UNKNOWN`~~ *(answered: `+0x298`–`+0x68F` is entries 1–127 of "
     "the navigation path record's waypoint table — the-battle-unit-field-map.md FF-2, 2026-09-26" + E + "."),
    (BP, "**`+0x298` is written by the acquire-side clear and read by nothing in the shipped image that\n"
         "static analysis can reach.**",
     "**`+0x298` is written by the acquire-side clear ~~and read by nothing in the shipped image that~~\n"
     "~~static analysis can reach~~.** *(answered: it is reached by index, as the waypoint table — "
     "the-battle-unit-field-map.md FF-2, 2026-09-26" + E),
    # C-S20
    (BU, "`00383670` `Navigation_SelectNextWaypointXZ` (1,223 B) — the waypoint",
     "`00383670` `Navigation_SelectNextWaypointXZ` ~~(1,223 B)~~ (204 B) *(answered: see the 2026-09-19 correction "
     "below; the body ends at `0038373B ret`" + E + " — the waypoint"),
    # C-S21
    (BP, "| `00234200` | `ActorSystem_ReleaseBattleUnitSlotForActor` | not read |",
     "| `00234200` | `ActorSystem_ReleaseBattleUnitSlotForActor` | ~~not read~~ *(answered: see \"The slot is "
     "scrubbed on RELEASE too\" below" + E + " |"),
    # C-S22
    (BP, "accessor admits 1 or 3; what classes 0 and 1 hold is the residue (§2).",
     "accessor admits 1 or 3; ~~what classes 0 and 1 hold is the residue (§2).~~ *(answered: §2, BV-4 — class 0 the "
     "script-only controller, class 1 the placed never-moving object" + E),
    # C-S23
    (HB, "then `002B58B0(that)` → `r14` — an unread resolver (`FB-1`) |",
     "then `002B58B0(that)` → `r14` — ~~an unread resolver~~ the resolver (`FB-1`) *(answered: FB-1, §3" + E + " |"),
    # C-S24
    (HB, "unit `+0x10`. Its meaning beyond the call list is not read.",
     "unit `+0x10`. ~~Its meaning beyond the call list is not read.~~ *(answered: `003243F0` is the unit retire "
     "helper, §3" + E),
    # C-S25
    (HB, "Which reader consumes unit `+0x18` — and therefore whether it is\nthe unit's display name — is `FB-6`.",
     "~~Which reader consumes unit `+0x18` — and therefore whether it is~~\n~~the unit's display name — is `FB-6`.~~ "
     "*(answered: FB-6 closed 2026-09-12, §3" + E),
    # C-S26
    (HB, "installer and the rotation** — the reader of the spawn record's `+0x12` copy is still open (`FB-3`).",
     "installer and the rotation** — ~~the reader of the spawn record's `+0x12` copy is still open (`FB-3`).~~ "
     "*(answered: FB-3, 2026-09-12, §3, with the second reader `00329220` added 2026-10-02" + E),
    (HB, "  `+0x12`. What reads that copy is `FB-3`.",
     "  `+0x12`. ~~What reads that copy is `FB-3`.~~ *(answered: FB-3, §3" + E),
    # C-S27
    (HB, "| What the remaining unread callees and unnamed row fields are | **not established** | — | UNKNOWN |",
     "| What the remaining unread callees and unnamed row fields are | ~~**not established**~~ *(answered: FB-4, §3" + E
     + " | — | UNKNOWN |"),
    # C-S29: the installer reads the six fields from the .ard slot-0 class row (0023A8E6-0023A910, r15).
    (HB, "is 0 or `0xFF` (66 / 2,226) — so the type, kind, facing and perception the installer uses come\n"
         "  from the *page*, not the row,",
     "is 0 or `0xFF` (66 / 2,226) — so ~~the type, kind, facing and perception the installer uses come~~\n"
     "  ~~from the *page*, not the row,~~ *(answered: the installer reads them from the `.ard` slot-0 class row, "
     "corrected 2026-09-12 in §2.2" + E + " the spawn row's own copies are unused, and"),
    # C-S30
    (HB, "EXP-047 executed the two wrappers' local stores in isolation; the delegate's effects are the static\n"
         "reading above.",
     "EXP-047 executed the two wrappers' local stores in isolation; ~~the delegate's effects are the static~~\n"
     "~~reading above.~~ *(answered: EXP-151 executed the rekey inner `003220E0` through `00322050` end-to-end — "
     "CONTRACT-battle-unit-construction.md" + E),
    (CB, "- **`EXP-047`** executed the two re-key wrappers' local stores; the delegate's effects remain static.",
     "- **`EXP-047`** executed the two re-key wrappers' local stores; ~~the delegate's effects remain static.~~ "
     "*(answered: EXP-151 executed the delegate end-to-end, below" + E),
    # C-S31
    (DR, "| `0031FEC0`, `0031FF70` | 167 / 199 B | two more callers, unread |",
     "| `0031FEC0`, `0031FF70` | 167 / 199 B | two more callers, ~~unread~~ actor-to-slot wrappers *(answered: see "
     "the 2026-09-12 half answer below" + E + " |"),
    # C-S32
    (DR, "| What the predicates and the three party-row words are | **not established** | — | UNKNOWN |",
     "| What the predicates and the three party-row words are | ~~**not established**~~ *(answered: FJ-1 and the "
     "2026-09-26 answer above" + E + " | — | UNKNOWN |"),
    # C-S33
    (DR, "  +0x60 u16 type  +0x62 u16 kind  +0x64 u16 page+0x52 (kind 1)   +0x66 u8[32] per-status countdown "
         "(0xFE = n/a)\n",
     "  +0x60 u16 type  +0x62 u16 kind  +0x64 u16 page+0x52 (kind 1)   +0x66 u8[32] per-status countdown "
     "(0xFE = n/a)   <- corrected 2026-10-02, OPUS - +0xE68 is the .ard class row, not a page (corrected 2026-09-13 "
     "above; 003298EA-0032990D)\n"),
    (DR, "`+0x64 = page +0x52 of unit +0xE68` for a kind-1 unit",
     "~~`+0x64 = page +0x52 of unit +0xE68`~~ `+0x64 = class row +0x52 of unit +0xE68` *(answered: `+0xE68` is the "
     "class row, corrected 2026-09-13 above" + E + " for a kind-1 unit"),
    (DR, "            -> unit +0x708/+0x710/+0x714/+0x6B4/+0x768/+0x76C/+0xBA0 ; spawn record +0x12 ; page +0x52\n",
     "            -> unit +0x708/+0x710/+0x714/+0x6B4/+0x768/+0x76C/+0xBA0 ; spawn record +0x12 ; page +0x52   <- "
     "corrected 2026-10-02, OPUS - class row +0x52 of [unit+0xE68], not a page\n"),
    # C-S34
    (TI, "- **Whether kind values other than 0 and 1 exist** — still the parent document's open item.",
     "- ~~**Whether kind values other than 0 and 1 exist** — still the parent document's open item.~~ *(answered: AL-4, "
     "2026-09-12 — `{0, 1}`, from the writer; battle-record-kind-byte.md §7" + E),
    # C-S35
    (TI, "What the thirteen types *are*, and what a presentation code selects, are untouched.",
     "~~What the thirteen types *are*, and~~ What a presentation code selects ~~, are~~ is untouched *(answered in "
     "part: §12 names the thirteen types — the Espers" + E + "."),
    # C-S36
    (KB, "`BattleUnit_ResetStateForReuse` (`00236AB4`); the byte is **authored definition data**, set",
     "`BattleUnit_ResetStateForReuse` (`00236AB4`); the byte is ~~**authored definition data**~~ definition data "
     "*(answered: see \"CORRECTED: this is not a shared authored definition\" — only the word \"authored\" was too "
     "strong" + E + ", set"),
    # C-S37
    (KB, "Open: joining the other values, including 6",
     "~~Open:~~ *(answered: see `GR-2` below, 2026-09-30" + E + " joining the other values, including 6"),
    # C-S38
    (KB, "`Tools/work/rtti/unit_record_fields.tsv`. What most individual fields *mean* is still open.",
     "`Tools/work/rtti/unit_record_fields.tsv`. ~~What most individual fields *mean* is still open.~~ *(answered: see "
     "the note below — 69 of the 72 observed offsets have a name or meaning, and `FE-1` was answered 2026-09-26" + E),
    # C-S39
    (KB, "as specific as the evidence goes: the consumers are named, the individual bits are not.",
     "as specific as the evidence goes: the consumers are named, ~~the individual bits are not~~ *(answered on the "
     "spawn side: see AL-10 below" + E + "."),
    # C-S40
    (KB, "> set membership consulted by many questions — and it strengthens **AL-2** and **N-4** without\n"
         "> answering either:",
     "> set membership consulted by many questions — and it strengthens **AL-2** and **N-4** ~~without~~\n"
     "> ~~answering either~~ *(answered: both on 2026-09-11 — see the correction below" + E + ":"),
    # C-S41
    (NM, "a guard\nwhose index arithmetic on a negative id is the page's open item.",
     "a guard\nwhose index arithmetic on a negative id ~~is the page's open item~~ *(answered: FN-2, 2026-09-14, §7"
     + E + "."),
    # C-S42 / B-6 (label left to the page owner: the page's own answer gives no confidence word)
    (NM, "| Kind 9 = the language `bin` block | index match and layout match only | 2 | PLAUSIBLE |",
     "| Kind 9 = the language `bin` block | ~~index match and layout match only~~ index match, layout match and the "
     "loader read (`002DF780`, `002DF9A0`) *(answered: see UQ-92, answered 2026-09-14" + E + " | 2 | PLAUSIBLE |"),
    # C-S43
    (MF, "The names of the members remain open; the layout does not depend on them.",
     "~~The names of the members remain open;~~ *(answered: CONTRACT-manager-slot-entry-tables.md names them — "
     "`definitionValue`, `lookupIndex`, `recordIndex`, `clock`, `rate`, `clockRunning`" + E + " the layout does not "
     "depend on them."),
    (MF, "| `+0x018` | 2 |  | *not named by any page* |",
     "| `+0x018` | 2 |  | ~~*not named by any page*~~ the side-A reverse-lookup words (`003DA4B9`) *(answered: "
     "CONTRACT-manager-slot-entry-tables.md, and FH-1's 2026-09-27 note — named by the store" + E + " |"),
    # C-S45
    (MC, "**45 mutants: 34 KILLED · 4 EQUIVALENT · 4 SURVIVED · 3 NO_BUILD · 0 TIMEOUT · 0 INVALID.**\n",
     "~~**45 mutants: 34 KILLED · 4 EQUIVALENT · 4 SURVIVED · 3 NO_BUILD · 0 TIMEOUT · 0 INVALID.**~~ *(answered: "
     "superseded by the 49-point run below" + E + "\n"),
    (MC, "**The suite has been mutation-tested: 45 mutants, 34 killed, 4 proven byte-identical,",
     "**The suite has been mutation-tested: ~~45 mutants, 34 killed~~ 49 points, 38 killed *(answered: §13's 49-point "
     "run supersedes the 45-mutant line" + E + ", 4 proven byte-identical,"),
    # C-S46
    (MC, "   > runtime range of `getcamerasubframe`, is the residue for the contract's owner.",
     "   > ~~runtime range of `getcamerasubframe`, is the residue for the contract's owner.~~ *(answered: see the "
     "2026-09-12 note above — the writes past `+0x1B` are real stores, and `getcamerasubframe` is a `mov eax, 1` / "
     "`ret` stub" + E),
    # C-S47
    (CX, "pointers, not the record offsets.** The planter has a second\n"
         "  branch that points them elsewhere; code that assumes `record+0x120` will be wrong there.",
     "pointers, not the record offsets.** ~~The planter has a second~~\n"
     "  ~~branch that points them elsewhere; code that assumes `record+0x120` will be wrong there.~~ *(answered: there "
     "is no second branch — see \"CORRECTED 2026-09-11\" in §2; `+0xB8` is `rec + 0x120` or NULL, `+0xC0` "
     "`rec + 0x350` or NULL, `00266AFB`–`00266B68`" + E),
    # C-S48
    (CX, "delta.md)). The write that assigns a real index is not in this census (`FS-2`) |",
     "delta.md)). ~~The write that assigns a real index is not in this census (`FS-2`)~~ *(answered: the element "
     "binder `002E3110` — FS-2, 2026-09-17, §7" + E + " |"),
    # C-S49
    (CX, "| `+0x14C` | 1 | 0 / 1 |",
     "| `+0x14C` | 1 | ~~0 / 1~~ 1 / 1 *(answered: the 2026-09-26 correction above" + E + " |"),
    (CX, "| `+0x14D` | 1 | 0 / 1 |",
     "| `+0x14D` | 1 | ~~0 / 1~~ 1 / 1 *(answered: the 2026-09-26 correction above" + E + " |"),
    (CX, "| `+0x14E` | 1 | 0 / 1 |",
     "| `+0x14E` | 1 | ~~0 / 1~~ 1 / 1 *(answered: the 2026-09-26 correction above" + E + " |"),
    # C-S51
    (FC, "frame you triggered it**: the actor is driven, asked whether it settled, and driven again.",
     "frame you triggered it**: the actor is driven ~~, asked whether it settled, and driven again~~ once per loop "
     "that names it *(answered: the inner repeat is dead code — §6, and the-field-runtime-pass.md §4, corrected "
     "2026-09-12" + E + "."),
    (FP, "> **One actor is driven repeatedly inside one frame until it settles.** The loop exits on bit `0x40`",
     "> ~~**One actor is driven repeatedly inside one frame until it settles.**~~ *(answered: see \"Corrected "
     "2026-09-12 (FABLE): nothing ever sets the low nibble\" below — each actor is driven once per loop that names "
     "it" + E + " The loop exits on bit `0x40`"),
    (FP, "> **There is no iteration cap.** A script that keeps work pending",
     "> ~~**There is no iteration cap.**~~ *(answered: the loop is dead code, below" + E + " A script that keeps work "
     "pending"),
    # C-S52
    (FC, "1,297-byte pass. There is no live evidence and the pass itself is still unexecuted.**",
     "1,297-byte pass. There is no live evidence ~~and the pass itself is still unexecuted~~.** *(answered: the pass "
     "body was executed from shipped bytes 2026-09-18, §13a" + E),
    (FC, "**Not claimed:** no live observation, and the pass itself is still unexecuted — §13's",
     "**Not claimed:** no live observation~~, and the pass itself is still unexecuted~~ *(answered: §13a, executed "
     "2026-09-18" + E + " — §13's"),
    # C-S53
    (FC, "   > that is consumed; this one never is.",
     "   > that is consumed; ~~this one never is~~ this one is cleared in two places *(answered: see the CORRECTION "
     "2026-09-21 below" + E + "."),
    (FC, "   > If the mark is truly never cleared, then a manager disposed once",
     "   > ~~If the mark is truly never cleared, then~~ *(answered: the mark is cleared — the CORRECTION 2026-09-21 and "
     "\"DISSOLVED rather than answered\" below" + E + " If it were never cleared, a manager disposed once"),
    # C-S54
    (FP, "  `0x012`–`0x047`, `0x050`–`0x057` and `0x068`–`0x287` are undeclared, which is 614 of 648 bytes.",
     "  `0x012`–`0x047`, `0x050`–`0x057` and `0x068`–`0x287` ~~are undeclared, which is 614 of 648 bytes~~ "
     "*(answered: CONTRACT-field-runtime-pass.md declares `+0x12`, `+0x13`, `+0x17`, `+0x20`, `+0x24`, `+0x38`, "
     "`+0x200`, and the actor-manager record field map maps 57 offsets" + E + "."),
    # C-S55
    (FP, "Whether a wider store reaches an actor record's `+0x14` is **not** settled by this pass either — it",
     "~~Whether a wider store reaches an actor record's `+0x14` is **not** settled by this pass either~~ *(answered: "
     "see \"Reconciled 2026-09-30\" below" + E + " — it"),
    # C-S56
    (FP, "> save meaning comes from the ledger name and from whoever writes `02CA99E8`, which this document\n"
         "> has not read.",
     "> save meaning comes from the ledger name and from whoever writes `02CA99E8`, ~~which this document~~\n"
     "> ~~has not read~~ *(answered: \"Read 2026-09-11\", the next paragraph" + E + "."),

    # Section 3.4 banners: README statuses against each page's front matter; the kind-byte page's body banner.
    (R, "  **DOCUMENTED, tier 1.** The fixed BattleUnit pool",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "fixed BattleUnit pool"),
    (R, "  **DOCUMENTED, tier 1.** The 3,920-byte battle unit,",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "3,920-byte battle unit,"),
    (R, "  **DOCUMENTED, tier 1.** The 648-byte manager record,",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "648-byte manager record,"),
    (R, "  **DOCUMENTED, tier 1.** A companion to the record page:",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* A "
     "companion to the record page:"),
    (R, "  **DOCUMENTED, tier 1.** The party member status view:",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "party member status view:"),
    (R, "  **PARTIAL, tier 1.** The two regions every actor record reaches",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`, both "
     "open items answered 2026-09-17)* The two regions every actor record reaches"),
    (KB, "**PARTIAL — deliberately.** The census is exact",
     "~~**PARTIAL — deliberately.**~~ **DOCUMENTED.** " + C + "the front matter says `status: DOCUMENTED`, and the "
     "note below records GR-2 answered)* The census is exact"),
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
