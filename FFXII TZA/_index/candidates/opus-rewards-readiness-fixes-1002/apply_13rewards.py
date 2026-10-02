"""apply_13rewards.py [--apply] - 13-Rewards-Progression-Economy readiness map (readiness-13-rewards.md), section 2.4
contradictions 1-43 and the two section 2.5 image findings, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the map's dated correction, the bytes or the shipped data
refute) and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing comment instead of a strike; their OLD runs into the next line so NEW never
contains OLD. Headings that change carry OPUS (publish heading gate).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "13-Rewards-Progression-Economy/"
R = F + "README.md"
CH = F + "the-chain-and-its-sticky-coin.md"
LD = F + "loot-drops-and-enemy-chain.md"
AW = F + "experience-and-license-point-award.md"
HX = F + "how-experience-is-computed-and-divided.md"
CXL = F + "CONTRACT-experience-and-licence-award.md"
DE = F + "what-happens-when-an-enemy-dies.md"
CDR = F + "CONTRACT-defeat-rewards-sequence.md"
GL = F + "gil-storage-clamp-and-every-path-that-moves-it.md"
CGL = F + "CONTRACT-gil-storage-and-movement.md"
LU = F + "what-happens-when-a-character-levels-up.md"
CLU = F + "CONTRACT-level-advance-and-growth.md"
CLC = F + "CONTRACT-loot-rolls-and-the-chain.md"
WL = F + "world-loot-pickups-the-ten-slot-pool-and-the-despawn.md"
CWL = F + "CONTRACT-world-loot-pickup-pool.md"

EDITS = [
    # C1: guests earn EXP, but LP only for row 6 (002F90E7-002F90F5 admits 0..6, 0x1A, >=0x28).
    (AW, "receives the full amount. Guests earn both. A summoned",
     "receives the full amount. ~~Guests earn both.~~ Guests earn experience; of the eleven guests only Reks (party "
     "row 6) can also earn license points *(corrected 2026-10-02, OPUS: checked at `002F90E7`–`002F90F5` — the LP "
     "filter admits ids `0..6`, `0x1A` and `≥ 0x28`, so guest rows 7–16 are refused; "
     "CONTRACT-experience-and-licence-award.md §4)*. A summoned"),
    (AW, "Esper earns no EXP or LP; a guest does.",
     "Esper earns no EXP or LP; ~~a guest does~~ a guest earns EXP, and LP only for row 6, Reks *(corrected "
     "2026-10-02, OPUS: `002F90E7`–`002F90F5`; CONTRACT-experience-and-licence-award.md §4)*."),

    # C2: chain rank does reach the loot rolls (00318116 mov r12d, [022C3158]); AE-7 reversed 2026-09-12.
    (LD, "  -> Loot_SelectChanceProfileByWeight (00318820)     LCG draw -> which profile\n     -> Loot_RollNormalSlotChance",
     "  -> Loot_SelectChanceProfileByWeight (00318820)     LCG draw -> which profile   <- corrected 2026-10-02, OPUS: "
     "only while 022C3164 > 0; otherwise the chance profile is the chain rank 022C3158 (Loot_RollDropEntries "
     "003180F0, 00318116, 0031815C-0031816A)\n     -> Loot_RollNormalSlotChance"),
    (LD, "**AE-7 ANSWERED in section 8b — not in\n      the functions read.** No chain global appears in any `Loot_*` function.",
     "**AE-7 ANSWERED in section 8b — ~~not in~~\n      ~~the functions read.~~** ~~No chain global appears in any "
     "`Loot_*` function.~~ **Yes** — reversed by §8b's correction of 2026-09-12: `Loot_RollDropEntries` (`003180F0`) "
     "takes the chance profile from the chain rank `022C3158` (`00318116`), so chain rank sets the drop chance and "
     "the model streak the quantity *(corrected 2026-10-02, OPUS: checked at `00318116`)*."),
    (LD, "### AE-7 answered - no, chain rank does not reach the loot rolls",
     "### AE-7 answered - ~~no, chain rank does not reach the loot rolls~~ yes, chain rank sets the drop chance "
     "(corrected 2026-10-02, OPUS)"),
    (LD, "**In the functions read, it does not.** All 22 references to the chain globals (`DAT_022C3158`,\n"
         "`DAT_022C315C`, `DAT_022C3170`, `DAT_022C3174`) fall inside `EnemyChain_UpdateOnDefeat` and\n"
         "`EnemyChain_TryAdvanceRank`. **Not one appears in any `Loot_*` function.**",
     "~~**In the functions read, it does not.** All 22 references to the chain globals (`DAT_022C3158`,~~\n"
     "~~`DAT_022C315C`, `DAT_022C3170`, `DAT_022C3174`) fall inside `EnemyChain_UpdateOnDefeat` and~~\n"
     "~~`EnemyChain_TryAdvanceRank`. **Not one appears in any `Loot_*` function.**~~ **It does:** "
     "`Loot_RollDropEntries` (`003180F0`) reads the chain rank `022C3158` at `00318116`, a reference the "
     "22-reference census missed *(corrected 2026-10-02, OPUS: checked at `00318116`; see the correction below)*."),
    (LD, "**the caller choosing a different profile index** -\na path that has not been read. The negative is bounded "
         "to the six functions examined, and recorded\nthat way rather than as \"chain does not affect loot\".",
     "**the caller choosing a different profile index** -\n~~a path that has not been read. The negative is bounded "
     "to the six functions examined, and recorded~~\n~~that way rather than as \"chain does not affect loot\".~~ "
     "*(answered: see the correction above — the caller `003180F0` takes the chance profile index from the chain "
     "rank at `00318116`, so chain rank does reach the drop chance; 2026-10-02, OPUS)*"),

    # C3: a profile is a chain level, not an enemy class; row +0x05 is read (003181C7-003181DE, AE-12/AE-13).
    (LD, "**Chance and quantity live in the same row**, indexed off the same profile - so a \"profile\" is a\n"
         "complete drop table for one enemy class: five chances followed by five groups of four weights.",
     "**Chance and quantity live in the same row**, ~~indexed off the same profile - so a \"profile\" is a~~\n"
     "~~complete drop table for one enemy class:~~ but a drop reads them from two rows: the chance from the "
     "chain-rank row (or a weighted draw after a chain break) and the quantity from the same-model-tier row, so a "
     "profile is a chain level, not an enemy class *(corrected 2026-10-02, OPUS: `00318116`, `0031815C`–`0031816A`, "
     "`003181C7`–`003181DE`; §7 AE-12, AE-13)*. Each row holds five chances followed by five groups of four weights."),
    (LD, "The **profile index** passed to both functions still comes from the caller, unread - so which\n"
         "profile a given enemy uses is unknown, and AE-7's negative (chain rank does not reach the loot\n"
         "rolls) still leaves that path open. **AE-12.**",
     "~~The **profile index** passed to both functions still comes from the caller, unread - so which~~\n"
     "~~profile a given enemy uses is unknown, and AE-7's negative (chain rank does not reach the loot~~\n"
     "~~rolls) still leaves that path open.~~ **AE-12.** *(answered: see §7 AE-12 and §8b's 2026-09-12 correction — "
     "the caller `003180F0` passes the chain rank as the chance profile (`00318116`) and the same-model tier as the "
     "quantity profile; no enemy has a profile of its own; 2026-10-02, OPUS)*"),
    (LD, "The byte at row `+0x05` is not touched by either function. **AE-13.**",
     "~~The byte at row `+0x05` is not touched by either function.~~ **AE-13.** *(answered: see §7 AE-13 — the "
     "caller `003180F0` reads it as the row's same-model requirement, `003181C7`–`003181DE`; 2026-10-02, OPUS)*"),
    (LD, "row + 0x05           NOT read by any consumer seen\nrow + 0x06",
     "row + 0x05           NOT read by any consumer seen   <- corrected 2026-10-02, OPUS: read by "
     "Loot_RollDropEntries 003180F0 as the same-model requirement (003181C7-003181DE, AE-13)\nrow + 0x06"),
    (LD, "  +0x05              -          unaccounted\n  +0x06 + slot*4",
     "  +0x05              -          unaccounted   <- corrected 2026-10-02, OPUS: i8 same-model requirement "
     "8/16/24/-1, read by 003180F0 (003181C7-003181DE, AE-13)\n  +0x06 + slot*4"),

    # C4: 022C3164 > 0 on every chain-break kill (00318088-003180B5), so the chance profile is drawn (0031815C-0031816A).
    (LD, "2026-09-12 (FABLE):** none of its own — the chance profile is the **chain rank** (0–3) and the",
     "2026-09-12 (FABLE):** none of its own — ~~the chance profile is the **chain rank** (0–3)~~ the chance profile "
     "is the **chain rank** (0–3) except on a kill that breaks a live chain (every kill, while the player "
     "alternates genera), when `022C3164` is positive and `Loot_SelectChanceProfileByWeight` (`00318820`) draws it "
     "*(corrected 2026-10-02, OPUS: checked at `00317F6A`, `00318088`–`003180B5` and `0031815C`–`0031816A`)*; and the"),
    (CLC, "- Whether `[022C3164]` is ever positive in shipped play, which decides if the chance profile is ever\n"
          "  drawn rather than taken from the rank.",
     "- ~~Whether `[022C3164]` is ever positive in shipped play, which decides if the chance profile is ever~~\n"
     "  ~~drawn rather than taken from the rank.~~ *(answered: yes — `00317ED0` increments it on every genus switch "
     "from a live chain (`00318088`–`003180B5`) before `003180F0` runs for the same kill, and zeroes it only on a "
     "continued chain (`00317F6A`), so a kill that breaks a chain draws its chance profile through `00318820`; see "
     "loot-drops-and-enemy-chain.md §7 AE-12; 2026-10-02, OPUS)*"),

    # C5: rank 2 = HP/MP 20 %, Protect and Shell picker-only 5 % each; rank 3 = HP/MP 25 %, party-wide 5 % each.
    (LD, "tenths; rank 2 halves \"nothing\" and adds Protect (5 % picker-only, 5 % party-wide); rank 3 pushes\n"
         "> HP and MP to 25 % each and swaps the Protect rolls for Shell — the authored table",
     "tenths; rank 2 halves \"nothing\", ~~and adds Protect (5 % picker-only, 5 % party-wide)~~ raises HP and MP to "
     "20 % each and adds Protect and Shell for the picker alone, 5 % each; rank 3 pushes\n"
     "> HP and MP to 25 % each and ~~swaps the Protect rolls for Shell~~ swaps both picker-only rolls for their "
     "party-wide forms, Protect 5 % and Shell 5 % *(corrected 2026-10-02, OPUS: weights `01EED3B8` rows 2 and 3, "
     "variants `00D102C0`; outcomes 3 and 5 are picker-only at `003111DD`–`003111F1`)* — the authored table"),

    # C6: the extra-item query tests the condition word (Monograph / Canopic Jar), not the loot (00318527-00318533).
    (CLC, "calls `BattleEncodedId_QueryMode0Positive` `0030B0E0` on the item id before it draws, and skips the draw "
          "when the query answers 0;",
     "calls `BattleEncodedId_QueryMode0Positive` `0030B0E0` ~~on the item id~~ on the spawn row's condition word "
     "(`+0x48` / `+0x4C`, the Monograph or Canopic Jar the party must hold), not on the loot item, before it draws "
     "*(corrected 2026-10-02, OPUS: checked at `00318527`–`00318533` with `dx` from `0031823F` / `00318267`; "
     "loot-drops-and-enemy-chain.md §7 AE-8)*, and skips the draw when the query answers 0;"),
    (CLC, "consumes a draw only for an item id the encoded-id query accepts,",
     "consumes a draw only ~~for an item id the encoded-id query accepts~~ when the party holds the condition key "
     "item *(corrected 2026-10-02, OPUS: AE-8)*,"),
    (LD, "and the extra-item roll is gated on the encoded-id query for the item.",
     "and the extra-item roll is gated on the encoded-id query ~~for the item~~ for the spawn row's condition key "
     "item, not the loot *(corrected 2026-10-02, OPUS: `00318527`–`00318533`; §7 AE-8)*."),

    # C7: counter 11 is fed the LP (00312484 mov edx, esi; 00312489 mov cl, 0xb; 00312496 call 00316A50).
    (CDR, "the defeat body passes each recipient's experience award as counter 11 inside the recipient loop",
     "the defeat body passes each recipient's ~~experience award~~ awarded licence points as counter 11 inside the "
     "recipient loop *(corrected 2026-10-02, OPUS: `00312484 mov edx, esi` (the LP after clamp and conversion), "
     "`00312489 mov cl, 0xb`, `00312496 call 00316A50`)*"),

    # C8: the conversion tests effect id 12 in the effect layers (00312409 / 0031240F), not status 12 (Reverse).
    (CDR, "  +0x069 / +0x079  u8   the two status layers; bit 4 of byte 1 is status id 12 (DR-5)\n  +0x18C",
     "  +0x069 / +0x079  u8   the two status layers; bit 4 of byte 1 is status id 12 (DR-5)   <- corrected "
     "2026-10-02, OPUS: byte 1 of the two EFFECT layers +0x68 / +0x78; bit 4 is effect id 12 (LP -> gil), not "
     "status 12 (Reverse); what-happens-when-an-enemy-dies.md\n  +0x18C"),
    (CDR, "**DR-5 — Status id 12 CONVERTS",
     "**DR-5 — ~~Status id 12~~ Effect id 12 *(corrected 2026-10-02, OPUS: `00312409` / `0031240F` test the effect "
     "layers `+0x69` / `+0x79`, not the status words; status 12 is Reverse — what-happens-when-an-enemy-dies.md, "
     "\"An equipment effect that turns LP into gil\")* CONVERTS"),
    (CDR, "When bit 4 is set in either status layer (",
     "When bit 4 is set in either ~~status~~ effect layer *(corrected 2026-10-02, OPUS)* ("),
    (CDR, "- A recipient carrying status 12 receives",
     "- A recipient carrying ~~status 12~~ effect 12, the Cat-ear Hood's augment *(corrected 2026-10-02, OPUS: "
     "DR-5)*, receives"),
    (CDR, "The inherited status-12 conversion path",
     "The inherited ~~status-12~~ effect-12 *(corrected 2026-10-02, OPUS: DR-5)* conversion path"),

    # C9: lp = 0 (003122A9 xor ebp, ebp; 0031241F mov esi, ebp); the running total is never copied into LP.
    (DE, "**Replacement** — `lp` is overwritten with the running total's previous value before the award, so the "
         "recipient's LP add is zero.",
     "**Replacement** — ~~`lp` is overwritten with the running total's previous value before the award~~ `lp` is "
     "set to zero (`ebp` zeroed at `003122A9`, `0031241F mov esi, ebp`) *(corrected 2026-10-02, OPUS: the running "
     "total is never copied into LP; see the listing in \"An equipment effect that turns LP into gil\")*, so the "
     "recipient's LP add is zero."),

    # C10: the first EXP cap bounds +0x18C (00312432-00312444); +0x190 is the LP total (0031248F).
    (CDR, "accumulated into `[rdi+0x190]`; this one bounds",
     "accumulated into ~~`[rdi+0x190]`~~ `[rdi+0x18C]` *(corrected 2026-10-02, OPUS: the EXP accumulator, stored "
     "at `00312444`; `+0x190` is the LP total, `0031248F`)*; this one bounds"),

    # C11: an unowned record still posts event 4 (0030C7E4 precedes the owner test 0030C7ED).
    (CLU, "- A record no battle unit owns levels silently (`LU-7`).",
     "- A record no battle unit owns ~~levels silently~~ still levels and posts event 4 (`0030C7E4`, before the "
     "owner test at `0030C7ED`); only the forwarding and audio calls need an owner, so it is silent only when "
     "notification is suppressed (`LU-7`) *(corrected 2026-10-02, OPUS: §4 LU-7's correction of 2026-09-25)*."),

    # C12: growth is gated on the kind byte (0030C6D9-0030C6DD), so every kind-0 record holds the four floats.
    (LU, "f32 at `+0x10`–`+0x1C` exist only for party records of type `0x1B`–`0x27`; a spawn-backed record",
     "f32 at `+0x10`–`+0x1C` exist ~~only for party records of type `0x1B`–`0x27`~~ on every kind-0 "
     "(party-table) record, rows 0–5 included *(corrected 2026-10-02, OPUS: the growth block is gated on the kind "
     "byte `+5`, not the type id, `0030C6D9`–`0030C6DD`; §4 and CONTRACT-level-advance-and-growth.md)*; a "
     "spawn-backed record"),

    # C13: SetGil(-500) from 500 meters 1,000 (00254EF1-00254F02: delta on the raw argument; GL-3).
    (GL, "same intent expressed as `SetGil(-500)` meters **500** as well, but `SetGil(newValue)` computed by a",
     "same intent expressed as `SetGil(-500)` ~~meters **500** as well, but~~ meters **1,000**, the distance from "
     "500 to `-500`, because the delta is taken on the raw argument before the floor (`00254EF1`–`00254F02`; GL-3) "
     "*(corrected 2026-10-02, OPUS)*; generally, `SetGil(newValue)` computed by a"),

    # C14: the pool init writes slot indices 0..9 (00319C3E-00319C84).
    (WL, "pool record region (`02EC1000` set to 1, the rest to zero).",
     "pool record region (~~`02EC1000` set to 1, the rest to zero~~ each node's `slotIndex` set to its index "
     "`0…9`: `02EC0FA0` 0, `02EC1000` 1, `02EC1060` 2, … `02EC1300` 9 *(corrected 2026-10-02, OPUS: checked at "
     "`00319C3E`–`00319C84`; CONTRACT-world-loot-pickup-pool.md I1)*)."),

    # C15: a chain break leaves +0x7C7C = 0x9 (0028EF07 = 0, 0028EF18 |= 8, 0028EF26 |= 1).
    (LD, "chain-record field writes on the `[0209BE80]` manager — `dword[+0x7C7C] = 0` (`0028EF07`),",
     "chain-record field writes on the `[0209BE80]` manager — ~~`dword[+0x7C7C] = 0` (`0028EF07`)~~ "
     "`dword[+0x7C7C] = 0x9`: zeroed at `0028EF07`, then OR-ed with 8 (`0028EF18`) and with 1 (`0028EF26`) "
     "*(corrected 2026-10-02, OPUS: the-chain-and-its-sticky-coin.md)*,"),

    # C16: CH's "does not claim" list is answered on the loot page (AE-5, AE-6, AE-9, AE-10).
    (CH, "~~what `0028EF70` and `0028EF00` present,~~ what `003183D0` does,\n"
         "what the `u16` at `[actor + 0xE68] + 0x40` identifies, what the state predicate at `00229E40`\n"
         "distinguishes (it changes a clamp from 999 to 998 and adds 1 to a reported length), or what the coin's\n"
         "success actually causes — ",
     "~~what `0028EF70` and `0028EF00` present,~~ ~~what `003183D0` does,~~\n"
     "~~what the `u16` at `[actor + 0xE68] + 0x40` identifies, what the state predicate at `00229E40`~~\n"
     "~~distinguishes (it changes a clamp from 999 to 998 and adds 1 to a reported length), or what the coin's~~\n"
     "~~success actually causes~~ *(answered: see loot-drops-and-enemy-chain.md §7 — AE-5: `003183D0` is the rank "
     "advance; AE-6: the coin waives its pickup penalty (`0031841D`); AE-10: the `u16` is the model id palette-swaps "
     "share; AE-9: `00229E40` returns the language id; 2026-10-02, OPUS)* — "),

    # C17: a non-zero locale predicate selects 0x3E6 (00317F2D-00317F61): 999 Japanese, 998 otherwise.
    (CH, "(mask `0xD81`). Which clamp belongs to which locale is\nfor the locale page to state; this note only names "
         "the input.",
     "(mask `0xD81`). ~~Which clamp belongs to which locale is~~\n~~for the locale page to state; this note only "
     "names the input.~~ *(answered: see loot-drops-and-enemy-chain.md §7 AE-9 — locale 0, Japanese, makes the "
     "predicate zero and keeps the 999 cap; every other locale selects 998, `0x3E6` (checked at "
     "`00317F2D`–`00317F61`); 2026-10-02, OPUS)*"),

    # C18: the chain key +0x56 is the class row's type byte +5 (LD 8b, AE-11 note).
    (CH, "comparison target for the next kill. **Stated as a kind on that basis, not proven to be one.** |",
     "comparison target for the next kill. ~~**Stated as a kind on that basis, not proven to be one.**~~ "
     "*(answered: see loot-drops-and-enemy-chain.md §8b, the AE-11 note — `+0x56` is the class row's type byte "
     "`+5`, sixty-four values in the shipped areas; 2026-10-02, OPUS)* |"),

    # C19: the loot page's body banner against its own front matter (AUDITED).
    (LD, "**PARTIAL.** The roll shapes, the chain rank bounds and the RNG source are read at tier 1. The\n"
         "profile table layouts and the chain's full state machine are not.",
     "~~**PARTIAL.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED` and every "
     "§7 box is ticked)*. The roll shapes, the chain rank bounds and the RNG source are read at tier 1. ~~The~~\n"
     "~~profile table layouts and the chain's full state machine are not.~~ The profile table layouts (§8c) and the "
     "chain's state machine (§8b) are read too."),

    # C20: the seven outcomes are the pickup chain bonus (AE-3 answered 2026-09-12), not the drop rolls.
    (LD, "**What the player experiences.** This is the numeric core of *\"keep your chain up for better\ndrops\"*.",
     "**What the player experiences.** ~~This is the numeric core of~~ This is not the numeric core of *\"keep "
     "your chain up for better\ndrops\"* — that is the drop chance the chain rank sets (§8b) — but the pickup chain "
     "bonus, AE-3 below *(corrected 2026-10-02, OPUS: AE-3's answer)*."),
    (LD, "**Not established:** what the seven outcomes *are*. The selector returns an index `0..6`; which loot\n"
         "tier or table that indexes has not been traced. Registered as **AE-3**.",
     "~~**Not established:** what the seven outcomes *are*.~~ The selector returns an index `0..6`; ~~which loot~~\n"
     "~~tier or table that indexes has not been traced.~~ Registered as **AE-3**. *(answered: see AE-3 directly "
     "below — the seven outcomes are the loot-pickup chain bonus, not a loot tier; 2026-10-02, OPUS)*"),

    # C21: function sizes: 00317ED0 529 B (to 003180E0), 003183D0 315 B (to 0031850A).
    (LD, "`00317ED0` `EnemyChain_UpdateOnDefeat` (149 B) — the defeat-side chain",
     "`00317ED0` `EnemyChain_UpdateOnDefeat` (~~149 B~~ 529 B, `00317ED0`–`003180E0` *(corrected 2026-10-02, "
     "OPUS)*) — the defeat-side chain"),
    (LD, "`003183D0` (`EnemyChain_TryAdvanceRank`, ~29 B) — `022C315C` minus",
     "`003183D0` ~~(`EnemyChain_TryAdvanceRank`, ~29 B)~~ (`EnemyChain_TryAdvanceRank`, 315 B, "
     "`003183D0`–`0031850A` *(corrected 2026-10-02, OPUS)*) — `022C315C` minus"),

    # C22: 022C3168 is the genus being chained, not a counter (003180D0 mov [022C3168], eax from byte [rdi+0x56]).
    (LD, "counters are `dword[022C315C]` (current, capped at 999) and\n`dword[022C3168]`; the record fields",
     "counters are `dword[022C315C]` (current, capped at 999) and\n~~`dword[022C3168]`~~ `dword[022C3170]`, the "
     "count at the last rank-up; `dword[022C3168]` is not a counter but the genus being chained, −1 = none, stored "
     "from `byte [rdi+0x56]` at `003180D0` *(corrected 2026-10-02, OPUS: checked at `003180D0`; §8b)*; the record "
     "fields"),

    # C23: GR-16 answered 2026-10-01 (HX:38). HX front matter (REOPENED) is left to its owner, FABLE.
    (HX, "  ([`section03-owner-review.md`](../_index/candidates/section03-owner-review.md)) but no independent "
         "auditor\n  verdict. That is GR-16.",
     "  ([`section03-owner-review.md`](../_index/candidates/section03-owner-review.md)) ~~but no independent "
     "auditor~~\n  ~~verdict. That is GR-16.~~ *(answered: see the banner at the top — independently accepted with a "
     "narrowing 2026-10-01, SWE2-AUDIT-SEM, GR-16; 2026-10-02, OPUS)*"),

    # C24: AW's "Still PARTIAL" residual is dispositioned in 7 (GR-17 answered, rows decoded, payout read on DE).
    (AW, "**Still PARTIAL:** actual retained reward header/row bytes and lifetime, full payout/event behavior,\n"
         "and initialized-game reachability of synthetic edge states are not supplied by these observations.\n"
         "That is a real residual, not missing arithmetic placeholders.",
     "~~**Still PARTIAL:** actual retained reward header/row bytes and lifetime, full payout/event behavior,~~\n"
     "~~and initialized-game reachability of synthetic edge states are not supplied by these observations.~~\n"
     "~~That is a real residual, not missing arithmetic placeholders.~~ *(answered: see §7 — the row bytes are "
     "decoded statically, the lifetime is GR-17 (answered 2026-09-30), the payout is read statically on "
     "what-happens-when-an-enemy-dies.md; of the four synthetic edge states only GR-18's high relocation base stays "
     "open; 2026-10-02, OPUS)*"),

    # C25: GR-18 narrowed 2026-09-30: three of four edge states cannot occur with shipped data.
    (CXL, "- Shipped reachability of zero-count/missing descriptors, high relocation bases, level-zero\n"
          "  rewards, and the synthetic kind-`0xFF` roster case remains separately unproved.",
     "- ~~Shipped reachability of zero-count/missing descriptors, high relocation bases, level-zero~~\n"
     "  ~~rewards, and the synthetic kind-`0xFF` roster case remains separately unproved.~~ Shipped reachability of "
     "a high relocation base, an `.ard` buffer at or above 4 GB, remains open *(answered for the other three: see "
     "experience-and-license-point-award.md §7, GR-18 — with shipped data every unit row selects inside a present, "
     "non-empty reward table, a level below its baseline is unreachable and a `0xFF` selector is refused; "
     "2026-10-02, OPUS)*."),
    (CXL, "| whether a level-0 unit can be alive at kill time is unknown | that is what decides whether the negative "
          "path is reachable — one observation, §13 | none | UNKNOWN |",
     "| whether a level-0 unit can be alive at kill time ~~is unknown~~ *(answered: see "
     "experience-and-license-point-award.md §7, GR-18 — an enemy is grown to level 1 at init (`0023AD37`) and the "
     "only other enemy grower keeps level ≥ baseline for every shipped argument, so not with shipped data; "
     "2026-10-02, OPUS)* | that is what decides whether the negative path is reachable — one observation, §13 | "
     "~~none~~ static, shipped-data census (GR-18) | ~~UNKNOWN~~ ANSWERED (GR-18) |"),

    # C26: the 0x80000003 bits are KO, Stone and X-Zone (statuses 0, 1, 31).
    (CXL, "- Which statuses occupy bits 0, 1 and 31 of the `0x80000003` mask; the question is already open in\n"
          "  `03-World-Area-Field`.",
     "- ~~Which statuses occupy bits 0, 1 and 31 of the `0x80000003` mask; the question is already open in~~\n"
     "  ~~`03-World-Area-Field`.~~ *(answered: see what-happens-when-an-enemy-dies.md, \"What the player sees\" — "
     "KO, Stone and X-Zone, statuses 0, 1 and 31; 2026-10-02, OPUS)*"),

    # C27: the defeat body retires nothing (003125B9-003125D8: last calls 00317090 and the cookie check).
    (CDR, "inputs with NULL recipients → gil → item placement → retirement. The visible order",
     "inputs with NULL recipients → gil → item placement ~~→ retirement~~ → counter 17 (`00317090`) *(corrected "
     "2026-10-02, OPUS: the body retires nothing, §2; its last calls are `00317090` and the cookie check, "
     "`003125B9`–`003125D8`)*. The visible order"),
    (CDR, "(floor, set, report) → drop → retire.*",
     "(floor, set, report) → drop ~~→ retire~~ → counter 17 (`00317090`).* *(corrected 2026-10-02, OPUS: §2 — the "
     "body retires nothing)*"),

    # C28: C-DR's peer acceptance is recorded (C-DR:38) and S-32's five pages are contracted (C-LU:35).
    (CDR, "observation of bindings, not reward payout. Formal peer acceptance and full S-32 obligations\nremain open. "
          "A CONTRACT READY header",
     "observation of bindings, not reward payout. ~~Formal peer acceptance and full S-32 obligations~~\n~~remain "
     "open.~~ *(answered: see the banner at the top — independently accepted with a narrowing 2026-10-01, GR-16; "
     "and all five of S-32's pages now carry a contract, CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)* "
     "A CONTRACT READY header"),

    # C29: the "uncontracted" siblings all carry contracts now (C-LU:35).
    (CLC, "**This takes the loot rolls and the chain**; the death sequence,\n> the gil paths and the level-up remain "
          "uncontracted and this document does not claim them.",
     "**This takes the loot rolls and the chain**; the death sequence,\n> the gil paths and the level-up ~~remain "
     "uncontracted~~ have since been contracted *(answered: see CONTRACT-defeat-rewards-sequence.md, "
     "CONTRACT-gil-storage-and-movement.md and CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)*, and this "
     "document does not claim them."),
    (CLC, "| **Uncontracted** | the death sequence, the gil paths and the level-up — S-32's other three pages, not "
          "claimed here |",
     "| ~~**Uncontracted**~~ **Contracted separately** | the death sequence, the gil paths and the level-up — S-32's "
     "other three pages, not claimed here *(answered: each has its own contract — "
     "CONTRACT-defeat-rewards-sequence.md, CONTRACT-gil-storage-and-movement.md, "
     "CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)* |"),
    (CLC, "- The three uncontracted pages of S-32.",
     "- ~~The three uncontracted pages of S-32.~~ *(answered: all three are contracted — "
     "CONTRACT-defeat-rewards-sequence.md, CONTRACT-gil-storage-and-movement.md, "
     "CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)*"),
    (CGL, "**this takes the gil paths.** The death\n> sequence and the level-up remain uncontracted and this document "
          "does not claim them.",
     "**this takes the gil paths.** The death\n> sequence and the level-up ~~remain uncontracted~~ have since been "
     "contracted *(answered: see CONTRACT-defeat-rewards-sequence.md and CONTRACT-level-advance-and-growth.md; "
     "2026-10-02, OPUS)*, and this document does not claim them."),
    (CGL, "| **Uncontracted** | the death sequence and the level-up — S-32's other two pages, not claimed here |",
     "| ~~**Uncontracted**~~ **Contracted separately** | the death sequence and the level-up — S-32's other two "
     "pages, not claimed here *(answered: CONTRACT-defeat-rewards-sequence.md, CONTRACT-level-advance-and-growth.md; "
     "2026-10-02, OPUS)* |"),
    (CDR, "The level-up page remains uncontracted and this document does not claim it.",
     "The level-up page ~~remains uncontracted~~ has since been contracted *(answered: see "
     "CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)*, and this document does not claim it."),
    (CDR, "| **Uncontracted** | the level-up page — S-32's last, not claimed here |",
     "| ~~**Uncontracted**~~ **Contracted separately** | the level-up page — S-32's last, not claimed here "
     "*(answered: CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)* |"),

    # C30: GR-19 is ANSWERED (DE:4, DE:230, register); the residual belongs to the shared placement test.
    (DE, "that DE-4 names; open is what that test accepts.)*",
     "that DE-4 names; ~~open is what that test accepts.~~)* *(answered: GR-19's question is answered — the gate "
     "asks whether the party leader could stand at the death position, see the drop-gate answer above, \"Answered "
     "2026-09-30\"; what the shared test accepts in full is a residual of the placement test, not of GR-19; "
     "2026-10-02, OPUS)*"),

    # C31: levelling precedes gil (0031244A-003124A3 before 0031251D).
    (DE, "**and it is where experience, LP, gil, levelling and the item drop all\nhappen, in that order, in one "
         "function.**",
     "**and it is where experience, LP, ~~gil, levelling~~ levelling, gil and the item drop all\nhappen, in that "
     "order, in one function.** *(corrected 2026-10-02, OPUS: the level walk and advance, `0031244A`–`003124A3`, "
     "run inside the per-recipient step, before gil at `0031251D`; steps 2 and 4 below)*"),

    # C32: what 00316A50 does with kinds 6 / 7 is in C-GL (GL-2 saturating dwords; 14: counter ids 8 / 0xA).
    (GL, "— **`cl`, settled §13.** Still open: **what `00316A50`",
     "— **`cl`, settled §13.** ~~Still open:~~ *(answered: see CONTRACT-gil-storage-and-movement.md GL-2 and §14 — "
     "kind 6 adds to the saturating gained dword `[020927C0] + 0x3860`, kind 7 to the spent dword `+0x3864`, and "
     "they feed counter ids 8 / `0xA`; 2026-10-02, OPUS)* **what `00316A50`"),
    (GL, "**Not claimed.** What `00316A50` does with kinds 6 and 7 — only its argument handling and its table's\n"
         "shape were read. How the award amount is computed, what determines",
     "**Not claimed.** ~~What `00316A50` does with kinds 6 and 7 — only its argument handling and its table's~~\n"
     "~~shape were read. How the award amount is computed,~~ *(answered: the kinds 6 / 7 meter — "
     "CONTRACT-gil-storage-and-movement.md GL-2 and §14; the award amount — CONTRACT-defeat-rewards-sequence.md "
     "DR-4; 2026-10-02, OPUS)* Still not claimed: what determines"),

    # C33: the gil award is computed in C-DR DR-4 and DE ("Gil comes from the same two tables").
    (GL, "- **How the award amount is computed** — `BattleUnit_ProcessDefeatRewardsAndLoot` is named as the\n"
         "  award caller but its computation is not read here. It is the natural next step and belongs beside\n"
         "  [`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md).",
     "- ~~**How the award amount is computed** — `BattleUnit_ProcessDefeatRewardsAndLoot` is named as the~~\n"
     "  ~~award caller but its computation is not read here. It is the natural next step and belongs beside~~\n"
     "  ~~[`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md).~~ *(answered: see "
     "CONTRACT-defeat-rewards-sequence.md DR-4 and what-happens-when-an-enemy-dies.md — gil = (defeated level − "
     "baseline) × `[+0xE78] + 0x30` + `[+0xE70] + 0x30`, plus the effect-12 conversion, `0031251D`–`00312546`; "
     "2026-10-02, OPUS)*"),

    # C34: 22 getter bodies, 19 direct + 3 through the thunk 00309BF0 (GL 4, C-GL GL-5).
    (GL, "disjoint from all 21 bodies calling `GameState_GetGil` or its thunk.",
     "disjoint from all ~~21~~ 22 bodies calling `GameState_GetGil` or its thunk *(corrected 2026-10-02, OPUS: 19 "
     "direct and 3 through `00309BF0`, §4's census and CONTRACT-gil-storage-and-movement.md GL-5)*."),
    (CGL, "`00316440`, `00316A63`, `0034C9A0`, `00352250`) are disjoint from all 21 bodies calling",
     "`00316440`, `00316A63`, `0034C9A0`, `00352250`) are disjoint from all ~~21~~ 22 *(corrected 2026-10-02, OPUS: "
     "19 + 3, GL-5)* bodies calling"),
    (CGL, "disjoint from the 21 `GetGil`/thunk bodies |",
     "disjoint from the ~~21~~ 22 *(corrected 2026-10-02, OPUS: 19 + 3, GL-5)* `GetGil`/thunk bodies |"),

    # C35: 008626C0 is a float body, not among 00254EE0's thirteen callers (checked at 008626C0).
    (GL, "`008626C0` (529 B) is a gil move/clamp body -",
     "`008626C0` (529 B) is ~~a gil move/clamp body~~ the 529-byte pool helper of the binder subtree, not a gil "
     "path: an SSE float body that is not among `00254EE0`'s thirteen callers *(corrected 2026-10-02, OPUS: checked "
     "at `008626C0`; §4's census)* -"),

    # C36: the UI helpers move and read no gil (GL:441).
    (GL, "position-watch flag the gil paths maintain.",
     "position-watch flag ~~the gil paths maintain~~ of the UI binder, which moves and reads no gil *(corrected "
     "2026-10-02, OPUS: the UI crossing paragraph above)*."),
    (GL, "the code-to-word translate the gil paths share.",
     "the code-to-word translate ~~the gil paths share~~ of the UI menus, which no gil path reads *(corrected "
     "2026-10-02, OPUS: the UI crossing paragraph above)*."),

    # C37: six growth calls per level (LU 4 table, LU 9, C-LU).
    (LU, "Each iteration applies four growth calls, each taking a **growth byte from the character's own growth",
     "Each iteration applies ~~four growth calls, each taking~~ six growth calls *(corrected 2026-10-02, OPUS: the "
     "table below has six rows, as §9 and CONTRACT-level-advance-and-growth.md say)*; the four float calls each "
     "take a **growth byte from the character's own growth"),

    # C38: LU's "not claimed" list is answered in 8 and the 0035D8C0 subtree; only 00329210 stays unread.
    (LU, "**Not claimed.** What `0035D8C0`, `0046A690`, `003B02A0`, `00329210` or bank 7 do — **their bodies\n"
         "were not read beyond their argument shapes.** Which stats the six fields are. Nothing was executed.",
     "**Not claimed.** What ~~`0035D8C0`, `0046A690`, `003B02A0`,~~ `00329210` ~~or bank 7~~ do — **their bodies\n"
     "were not read beyond their argument shapes.** ~~Which stats the six fields are.~~ Nothing was executed. "
     "*(answered: see §8 — `0046A690` posts the level-up message, event 4, and there is no bank 7, only slot 7 of "
     "the live bank (UQ-135); `003B02A0` spawns presentation `0x71` (narrowed 2026-09-25); the six fields are HP, "
     "MP, Strength, Magick Power, Vitality and Speed (UQ-134); `0035D8C0` is the `002905D0` manager dispatch (\"The "
     "`0035D8C0` exclusive subtree\"); 2026-10-02, OPUS)*"),

    # C39: 002FB150 was read 2026-09-11; both selectors have one static caller (00310DB0; 00312730 at 003129AF).
    (WL, "(`002FB150`),\nstill unread (`CM-5`).",
     "(`002FB150`),\n~~still unread (`CM-5`).~~ *(answered: read 2026-09-11, the next subsection; `CM-5` ANSWERED in "
     "§5; 2026-10-02, OPUS)*"),
    (WL, "questions, and neither has a caller in the function graph (`CM-5`'s residue).",
     "questions, and ~~neither has a caller in the function graph (`CM-5`'s residue)~~ each has one static caller "
     "the function graph missed: `00310DB0` runs the overlap test (`003110DC`–`00311141`, \"Who runs the collector\" "
     "below) and `00312730` calls the nearest selector at `003129AF` *(corrected 2026-10-02, OPUS: §5's `CM-5` "
     "answer, corrected 2026-09-23)*."),

    # C40: 438 reads + one writer instruction each = the table's 441 references (001EDDF2, 001EDDD8, 001EDDE0).
    (WL, "scalar**, one of a triple read **438 times** across the image (`01DFE0B4` 211, `01DFE0B8` 45,",
     "scalar**, one of a triple read **438 times** *(reconciled 2026-10-02, OPUS: reads only; the table under "
     "\"What the page did not have\" counts 441 references, the same reads plus one writer instruction each, "
     "`001EDDF2` / `001EDDD8` / `001EDDE0`)* across the image (`01DFE0B4` 211, `01DFE0B8` 45,"),

    # C41: UQ-137 is closed (register row SUPERSEDED 2026-09-26; WL's box ticked).
    (CWL, "4 GB — is a live\nquestion and remains open.",
     "4 GB — ~~is a live~~\n~~question and remains open.~~ is closed *(answered: see the register row UQ-137, "
     "SUPERSEDED 2026-09-26 under the runtime rule — the requirement chain is static and replayed (EXP-141) — and "
     "the pool page's ticked §5 box; 2026-10-02, OPUS)*."),
    (CWL, "behaviour. `UQ-137` is untouched by it.",
     "behaviour. ~~`UQ-137` is untouched by it.~~ *(answered: `UQ-137` is closed, SUPERSEDED 2026-09-26 — see §13; "
     "2026-10-02, OPUS)*"),
    (CWL, "* **`UQ-137`** **[live]**.",
     "* ~~**`UQ-137`** **[live]**.~~ *(answered: `UQ-137` is closed, SUPERSEDED 2026-09-26 — see §13; 2026-10-02, "
     "OPUS)*"),

    # C42: README labels against the pages' own front matter, and the twelve pages it omitted.
    (R, "  **PARTIAL, tier 1.** Every loot roll",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. Every loot roll"),
    (R, "nothing, not less. EXP is divided by a live count of eligible recipients.\n\n## How to add a system here",
     "nothing, not less. EXP is divided by a live count of eligible recipients.\n"
     "- [`how-experience-is-computed-and-divided.md`](how-experience-is-computed-and-divided.md) - function note of "
     "the award page: the EXP computer and its divisor - **REOPENED** (SECTION-03 accepted 2026-10-01; the "
     "re-status is left to its owner)\n"
     "- [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) - the EXP and LP "
     "computers - **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`what-happens-when-an-enemy-dies.md`](what-happens-when-an-enemy-dies.md) - the defeat sequence "
     "`00312280` - **DOCUMENTED**\n"
     "- [`CONTRACT-defeat-rewards-sequence.md`](CONTRACT-defeat-rewards-sequence.md) - **CONTRACT READY**\n"
     "- [`what-happens-when-a-character-levels-up.md`](what-happens-when-a-character-levels-up.md) - the level "
     "advance `0030C650` - **AUDITED**\n"
     "- [`CONTRACT-level-advance-and-growth.md`](CONTRACT-level-advance-and-growth.md) - **CONTRACT READY**\n"
     "- [`gil-storage-clamp-and-every-path-that-moves-it.md`](gil-storage-clamp-and-every-path-that-moves-it.md) - "
     "the gil setter and its thirteen writers - **AUDITED**\n"
     "- [`CONTRACT-gil-storage-and-movement.md`](CONTRACT-gil-storage-and-movement.md) - **CONTRACT READY**\n"
     "- [`the-chain-and-its-sticky-coin.md`](the-chain-and-its-sticky-coin.md) - the chain update and its sticky "
     "coin - **AUDITED**\n"
     "- [`CONTRACT-loot-rolls-and-the-chain.md`](CONTRACT-loot-rolls-and-the-chain.md) - **CONTRACT READY**\n"
     "- [`world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`](world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) "
     "- the ten-slot pickup pool - **AUDITED**\n"
     "- [`CONTRACT-world-loot-pickup-pool.md`](CONTRACT-world-loot-pickup-pool.md) - **BEHAVIORALLY UNDERSTOOD**\n"
     "- *(twelve pages added to this list 2026-10-02, OPUS, each with the status its own front matter states)*\n"
     "\n## How to add a system here"),

    # C43: the heading counts three counters (the table's third row is the break counter).
    (CH, "## Two counters, not one",
     "## ~~Two~~ Three counters, not one (count corrected 2026-10-02, OPUS: the table has three rows; the third is "
     "the break counter)"),

    # F1 (2.5): the rank advance runs inside the chain update, before the coin, on a continued chain only
    # (00317F27 jne 0031806C to the break path; 00317FBC call 003183D0; coin draw 00317FC1-0031800C; store 003180C6).
    (LD, "  -> EnemyChain_TryAdvanceRank (003183D0)\n       -> authored threshold",
     "  -> EnemyChain_TryAdvanceRank (003183D0)   <- corrected 2026-10-02, OPUS: not a separate step; "
     "EnemyChain_UpdateOnDefeat calls it at 00317FBC, on the same-genus path only, before the coin draw "
     "(00317FC1-0031800C) and coin store (003180C6); the break path (00317F27 jne 0031806C) never calls it\n"
     "       -> authored threshold"),
    (LD, "to start and a 60 % chance per kill to keep; while it holds, the rank advance skips the",
     "to start and a 60 % chance per kill to keep; ~~while it holds~~ while the bit stored by the previous "
     "continued kill holds — the rank advance runs at `00317FBC`, before this kill's coin draw "
     "(`00317FC1`–`0031800C`) and store (`003180C6`), so its roll also precedes the coin's in the LCG stream "
     "*(corrected 2026-10-02, OPUS: checked at `00317ED0`)* — the rank advance skips the"),
    (CLC, "Per kill: *chain update → rank advance → profile (rank, or drawn)",
     "Per kill: *~~chain update → rank advance~~ chain update, which calls the rank advance itself (`00317FBC`) on a "
     "continued chain only, before the coin draw (`00317FC1`–`0031800C`) and the coin store (`003180C6`), while a "
     "break (`00317F27 jne 0031806C`) never calls it (corrected 2026-10-02, OPUS) → profile (rank, or drawn)"),
    (CLC, "| chain on a kill | `EnemyChain_UpdateOnDefeat` (`00317ED0`) → `EnemyChain_TryAdvanceRank` (`003183D0`) "
          "| 1 each |",
     "| chain on a kill | `EnemyChain_UpdateOnDefeat` (`00317ED0`) ~~→ `EnemyChain_TryAdvanceRank` (`003183D0`)~~, "
     "which itself calls `EnemyChain_TryAdvanceRank` (`003183D0`) at `00317FBC` on a continued chain only, before "
     "its coin draw *(corrected 2026-10-02, OPUS: checked at `00317ED0`; a break, `00317F27 jne 0031806C`, never "
     "calls it)* | 1 each |"),

    # F2 (2.5): AE-13's tier is 0, not n, when the walk admits all n rows (003181E0-003181EF).
    (LD, "negative byte or a counter ≤ the byte stops the walk; `ebp = min(rows admitted, n)`), so the",
     "negative byte or a counter ≤ the byte stops the walk; ~~`ebp = min(rows admitted, n)`~~ `ebp` = the rows "
     "admitted when the walk stops early, but **0** when it admits all `n` rows — `mov ebp, r14d` (0), then "
     "`cmovl ebp, edi` *(corrected 2026-10-02, OPUS: checked at `003181E0`–`003181EF`; unreachable with the shipped "
     "table, whose row 3 byte −1 stops the walk, but a port that edits that byte would see it)*), so the"),
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
