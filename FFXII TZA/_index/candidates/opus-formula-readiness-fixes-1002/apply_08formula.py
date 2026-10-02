"""apply_08formula.py [--apply] - 08-Combat-Formula readiness map (readiness-08-formula.md), section 2.4
contradictions 1-56 and the two section 2.5 findings no other item carries, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the map's dated correction, the bytes or the shipped tables
refute) and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike; their OLD runs into the next line so NEW
never contains OLD. No heading changes.
Item 50's favoured side is a 12-Items page; only the disfavoured 08 page is edited. Item 37 restates the HP page's own
census without a new number. Item 20 corrects only the class range (the "246 of 279" figure is left as it is).
The structural gaps (section 2.2) are left for later, as briefed.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "08-Combat-Formula/"
R = F + "README.md"
NS = F + "Status-And-Augment-Namespaces/README.md"
EA = F + "elemental-affinity-and-the-five-bytes.md"
CST = F + "CONTRACT-formula-step-table.md"
CWE = F + "CONTRACT-environmental-element-scaling.md"
CB = F + "combos-and-the-guard-parry-flag.md"
CRW = F + "CONTRACT-weapon-recipes.md"
EC = F + "Evaluation-Context/the-evaluation-context-field-map.md"
WX = F + "Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md"
CSD = F + "CONTRACT-stat-derivation.md"
AS = F + "the-auto-status-rebuild.md"
SL = F + "Steal/the-steal-roll.md"
RW = F + "Recipe-System/ranged-weapon-recipes.md"
CC = F + "Recipe-System/the-count-clock-and-bank-recipes.md"
SB = F + "Scratch-Block/the-formula-scratch-block.md"
WS = F + "where-a-stat-number-comes-from.md"
CPF = F + "CONTRACT-preparation-step-family.md"
HP = F + "Current-HP/the-hp-write-and-the-lethal-transition.md"
CHP = F + "CONTRACT-hp-write-and-lethal-transition.md"
STP = F + "Step-Table/combat-formula-step-table.md"
FM = F + "Battle-Stats-Record/the-battle-stats-record-field-map.md"
AD = F + "Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md"

EDITS = [
    # C1: the foe max-HP cap is 1,000,000,000 (002FF7BB-002FF7C8 mov eax, 0x3b9aca00 / cmove).
    (FM, "cap **9,999** for party records, **999,999,999** for the rest (`002FF7B1`–`002FF7E2`)",
     "cap **9,999** for party records, ~~**999,999,999**~~ **1,000,000,000** for the rest *(corrected 2026-10-02, "
     "OPUS: checked at `002FF7BB`–`002FF7C8`, `mov eax, 0x3b9aca00` / `cmove eax, r8d`; CONTRACT-stat-derivation.md "
     "D-3)* (`002FF7B1`–`002FF7E2`)"),

    # C2: +0x08 on the party path is base HP, scaled by the party row (002FF078-002FF07B, 002F8E50-002F8E6D).
    (CSD, "| shape | `float` fields converted to `int`, plus the level at `+0x08` |",
     "| shape | `float` fields converted to `int`, plus ~~the level at `+0x08`~~ the base HP at `+0x08`, scaled by the "
     "party row: `(row[+0x18] + 1) × stats[+0x08] × row[+0x19] / 100` *(corrected 2026-10-02, OPUS: checked at "
     "`002FF078`–`002FF07B` `mov ecx, [rdi+8]` / `call 002F8E50` and `002F8E50`–`002F8E6D`; "
     "where-a-stat-number-comes-from.md, corrected 2026-09-30)* |"),

    # C3: the 0x7FFF re-store is gated on [rsp+0x5C] (002FF003-002FF021): party Esper rows only, not the .ard column.
    (WS, "| `+0x20` | `int` | **HP** | `0x7FFF` |",
     "| `+0x20` | `int` | **HP** | ~~`0x7FFF`~~ 1,000,000,000 *(corrected 2026-10-02, OPUS: the `0x7FFF` re-store "
     "`002FF7E5`–`002FF805` is gated on `[rsp+0x5C]`, set at `002FF003`–`002FF021` only when `+0x05 == 0` and the type "
     "is `0x1B`–`0x27`, the thirteen party Esper rows; a foe's HP takes the 1,000,000,000 cap; "
     "CONTRACT-stat-derivation.md §14)* |"),

    # C4: +0x31-+0x33 are read as the outcome bands (00388FB0-00388FC8, 00389093-003890AB).
    (FM, "  `+0x31`–`+0x36` have **no reader** the enumeration reaches: six output bytes the rebuild computes\n"
         "  that nothing on a battle unit consumes.",
     "  ~~`+0x31`–`+0x36` have **no reader** the enumeration reaches: six output bytes the rebuild computes~~\n"
     "  ~~that nothing on a battle unit consumes.~~ `+0x31`–`+0x33` are read by every outcome roll: the threshold "
     "loaders `00388FB0` and `00389040` load target `+0x33`, `+0x32` and `+0x31` into the bands `02AEDFF0`, "
     "`02AEDFF4` and `02AEDFEC` *(corrected 2026-10-02, OPUS: checked at `00388FB0`–`00388FC8` and "
     "`00389093`–`003890AB`; this page's own rows for `+0x31`–`+0x33` and the-formula-scratch-block.md §2.2)*."),
    (FM, "  +0x2A..+0x30 u8  Str Mag Vit Spd Atk Def MRes      +0x31..+0x36 rebuild outputs (unread)   +0x37 u8 MP bars\n"
         "  +0x38 +0x3C +0x64 u32 status words",
     "  +0x2A..+0x30 u8  Str Mag Vit Spd Atk Def MRes      +0x31..+0x36 rebuild outputs (unread)   +0x37 u8 MP bars"
     "   <- corrected 2026-10-02, OPUS: +0x31..+0x33 are read as the outcome bands (00388FB0-00388FC8, "
     "00389093-003890AB)\n"
     "  +0x38 +0x3C +0x64 u32 status words"),
    (FM, "- **`+0x31`–`+0x36` are free to repurpose on the unit side** — nothing enumerated reads them — but\n"
         "  the rebuild rewrites them, so a mod must write after it or hook it.",
     "- ~~**`+0x31`–`+0x36` are free to repurpose on the unit side** — nothing enumerated reads them — but~~\n"
     "  ~~the rebuild rewrites them, so a mod must write after it or hook it.~~ **`+0x31`–`+0x33` are not free to "
     "repurpose**: every outcome roll reads them as its evade bands, so a port that reuses them breaks every hit roll; "
     "the rebuild rewrites all six, so a mod must write after it or hook it *(corrected 2026-10-02, OPUS: checked at "
     "`00388FB0`–`00388FC8` and `00389093`–`003890AB`)*."),
    (FM, "That nothing\n    enumerated reads them is a separate fact, and it stands.",
     "~~That nothing~~\n    ~~enumerated reads them is a separate fact, and it stands.~~ The three bands are read: "
     "`00388FB0` and `00389040` load `+0x33` / `+0x32` / `+0x31` into `02AEDFF0` / `02AEDFF4` / `02AEDFEC` "
     "*(corrected 2026-10-02, OPUS: checked at `00388FB0`–`00388FC8` and `00389093`–`003890AB`)*."),

    # C5: with layer bit 7 (id 39) set, MP and +0x06 are clamped to 0 (0031050B-00310566, r14d = 0 at 0030FF07).
    (AS, "- Two further caps (`+0x4C` and `+0x06`) are applied **only when both status layers have bit 7 clear**\n"
         "  (`+0x6C` and `+0x7C` non-negative) — **a single status that suspends two independent clamps.**",
     "- Two further caps (`+0x4C` and `+0x06`) ~~are applied **only when both status layers have bit 7 clear**~~\n"
     "  ~~(`+0x6C` and `+0x7C` non-negative) — **a single status that suspends two independent clamps.**~~ take their "
     "normal cap only when both status layers have bit 7 clear (`+0x6C` and `+0x7C` non-negative); with bit 7 (id 39) "
     "set on either, the cap is **0**, so MP and the secondary pool are clamped to 0, not left unclamped "
     "*(corrected 2026-10-02, OPUS: checked at `0031050B`–`00310566`, `js` / `jl` selecting `r14d`, zeroed at "
     "`0030FF07`; the formula below, `cap = (+0x6C ≥ 0 && +0x7C ≥ 0) ? +0x28 : 0`)*."),

    # C6: the scratch triple is f32 (0038A15B-0038A163 addss / movss; 0038BE0A-0038BE1A). Code block: comment.
    (CST, "02AEE05C  u32  /\n```",
     "02AEE05C  u32  /   <- corrected 2026-10-02, OPUS: all three words are f32, not u32 (0038A15B-0038A163 addss / "
     "movss [02AEE054]; 0038BE0A-0038BE1A mulss)\n```"),

    # C7: recipes 20-29 are not one template (01EF9C80-01EF9FB0 decoded; RW-4, E-4).
    (CPF, "- **Recipes 20–29 differ only in this slot** — identical preview lists, and resolution lists identical\n"
          "  but for the preparation entry: 20→65,",
     "- ~~**Recipes 20–29 differ only in this slot** — identical preview lists, and resolution lists identical~~\n"
     "  ~~but for the preparation entry:~~ **Recipes 20–29 each name one slot of this family, but differ in more "
     "than it** *(corrected 2026-10-02, OPUS: decoded at `01EF9C80`–`01EF9FB0` — 20–24 and 28 share the first list "
     "`[5, 6, 7, 8, 9, 10, 22, 33, 34, 41]` and open the second with 28, but 23 finalises with 126; the bows 25 / 26 / "
     "27 have their own first lists and open the second with 29; recipe 29 stops at 165; CONTRACT-weapon-recipes.md "
     "RW-4, ranged-weapon-recipes.md E-4)*. The entries are 20→65,"),
    (CPF, "| recipes 20-29 differ only in this slot | identical preview lists and resolution lists differing only in "
          "the preparation entry, 20→65 … 29→72 |",
     "| ~~recipes 20-29 differ only in this slot~~ recipes 20-29 each name one slot of this family *(corrected "
     "2026-10-02, OPUS: they differ elsewhere too, decoded at `01EF9C80`–`01EF9FB0`; §6)* | ~~identical preview lists "
     "and resolution lists differing only in the preparation entry,~~ 20→65 … 29→72 |"),

    # C8: the bows' second lists open with 29, not the no-op 28 (01EF9C80-01EF9FB0; C-RW RW-2).
    (AD, "Every list opens with slot 28 (a no-op, AK-5). So **the modifier chain",
     "~~Every list opens with slot 28 (a no-op, AK-5).~~ The melee lists open with slot 28 (a no-op, AK-5); the bows' "
     "lists, recipes 25–27, open with slot **29**, the reaction roll that sets the flag slot 98 doubles on "
     "*(corrected 2026-10-02, OPUS: decoded at `01EF9C80`–`01EF9FB0`; CONTRACT-weapon-recipes.md RW-2 decodes recipe "
     "25 as `… | -1 | 29 66 96 …`)*. So **the modifier chain"),
    (AD, "25 / 26 / 27 (bows)  66 / 65 / 70                      96 97 98 99        125            165 171 176 182\n"
         "28       71",
     "25 / 26 / 27 (bows)  66 / 65 / 70                      96 97 98 99        125            165 171 176 182"
     "   <- corrected 2026-10-02, OPUS: the bows open their second list with 29, not 28 (01EF9C80-01EF9FB0)\n"
     "28       71"),

    # C9: slot 43 rolls bands A and B, then the hit (0038999E, 003899E7; no 02AEDFEC read).
    (STP, "| `00389950` | 43 | banded outcome roll — `RNG % hit` against the `02AEDFF0` band, writes",
     "| `00389950` | 43 | banded outcome roll — ~~`RNG % hit` against the `02AEDFF0` band~~ bands A (`02AEDFF0`) "
     "and B (`02AEDFF4`), then the hit roll; no band C, no parry *(corrected 2026-10-02, OPUS: checked at `0038999E` "
     "`cmp edx, [02AEDFF0]` and `003899E7` `cmp edi, [02AEDFF4]`, no `02AEDFEC` read; ranged-weapon-recipes.md "
     "E-4)*, writes"),

    # C10 + section 2.5 finding 1: slot 98 doubles (01CEBC08 = 2.0) on result +0x18 bit 0, which slot 29 sets.
    (STP, "| `0038BE00` | 98 | multiplier `×1.7` (`01CEBC08`) when the context sub-record `+0x18` bit 0 is set |",
     "| `0038BE00` | 98 | multiplier ~~`×1.7`~~ `×2.0` (`01CEBC08`) when ~~the context sub-record `+0x18` bit 0~~ "
     "the result record's `+0x18` bit 0 (through context `+0x10`) is set — the bit slot 29 `00389140` sets at "
     "`003891D9` *(corrected 2026-10-02, OPUS: checked at `0038BE00`–`0038BE12`, `mov rax, [r8+0x10]` / "
     "`test byte [rax+0x18], 1` / `mulss xmm0, [01CEBC08]`, and `01CEBC08` = 2.0; the-formula-scratch-block.md "
     "§2.4)* |"),
    (AD, "The constant is a literal `2.0` in `.rdata`. One flag bit doubles the damage multiplier.",
     "The constant is a literal `2.0` in `.rdata`. One flag bit — result `+0x18` bit 0, set by slot 29's reaction roll "
     "`00389140` at `003891D9`, the slot the bows' second lists open with — doubles the damage multiplier "
     "*(corrected 2026-10-02, OPUS: checked at `0038BE00`–`0038BE08` and `003891D9`; the-formula-scratch-block.md "
     "§2.4)*."),

    # C11: the Vitality variant is 2 x (L + VIT) x STR / 256, no +1 (0038A2D6-0038A31F).
    (AD, "      the multiplier is `(L + VIT) × VIT / 256` with no unity term, so at low level and Vitality it is\n"
         "      **below 1** — `(L + VIT) × VIT < 256`, e.g. level 5 with Vitality 20 gives `0.98`, level 1\n"
         "      with Vitality 10 gives `0.43` — and the weapon deals *less* than `attack − defence` until the\n"
         "      product passes 256;",
     "      the multiplier is ~~`(L + VIT) × VIT / 256`~~ `2 × (L + VIT) × STR / 256` with no unity term *(corrected "
     "2026-10-02, OPUS: checked at `0038A2D6`–`0038A31F` — `(L + [+0x2C]) × [+0x2A]`, `mulss` by 1/256, "
     "`addss xmm0, xmm0`, no `+1`; CONTRACT-preparation-step-family.md §7)*, ~~so at low level and Vitality it is~~\n"
     "      ~~**below 1** — `(L + VIT) × VIT < 256`, e.g. level 5 with Vitality 20 gives `0.98`, level 1~~\n"
     "      ~~with Vitality 10 gives `0.43` — and the weapon deals *less* than `attack − defence` until the~~\n"
     "      ~~product passes 256;~~ so it is below 1 only while `(L + VIT) × STR < 128` — level 5 with Vitality 20 and "
     "Strength 20 gives 3.9;"),
    (AD, "                                                      /* no +1 for the Vitality variant */\n"
         "                                                      /* x1.5",
     "                                                      /* no +1 for the Vitality variant */"
     "   <- corrected 2026-10-02, OPUS: and it is 2 x (L + VIT) x STR / 256 (0038A2D6-0038A31F)\n"
     "                                                      /* x1.5"),

    # C12: the Speed variant's second factor is Strength (0038A116-0038A15B).
    (AD, "family (daggers, ninja swords, bows) the multiplier `1 + (L + SPD) × SPD / 218` is",
     "family (daggers, ninja swords, bows) the multiplier ~~`1 + (L + SPD) × SPD / 218`~~ `1 + (L + SPD) × STR / 218` "
     "*(corrected 2026-10-02, OPUS: checked at `0038A116`–`0038A15B` — `movzx [rcx+0x2d]` plus the level, `imul` by "
     "`[rcx+0x2a]`, Strength, `divss` 218, `addss` 1; ranged-weapon-recipes.md §4)* is"),

    # C13: Lure (17) is read by the steal's three-roll branch (00384827 merge, 003904A5 test).
    (NS, "| 17 | Lure | Thievery | no formula role established |",
     "| 17 | Lure | Thievery | ~~no formula role established~~ the steal's three-roll branch: the merge carries the "
     "status layer, so a Lured source steals like one wearing Thief's Cuffs *(corrected 2026-10-02, OPUS: checked at "
     "`00384827`, the merge tests `[stats + 0x68 + (id>>3)]`, and `003904A5` `test byte ptr [rsi + 0x1c], 2`; "
     "the-evaluation-context-field-map.md §2.3)* |"),
    (NS, "**Lure** (17) has no formula reader\n  and its alias is inert.",
     "~~**Lure** (17) has no formula reader~~\n  ~~and its alias is inert.~~ **Lure** (17) is read by the steal's "
     "three-roll branch (`003904A5`), so a Lured source steals with three independent rolls *(corrected 2026-10-02, "
     "OPUS: checked at `00384827` and `003904A5`)*."),

    # C14: an environment rule and a terrain rule on one element share one multiply (0038B3E1-0038B424).
    (WX, "Three independent inputs, applied in sequence and multiplied together:",
     "Three ~~independent~~ inputs, applied in sequence ~~and multiplied together~~ — but not as independent factors: "
     "Lightning, Ice, Earth and Water each take one ×1.2 when the environment class **or** the terrain class matches, "
     "so Lightning in rain on water terrain is ×1.2, not ×1.44; only rules on different elements, or a ×0.5 against a "
     "×1.2, compose *(corrected 2026-10-02, OPUS: checked at `0038B3E1`–`0038B424`, one `mulss` for either test, and "
     "the same shape at `0038B46D`, `0038B4F3` and `0038B579`; CONTRACT-environmental-element-scaling.md, the "
     "2026-09-25 rule table)*:"),
    (CWE, "**WE-2 — Three independent inputs, multiplied in sequence.** Global environment class, MWeather",
     "**WE-2 — Three ~~independent~~ inputs, ~~multiplied in sequence~~ tested in sequence** *(corrected 2026-10-02, "
     "OPUS: an environment rule and a terrain rule for the same element share one multiply, `0038B3E1`–`0038B424`; "
     "the rule table below)*. Global environment class, MWeather"),

    # C15: the first list runs at execution (00385680 <- 00303830@00303910, 00303A00@00303AD7;
    #      00303830 <- 00304850@00304F1D, 00313120@003132A6); 003858E7 is inside 00385680.
    (CRW, "**The first list\nis preview-side and the second is the committed result**, and the committed path",
     "~~**The first list~~\n~~is preview-side and the second is the committed result**~~ **The first list is the "
     "outcome decision, run when the action executes and memoised into the result, and the second is the committed "
     "result** *(corrected 2026-10-02, OPUS: §14's correction; ranged-weapon-recipes.md §2)*, and the committed path"),
    (CRW, "a second recipe walker — and it is statically orphaned.** The recipe",
     "a second recipe walker~~ — and it is statically orphaned~~.** *(corrected 2026-10-02, OPUS: `0x3858E7` lies "
     "inside `00385680`, reached by `jne` / `je` at `00385893` / `003858A0`, and `00385680` has two callers; see "
     "below)* The recipe"),
    (CRW, "**The residual:** `0x3858E7` itself is statically orphaned — zero",
     "**The residual:** `0x3858E7` ~~itself is statically orphaned~~ is an interior label of "
     "`BattleFormula_EvaluateTargetPreview` `00385680`, reached by `jne` / `je` at `00385893` / `003858A0`, which is "
     "why it has *(corrected 2026-10-02, OPUS: checked at those addresses)* — zero"),
    (CRW, "Who *invokes* the preview walker is a runtime-registration question,\n  not answerable from the image.",
     "~~Who *invokes* the preview walker is a runtime-registration question,~~\n  ~~not answerable from the image.~~ "
     "The image answers who invokes it: `00385680` is called by `BattleAction_EvaluateTargetPreviews` `00303830` "
     "(`00303910`) and by `00303A00` (`00303AD7`), and `00303830` by `BattleUnit_AdvanceStandardActionState` "
     "`00304850` (`00304F1D`) and by `00313120` (`003132A6`) — the first list runs when the action executes, as its "
     "hit / evade / knockback / combo decision *(corrected 2026-10-02, OPUS: checked by `retool.py callers`; "
     "ranged-weapon-recipes.md §2, corrected 2026-09-30)*."),

    # C16: 02AEDFF8, 02AEDFFC and 02AEE050 reset to -1 (00384A59, 00384A63, 00384AF9).
    (SB, "| `02AEDFF8` | 0 | 7 / 1 |",
     "| `02AEDFF8` | ~~0~~ `-1` *(corrected 2026-10-02, OPUS: `00384A59` stores `0xFFFFFFFF`)* | 7 / 1 |"),
    (SB, "| `02AEDFFC` | 0 | 7 / 1 |",
     "| `02AEDFFC` | ~~0~~ `-1` *(corrected 2026-10-02, OPUS: `00384A63` stores `0xFFFFFFFF`)* | 7 / 1 |"),
    (SB, "| `02AEE050` | 0 | 8 / 2 |",
     "| `02AEE050` | ~~0~~ `-1` *(corrected 2026-10-02, OPUS: `00384AF9` stores `0xFFFFFFFF`; a port that "
     "initialises 0 hands out item 0 when no poach step ran)* | 8 / 2 |"),
    (SB, "writes 42 stores over 43 of the 44: `0` into `02AEDFB8`–`02AEE000`\n(`003849BC`",
     "writes 42 stores over 43 of the 44: `0` into `02AEDFB8`–`02AEE000` *(corrected 2026-10-02, OPUS: except "
     "`02AEDFF8` and `02AEDFFC`, which get `0xFFFFFFFF` at `00384A59` / `00384A63`)*\n(`003849BC`"),

    # C17: the applier's stat deltas are foe-only (0031189B cmp byte ptr [rdi + 5], 1 / jne).
    (FM, "— a\n  result can raise base HP, base MP and two stat words directly (the applier",
     "— ~~a~~\n  ~~result can raise base HP, base MP and two stat words directly~~ on foe records only: `0031189B` "
     "`cmp byte ptr [rdi + 5], 1` / `jne` skips all four adds unless the kind is 1, so a result cannot change a party "
     "record's base stats *(corrected 2026-10-02, OPUS: checked at `0031189B`–`0031189F`; §2.2, the `FE-6` correction "
     "of 2026-09-26)* (the applier"),
    (FM, "`+0x14` (`003118D9`, `003118F7`, `00311915`) with no kind test in sight (`FE-6`). The",
     "`+0x14` (`003118D9`, `003118F7`, `00311915`) ~~with no kind test in sight (`FE-6`)~~ behind the kind test "
     "`0031189B` (`cmp byte ptr [rdi + 5], 1` / `jne`), so on foe records only *(corrected 2026-10-02, OPUS: checked at "
     "`0031189B`–`0031189F`; the `FE-6` correction above)*. The"),

    # C18: base MP is read sign-extended (002FF084 movsx ecx, word ptr [rdi + 0xc]).
    (FM, "| `+0x00C` | 2 | u16 | **base MP stat",
     "| `+0x00C` | 2 | ~~u16~~ s16 *(corrected 2026-10-02, OPUS: the rebuild sign-extends it, `002FF084` "
     "`movsx ecx, word ptr [rdi + 0xc]`)* | **base MP stat"),
    (FM, "+0x0C u16 base MP    +0x10..+0x1F  UNION by kind +0x05: party (kind 0) f32[4]; else i16[8]   "
         "(+0x0A/0E words: rebuild inputs)\n  +0x20 u8   rank",
     "+0x0C u16 base MP    +0x10..+0x1F  UNION by kind +0x05: party (kind 0) f32[4]; else i16[8]   "
     "(+0x0A/0E words: rebuild inputs)   <- corrected 2026-10-02, OPUS: +0x0C is s16 (002FF084 movsx)\n"
     "  +0x20 u8   rank"),

    # C19 + C53 (README, Evaluation-Context line): the context is 0x30 bytes (003847F3); EC's front matter AUDITED.
    (R, "  **DOCUMENTED, tier 1.** The 0x2A-byte record every calculator slot is handed:",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The ~~0x2A-byte~~ `0x30`-byte *(corrected 2026-10-02, OPUS: the builder's last store is "
     "`mov qword ptr [rcx + 0x28], rax` at `003847F3`; the page's §9 falsification pass)* record every calculator slot "
     "is handed:"),

    # C20: the class domain is 0..4 and the code has no arm for 4 (0038B2A8 ... 0038B584). Code block: comment.
    (WX, "  02099DA8  global environment class   0..3\n  02099DAC",
     "  02099DA8  global environment class   0..3   <- corrected 2026-10-02, OPUS: the domain is 0..4; the stage has "
     "arms for 0..3 only and class 4 matches none (0038B2A8, 0038B3F4, 0038B4FE, 0038B478, 0038B584; the OPUS "
     "2026-09-21 section below)\n  02099DAC"),

    # C21: the interpreter is read (C-RW section 2 and 4: -1 terminators, the stop flag; STP section 11).
    (CST, "The interpreter that walks a recipe is **not read here**; this contract",
     "~~The interpreter that walks a recipe is **not read here**;~~ *(answered: see CONTRACT-weapon-recipes.md §2 and "
     "§4 — the two `-1`-terminated lists and the stop flag — and combat-formula-step-table.md §11, \"The interpreter, "
     "read\"; 2026-10-02, OPUS)* this contract"),
    (CST, "- **The interpreter that walks a recipe is not read**, so how a list is terminated, whether ids may\n"
          "  repeat, and what a second finalize does are all open (`ST-5`).",
     "- ~~**The interpreter that walks a recipe is not read**, so how a list is terminated,~~ *(answered: see "
     "CONTRACT-weapon-recipes.md §2 and §4 — each list is `-1`-terminated and the walk stops when `02AEDFB8` is 1 — and "
     "combat-formula-step-table.md §11; 2026-10-02, OPUS)* whether ids may\n"
     "  repeat, and what a second finalize does are ~~all~~ open (`ST-5`)."),

    # C22: the step-table page's own interpreter claims (answered on the same page, sections 7 and 11).
    (STP, "authored action data  ->  a recipe: a sequence of step ids   [interpreter NOT read]\n"
          "                              |",
     "authored action data  ->  a recipe: a sequence of step ids   [interpreter NOT read]   <- corrected 2026-10-02, "
     "OPUS: read, section 11 and section 7 (AK-1, AK-7)\n"
     "                              |"),
    (STP, "It does not\nestablish that anything walks a list of ids at runtime — the interpreter is unread, and the word\n"
          "\"recipe\" is carried over from the ranged-weapon document, which established two bindings but not the\n"
          "execution model.",
     "~~It does not~~\n~~establish that anything walks a list of ids at runtime — the interpreter is unread, and the "
     "word~~\n"
     "~~\"recipe\" is carried over from the ranged-weapon document, which established two bindings but not the~~\n"
     "~~execution model.~~ *(answered: see §11, \"The interpreter, read\", and §7's AK-1 / AK-7 — "
     "`BattleFormula_ResolveTargetResult` `00385F60` walks a recipe's two `-1`-terminated lists through this table; "
     "2026-10-02, OPUS)*"),

    # C23: seven targets carry several ids (the table bytes; C-ST ST-2).
    (STP, "- **An id is not an identity.** Six targets are reachable by two or three ids each;",
     "- **An id is not an identity.** ~~Six~~ Seven targets *(corrected 2026-10-02, OPUS: counted in the table at "
     "`01EFA5C0` — the six of §2 plus `0038F5A0`, ids 115 / 160; CONTRACT-formula-step-table.md ST-2)* are reachable "
     "by two or three ids each;"),
    (CST, "treating an id as a behaviour makes six ids alias wrongly.",
     "treating an id as a behaviour makes ~~six ids~~ the ids of seven targets alias wrongly *(corrected 2026-10-02, "
     "OPUS: ST-2 above lists seven)*."),

    # C24: four live slots no recipe names: 37, 73, 118, 131 (the 109 lists at 01EF96C0).
    (STP, "and only two bodies are named by no shipped\n> recipe — 118 and 131, read above.",
     "and ~~only two bodies are named by no shipped~~\n> ~~recipe — 118 and 131, read above.~~ four live slots are "
     "named by no shipped recipe — 37, 73, 118 and 131 *(corrected 2026-10-02, OPUS: checked against the 109 lists at "
     "`01EF96C0`; §12b.1–§12b.2)*; 118 and 131 are read above."),

    # C25: 42 slots hold ret 0; 38 of them are named by no recipe (01EFA5C0; the no-op ids 28, 193, 198, 199).
    (CPF, "of the 202 slots, 38 hold the `ret 0`, 160 are named",
     "of the 202 slots, ~~38 hold the `ret 0`~~ 42 hold the `ret 0` (38 of them named by no recipe; the four no-op "
     "ids 28, 193, 198 and 199 are among the 160 named) *(corrected 2026-10-02, OPUS: counted in the table at "
     "`01EFA5C0` and the 109 lists at `01EF96C0`; CONTRACT-formula-step-table.md §4)*, 160 are named"),

    # C26: 02AEE054 has 127 references (64 writes, 63 reads) in 45 functions (retool.py refs 02AEE054).
    (AD, "`02AEE054` alone is touched at **380 sites across\n45 functions**, every one",
     "`02AEE054` alone is touched at ~~**380 sites across~~\n~~45 functions**~~ **127 instructions — 64 writes, 63 "
     "reads — across 45 functions** *(corrected 2026-10-02, OPUS: `retool.py refs 02AEE054`; "
     "the-formula-scratch-block.md §2.2 and its access TSV, 127 rows)*, every one"),
    (AD, "| 380 sites / 45 functions touch the multiplier slot |",
     "| ~~380 sites~~ 127 instructions *(corrected 2026-10-02, OPUS: `retool.py refs 02AEE054`, 64 writes and 63 "
     "reads)* / 45 functions touch the multiplier slot |"),
    (AD, "                    (380 sites on the multiplier slot alone)  -- NOT read here\n```",
     "                    (380 sites on the multiplier slot alone)  -- NOT read here   <- corrected 2026-10-02, OPUS: "
     "127 instructions, 64 writes and 63 reads (retool.py refs 02AEE054)\n```"),

    # C27: the reset is 42 stores over 43 entries, eighteen number words -1 (003849B0-00384B03).
    (SB, "| the block is 44 words from `02AEDFB8` and the reset touches 41 |",
     "| the block is 44 words from `02AEDFB8` and the reset touches ~~41~~ 43 of them in 42 stores *(corrected "
     "2026-10-02, OPUS: `003849B0`–`00384B03` read whole; the falsification pass below)* |"),
    (SB, "`0xFFFFFFFF` into the seventeen number words `02AEE004`–`02AEE048`",
     "`0xFFFFFFFF` into the ~~seventeen~~ eighteen number words `02AEE004`–`02AEE048` *(corrected 2026-10-02, OPUS: "
     "`003849B0`–`00384B03` read whole — eighteen words in that range, and `02AEDFF8`, `02AEDFFC` and `02AEE050` get "
     "`-1` too)*"),

    # C28: FT-4 was answered 2026-09-15 (section 7).
    (SB, "not re-derived, and `FT-4` remains open.",
     "not re-derived~~, and `FT-4` remains open~~ *(answered: see §7 — `FT-4` ANSWERED 2026-09-15, FABLE; 2026-10-02, "
     "OPUS)*."),

    # C29: context +0x18 0xD is Undead (EC section 7); augment 15 is "Reverses effects of restorative items" (EC 2.3).
    (SB, "(the unit byte `FQ-2` leaves\n      unnamed): the history bit",
     "(the unit byte ~~`FQ-2` leaves~~\n      ~~unnamed~~ is the enemy class, and `0xD` is Undead *(answered: see "
     "the-evaluation-context-field-map.md §7, ANSWERED 2026-09-18; 2026-10-02, OPUS)*): the history bit"),
    (SB, "  - **Not claimed:** which augment shares merged id 15 with Slow, what the history bit is for",
     "  - **Not claimed:** ~~which augment shares merged id 15 with Slow,~~ *(answered: augment 15, \"Reverses effects "
     "of restorative items\" — the-evaluation-context-field-map.md §2.3; 2026-10-02, OPUS)* what the history bit is "
     "for"),

    # C30: the combos page's limits list is answered below it (2026-09-11, 2026-09-30, GR-8).
    (CB, "**What this document does not claim:** what `02AEDFDC` and `02AEDFE4` hold or who sets them, what\n"
         "status bit 23 on the target means, what the other bits of the 64-byte slot hold, what `02AEDFC8` is, or\n"
         "what consumes the guard/parry flag downstream.",
     "**What this document does not claim:** ~~what `02AEDFDC` and `02AEDFE4` hold or who sets them, what~~\n"
     "~~status bit 23 on the target means, what the other bits of the 64-byte slot hold, what `02AEDFC8` is, or~~\n"
     "~~what consumes the guard/parry flag downstream.~~ *(answered: every item, in the two notes directly below — "
     "2026-09-11 and 2026-09-30, with `GR-8` answered 2026-09-30; what this page still does not claim is the last "
     "bullet's; 2026-10-02, OPUS)*"),
    (CB, "The rest of the 64-byte record is only partly\n  mapped (`GR-8`, Limits).",
     "~~The rest of the 64-byte record is only partly~~\n  ~~mapped (`GR-8`, Limits).~~ *(answered: `GR-8` ANSWERED "
     "2026-09-30 — the second half `+0x20`..`+0x3F` is never accessed and every field of the first half has a reader; "
     "see Limits; 2026-10-02, OPUS)*"),

    # C31: the cancel bits are Confuse (5) and Berserk (27) (WS, "The tail").
    (CSD, "  **The bits are answered; their meaning is not** *(2026-09-25",
     "  **The bits are answered; ~~their meaning is not~~** *(answered: they are Confuse (5) and Berserk (27) — "
     "where-a-stat-number-comes-from.md, \"The tail\"; 2026-10-02, OPUS)* *(2026-09-25"),

    # C32: the 9,999 cap is on max HP (002FF7E2 stores output +0, stats +0x24).
    (CSD, "A character's damage stops rising at 9,999 where an enemy's does not.",
     "A character's ~~damage~~ maximum HP stops rising at 9,999 where an enemy's does not *(corrected 2026-10-02, OPUS: "
     "the cap's store `002FF7E2` writes output `+0`, stats `+0x24`, max HP; D-3)*."),

    # C33: the cap is mov reg, imm + cmove, not a cmp (002FF7BD-002FF7C8).
    (WS, "> **The famous 9,999 is a `cmp` in this function**, and it applies",
     "> **The famous 9,999 is ~~a `cmp`~~ a `mov r8d, 0x270f` that a `cmove` selects in this function** *(corrected "
     "2026-10-02, OPUS: checked at `002FF7BD`–`002FF7C8`; CONTRACT-stat-derivation.md D-3)*, and it applies"),
    (WS, "- **Caps are code:** 9,999 / 999 / 99 / 255 / 100 are `cmp` literals in this body.",
     "- **Caps are code:** 9,999 / 999 / 99 / 255 / 100 are ~~`cmp` literals~~ literals in this body — the main value's "
     "9,999 is a `mov r8d, 0x270f` that a `cmove` picks, not a `cmp` *(corrected 2026-10-02, OPUS: `002FF7BD`–"
     "`002FF7C8`; CONTRACT-stat-derivation.md D-3)*."),

    # C34: the three skips are bit 24, +0x714/+0x6B4, id 0x113; 0x95 belongs to the bit-14 clear.
    (WS, "with three exceptions guarding action ids `0x113` and `0x95`",
     "with three exceptions ~~guarding action ids `0x113` and `0x95`~~ (unit bit 24, `+0x714 ≤ 0x21E` with "
     "`+0x6B4 ≥ 9`, and action id `0x113`; `0x95` belongs to the later bit-14 clear) *(corrected 2026-10-02, OPUS: the "
     "list below, `002FF99C`–`002FF9BF` and `002FF9E1`–`002FFA11`)*"),

    # C35: 002FEF30 is read whole (WS; C-SD).
    (AS, "Still not claimed: what any status id means, and the body of `002FEF30`",
     "Still not claimed: what any status id means~~, and the body of `002FEF30`~~ *(answered for the body: "
     "where-a-stat-number-comes-from.md and CONTRACT-stat-derivation.md read `002FEF30` whole; 2026-10-02, OPUS)*"),

    # C36: 005369C0 is read (FK-4, section 2.5 and section 7). Code block: comment.
    (SL, "     -> 0046AB10 (ring 02EBB560, table 02EBF018) -> 005369C0 (display, unread)\n```",
     "     -> 0046AB10 (ring 02EBB560, table 02EBF018) -> 005369C0 (display, unread)   <- corrected 2026-10-02, OPUS: "
     "read, FK-4 answered 2026-09-11 (section 2.5, section 7)\n```"),

    # C37: the HP page's own census (section 2.3) counts 23 calls in 14 scripts.
    (HP, "  two shipped scripts set it above zero (§2.3). `EY-2`.",
     "  ~~two shipped scripts set it above zero (§2.3).~~ the HP page's own census (§2.3) counts 23 calls in 14 scripts "
     "*(corrected 2026-10-02, OPUS: §2.3's correction of 2026-09-13)*. `EY-2`."),
    (HP, "above zero only in `dst_a01.ebp` (67)\nand `naf_a02.ebp` (1000)",
     "~~above zero only in `dst_a01.ebp` (67)~~\n~~and `naf_a02.ebp` (1000)~~ *(corrected 2026-10-02, OPUS: the HP "
     "page's own census (§2.3) counts 23 calls in 14 scripts)*"),

    # C38: EY-3 answered 2026-09-13, directly above.
    (HP, "(see §2.1). What the two callees do with it is still open.",
     "(see §2.1). ~~What the two callees do with it is still open.~~ *(answered: see `EY-3` directly above, ANSWERED 2026-09-13; "
     "2026-10-02, OPUS)*"),

    # C39: the status transition stores HP again (section 4, CORRECTED 2026-09-25; EXP-148).
    (CHP, "| the store is the only HP write | `00300749 mov dword ptr [rsi + 0x48], r14d`. Executed:",
     "| ~~the store is the only HP write~~ the store is `00300530`'s only HP write *(corrected 2026-10-02, OPUS: the "
     "status transition it calls stores HP again — §4, CORRECTED 2026-09-25; EXP-148)* | "
     "`00300749 mov dword ptr [rsi + 0x48], r14d`. Executed:"),

    # C40: the floor's purpose was answered by FABLE; its two writers are in section 14 item 1.
    (CHP, "rather than at zero — is a semantic reading and is **routed to FABLE**\n"
          "> (`OPUS-REQ-FABLE-HPFLOOR-MEANING`), not asserted here.",
     "rather than at zero — ~~is a semantic reading and is **routed to FABLE**~~\n"
     "> ~~(`OPUS-REQ-FABLE-HPFLOOR-MEANING`), not asserted here.~~ *(answered: FABLE answered "
     "`OPUS-REQ-FABLE-HPFLOOR-MEANING` on 2026-09-13 — every non-zero floor sits in a boss's or mark's spawn preamble "
     "with event-flag mode 1, an authored end or phase change; Current-HP/the-hp-write-and-the-lethal-transition.md "
     "§2.3; 2026-10-02, OPUS)*"),
    (CHP, "game, and nothing shows the `+0x48` floor being written by anything (§14).",
     "game~~, and nothing shows the `+0x48` floor being written by anything~~ *(answered: §14 item 1 names its two "
     "writers, the definition apply `0023ABDB` and the script verb's `00239832`; 2026-10-02, OPUS)* (§14)."),

    # C41: UQ-119 / FE-4 answered 2026-09-27 (section 7).
    (FM, "inherits that limit. `UQ-119` stays unticked.",
     "inherits that limit. ~~`UQ-119` stays unticked.~~ *(answered: see §7 — `UQ-119` / `FE-4` ANSWERED 2026-09-27, the seed repaired and "
     "the stored pointer followed; 2026-10-02, OPUS)*"),
    (FM, "| What the untouched bytes and the unnamed fields are | **not established** |",
     "| What the untouched bytes and the unnamed fields are | ~~**not established**~~ *(answered for the bytes: see "
     "§7, `FE-4` ANSWERED 2026-09-27 — four paddings and the unused region `+0x5C`–`+0x63`; 2026-10-02, OPUS)* |"),

    # C42: bit 2's writers store at displacement 0 (UQ-123: 0023AF28, 00239D89 / 00239D94).
    (FM, "two readers and no writer. No other bit",
     "two readers ~~and no writer~~ in this census; its writers store through a register at displacement 0 "
     "(`0023AF28`, `00239D89` / `00239D94`) *(answered: see §7, `UQ-123`, 2026-09-14; whether this sweep should see "
     "them is the open `FE-1` reconcile below; 2026-10-02, OPUS)*. No other bit"),

    # C43: the published TSV has 1,286 rows, 285 functions, 87 displacements.
    (FM, "| access rows | 1280 (807 at a seed, 473 through propagation) |",
     "| access rows | ~~1280 (807 at a seed, 473 through propagation)~~ 1,286 in the published TSV *(corrected "
     "2026-10-02, OPUS: counted in battle-stats-record-accesses.tsv)* |"),
    (FM, "| functions reached | 284 |",
     "| functions reached | ~~284~~ 285 *(corrected 2026-10-02, OPUS: distinct functions in the published TSV)* |"),
    (FM, "| offsets touched | 85 |",
     "| offsets touched | ~~85~~ 87 *(corrected 2026-10-02, OPUS: distinct displacements in the published TSV)* |"),
    (R, "  reaches 283 functions:",
     "  reaches ~~283~~ 285 functions *(corrected 2026-10-02, OPUS: distinct functions in the published "
     "battle-stats-record-accesses.tsv)*:"),

    # C44: the attack-defence page's open items, answered on the same page (AJ-1, AJ-2, AJ-9, AJ-10, AJ-12).
    (AD, "What remains open is which weapon type selects which variant, and the\n"
         "many *modifier* stages that sit between preparation and the final write.",
     "~~What remains open is which weapon type selects which variant, and the~~\n"
     "~~many *modifier* stages that sit between preparation and the final write.~~ *(answered: §7 AJ-1 — the weapon "
     "row's byte `+0x19` picks the variant, §5.1 — and §11a AJ-8, the modifier chain for every weapon family; "
     "2026-10-02, OPUS)*"),
    (AD, "It does **not**\nestablish how damage is finally derived from those three values — that is 45 unread functions "
         "away,\nand no equation of the form \"damage = (attack − defence) × multiplier\" is asserted here.",
     "~~It does **not**~~\n~~establish how damage is finally derived from those three values — that is 45 unread "
     "functions away,~~\n~~and no equation of the form \"damage = (attack − defence) × multiplier\" is asserted here.~~ "
     "*(answered: see §10, AJ-2 — `damage = raw ≤ 0 ? 0 : trunc(raw × multiplier)` with `raw = ATK + variance − DEF`; "
     "2026-10-02, OPUS)*"),
    (AD, "Which of A and B is HP versus something else is **not**\nestablished — both",
     "~~Which of A and B is HP versus something else is **not**~~\n~~established~~ *(answered: see §7, AJ-9 — "
     "`02AEE004` is the HP loss and `02AEE008` the HP gain; 2026-10-02, OPUS)* — both"),
    (AD, "**That\nis a lead, not a finding**: only the constants were extracted, not the conditions that select them,\n"
         "and this document does not claim which value applies when. **AJ-10.**",
     "~~**That~~\n~~is a lead, not a finding**: only the constants were extracted, not the conditions that select "
     "them,~~\n~~and this document does not claim which value applies when.~~ *(answered: see §12 — AJ-10 and AJ-12; "
     "the lead was wrong: step 97's constants are pairs chosen by unit category and its gates are HP-conditioned "
     "augments, none elemental; 2026-10-02, OPUS)* **AJ-10.**"),

    # C45: slots 72 and 73 have no +1 either (section 5.1; C-PF section 7).
    (AD, "is the only variant with **no `+1.0`** — its",
     "is ~~the only variant~~ one of three variants with **no `+1.0`** *(corrected 2026-10-02, OPUS: slots 72 and 73 "
     "have none either, §5.1 and CONTRACT-preparation-step-family.md §7)* — its"),

    # C46: the bows' first lists (recipe 27 is [5, 6, 22, 33, 34, 44]).
    (AD, "(bows: `[5, 6, 22, 33, 34, 35 / 36 / 44, 42 / 43]`): knockback",
     "(bows: ~~`[5, 6, 22, 33, 34, 35 / 36 / 44, 42 / 43]`~~ `[5, 6, 22, 33, 34, 35, 42]`, `[5, 6, 22, 33, 34, 36, 43]` "
     "and `[5, 6, 22, 33, 34, 44]` for recipes 25, 26 and 27 *(corrected 2026-10-02, OPUS: decoded at "
     "`01EF9C80`–`01EF9FB0`; 44 is recipe 27's resolver, not a weather scale — ranged-weapon-recipes.md E-4)*): "
     "knockback"),

    # C47: the builder caches the target unit in 02EBF188 (00384870).
    (EC, "- **The context is per resolution and lives on the stack**: nothing persists it.",
     "- **The context is per resolution and lives on the stack**: ~~nothing persists it~~ the context itself is not "
     "persisted, but its builder caches the target unit in `02EBF188` (`00384870`) *(corrected 2026-10-02, OPUS: §9, "
     "\"The builder is not side-effect-free\")*."),

    # C48: the early-out's TESTs are at 0038B226 / 0038B233 / 0038B23D (0038B220 push rdi). Code block: comment.
    (WX, "0038B220  TEST byte ptr [RDX+6A],01   ; target BKBI +0x68 layer, bit 16\n0038B222  JNE  skip",
     "0038B220  TEST byte ptr [RDX+6A],01   ; target BKBI +0x68 layer, bit 16   <- corrected 2026-10-02, OPUS: the TEST "
     "is at 0038B226 (0038B220 is push rdi, 0038B222 sub rsp, 0x30)\n"
     "0038B222  JNE  skip   <- corrected 2026-10-02, OPUS: the JNE is at 0038B22D; the next two tests are 0038B233 and "
     "0038B23D"),

    # C49: the multipliers are .rdata constants (0038B299 [01CEBB70], 0038B3E5 [008FCC90]).
    (WX, "literal float constants inside\n  `0038B220`. The *classes*",
     "~~literal float constants inside~~\n  ~~`0038B220`~~ float constants in `.rdata` that `0038B220` loads — ×0.5 "
     "from `01CEBB70` (`0038B299`) and ×1.2 from `008FCC90` (`0038B3E5`) *(corrected 2026-10-02, OPUS: checked at "
     "those addresses; CONTRACT-environmental-element-scaling.md, the rule table)*. The *classes*"),

    # C50: 002FAE40 reads the shop table (002FAE4A mov rax, [02EBF158]); the favoured side is a 12-Items page.
    (CC, "`002FAE40` (114 B) is the bank-recipe row read:",
     "`002FAE40` (114 B) is ~~the bank-recipe row read~~ the shop-table row read *(corrected 2026-10-02, OPUS: checked "
     "at `002FAE4A`, `mov rax, [02EBF158]`, the shop table; 12-Items-Equipment-Shops-License/"
     "the-shop-table-and-its-stock-gates.md §2.3, `002FAE40(shopIndex)`)*:"),
    (CC, "calls `002FAE40`, the bank-recipe row read — the recipe table is script-driven.",
     "calls `002FAE40`, ~~the bank-recipe row read — the recipe table is script-driven~~ the shop-table row read, for "
     "the script verb `setshopname` *(corrected 2026-10-02, OPUS: `002FAE4A` reads `02EBF158`, the shop table; "
     "12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md §2.3)*."),

    # C51: preparation is slots 60-79 (section 2; C-PF).
    (STP, "Preparation sits at 65–79, the modifiers",
     "Preparation sits at ~~65–79~~ 60–79 *(corrected 2026-10-02, OPUS: §2's table and "
     "CONTRACT-preparation-step-family.md, slots 60–79)*, the modifiers"),

    # C52: the element-affinity page's limits (C-WE section 3; SB section 2.2).
    (EA, "**What this document does not claim:** which bit is which element, what `00384B10` does, where the\n"
         "absorb and nullify globals are consumed, or what the running multiplier at `02AEE054` is initialised\n"
         "to and by whom.",
     "**What this document does not claim:** ~~which bit is which element,~~ what `00384B10` does~~, where the~~\n"
     "~~absorb and nullify globals are consumed, or what the running multiplier at `02AEE054` is initialised~~\n"
     "~~to and by whom~~. *(answered: the element bits are CONTRACT-environmental-element-scaling.md §3's mask; the "
     "absorb and nullify globals are consumed by the finaliser `0038D280`, and `02AEE054` is reset to 0 by `003849B0` "
     "at `00384A29` — Scratch-Block/the-formula-scratch-block.md §2.2; 2026-10-02, OPUS)*"),

    # C53: README labels against each page's own front matter, the twelve pages it omitted, and the stale list.
    (R, "  the 109-recipe machinery, with Bow (25) and Crossbow (26) closed - **PARTIAL**",
     "  the 109-recipe machinery, with Bow (25) and Crossbow (26) closed - ~~**PARTIAL**~~ **DOCUMENTED** *(corrected "
     "2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)*"),
    (R, "  how weather and ground change elemental damage - **DOCUMENTED**",
     "  how weather and ground change elemental damage - ~~**DOCUMENTED**~~ **AUDITED** *(corrected 2026-10-02, OPUS: "
     "the page's front matter says `status: AUDITED`)*"),
    (R, "  **DOCUMENTED, tier 1.** The one function every damage and heal ends in:",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The one function every damage and heal ends in:"),
    (R, "  **DOCUMENTED, tier 1.** The recompute every stats write ends in",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The recompute every stats write ends in"),
    (R, "  **DOCUMENTED, tier 1.** The `0x1C8` stats record",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The `0x1C8` stats record"),
    (R, "— **DOCUMENTED, tier 1.** Calculator",
     "— ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. Calculator"),
    (R, "  **DOCUMENTED, tier 1.** The 44 globals",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The 44 globals"),
    (R, "  **DOCUMENTED, tier 1.** Four recipes",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. Four recipes"),
    (R, "  walked-distance accumulator, explained.\n\n## Not yet documented",
     "  walked-distance accumulator, explained.\n\n"
     "- [`elemental-affinity-and-the-five-bytes.md`](elemental-affinity-and-the-five-bytes.md) — element affinity, "
     "the five bytes `+0x40`–`+0x44` — **AUDITED**\n"
     "- [`combos-and-the-guard-parry-flag.md`](combos-and-the-guard-parry-flag.md) — the combo count and the "
     "guard / parry flag — **DOCUMENTED**\n"
     "- [`Step-Table/combat-formula-step-table.md`](Step-Table/combat-formula-step-table.md) — the 202-slot step "
     "table at `01EFA5C0` — **AUDITED**\n"
     "- [`Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`]"
     "(Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) — the preparation variants, the finaliser and "
     "the modifier chain — **AUDITED**\n"
     "- [`where-a-stat-number-comes-from.md`](where-a-stat-number-comes-from.md) — the stat rebuild `002FEF30` — "
     "**DOCUMENTED**\n"
     "- [`Status-And-Augment-Namespaces/README.md`](Status-And-Augment-Namespaces/README.md) — the status and augment "
     "ids that share one merged bitmap — no front-matter status\n"
     "- [`CONTRACT-formula-step-table.md`](CONTRACT-formula-step-table.md) — **CONTRACT READY**\n"
     "- [`CONTRACT-environmental-element-scaling.md`](CONTRACT-environmental-element-scaling.md) — "
     "**CONTRACT READY**\n"
     "- [`CONTRACT-weapon-recipes.md`](CONTRACT-weapon-recipes.md) — **CONTRACT READY**\n"
     "- [`CONTRACT-stat-derivation.md`](CONTRACT-stat-derivation.md) — **CONTRACT READY**\n"
     "- [`CONTRACT-preparation-step-family.md`](CONTRACT-preparation-step-family.md) — "
     "**BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-hp-write-and-lethal-transition.md`](CONTRACT-hp-write-and-lethal-transition.md) — "
     "**BEHAVIORALLY UNDERSTOOD**\n"
     "- *(twelve pages added to this list 2026-10-02, OPUS, each with the status its own front matter states)*\n"
     "\n## Not yet documented"),
    (R, "- `0038B6A0` `BattleFormula_ApplyActionElementAffinity` - resistance/weakness/absorb",
     "- ~~`0038B6A0` `BattleFormula_ApplyActionElementAffinity` - resistance/weakness/absorb~~ *(answered: see "
     "elemental-affinity-and-the-five-bytes.md; 2026-10-02, OPUS)*"),
    (R, "- `003896B0` `BattleFormula_RollAvoidGuardParryOutcome` - the standard outcome resolver",
     "- ~~`003896B0` `BattleFormula_RollAvoidGuardParryOutcome` - the standard outcome resolver~~ *(answered: see "
     "Scratch-Block/the-formula-scratch-block.md §2.3; 2026-10-02, OPUS)*"),
    (R, "- `00389040` `BattleFormula_LoadHitAvoidGuardThresholds`",
     "- ~~`00389040` `BattleFormula_LoadHitAvoidGuardThresholds`~~ *(answered: see "
     "Recipe-System/ranged-weapon-recipes.md §3 and Scratch-Block/the-formula-scratch-block.md §2.2; 2026-10-02, "
     "OPUS)*"),
    (R, "- The remaining 107 recipes and the full calculator-slot table at `0x01EFA5C0`",
     "- ~~The remaining 107 recipes and the full calculator-slot table at `0x01EFA5C0`~~ *(answered: see "
     "Recipe-System/ranged-weapon-recipes.md §7, E-3, and Step-Table/combat-formula-step-table.md; 2026-10-02, OPUS)*"),

    # C54: the step-table banner against its front matter (AUDITED; AK-3 answered, section 7).
    (STP, "**PARTIAL.** The table itself is read exactly:",
     "~~**PARTIAL.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`; the "
     "interpreter is read, §11, and AK-3 is answered, §7)*. The table itself is read exactly:"),
    (STP, "What remains open is the meaning of the 125 unnamed steps\n(**AK-3**), not the mechanism.",
     "~~What remains open is the meaning of the 125 unnamed steps~~\n~~(**AK-3**), not the mechanism.~~ *(answered: "
     "see §7 — AK-3 ANSWERED 2026-09-12; the front matter now says `status: AUDITED`; 2026-10-02, OPUS)*"),

    # C55: the attack-defence banner against its front matter (AUDITED).
    (AD, "**DOCUMENTED.** The seven preparation variants",
     "~~**DOCUMENTED.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`)*. The "
     "seven preparation variants"),

    # C56: the preparation family was executed (section 13: twenty-eighth pilot, 598 lines, 67 mutants).
    (CPF, "**Nothing in this family has been executed** (§13), so no\nrow claims more than static evidence.",
     "~~**Nothing in this family has been executed** (§13), so no~~\n~~row claims more than static evidence.~~ "
     "*(answered: see §13 — executed 2026-09-12 as the twenty-eighth differential pilot, 598 compared lines with 0 "
     "mismatches, and a 67-mutant campaign; 2026-10-02, OPUS)*"),

    # X2 (2.5): 0031E9A0 maps runtime 1-5 -> 1, 6 -> 2, 7-9 -> 3, so ammunition and accessories are kinds 1 and 3.
    (WS, "**kind 1 (weapons)** adds row `+0x1A` to attack",
     "**kind 1 (weapons)** — runtime categories 1–5, so ammunition too *(corrected 2026-10-02, OPUS: `0031E9A0` maps "
     "runtime 1–5 to 1, 6 to 2 and 7–9 to 3, checked at `0031E9AD`–`0031E9C4`; runtime 5 is arrows, bolts, shot and "
     "incendiaries, the-auto-status-rebuild.md)* — adds row `+0x1A` to attack"),
    (WS, "**kind 3 (armour)** adds row `+0x18` to defence",
     "**kind 3 (armour)** — runtime categories 7–9: helms, chest armour and accessories *(corrected 2026-10-02, OPUS: "
     "`0031E9B7`–`0031E9BF`; runtime 9 is the accessories)* — adds row `+0x18` to defence"),
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
