"""apply_hit_odds.py [--apply] - the hit pipeline's odds: knockback (00388350), the counter chance (00388490),
the combo chance (00388550), the ranged critical (slot 29, 00389140) and the post-modifiers (00390F20), with the
statements those reads overturn, settled on the pages (OPUS, 2026-10-02).

Facts the edits rest on (checked at the bytes / shipped data):
  F1  00388490 (slot 7) writes 02AEDFDC from the target only: Speed +0x2D >> 1 when raw layer id 6 is set,
      Speed * 2 when ids 6 and 7 are both set, else 0 (0038849A-003884D8); a Stop / Sleep / Disable target
      (context +0x08 & 0x2018) gets 0. Augment 6 is "When attacked, automatically counter with weapon in hand."
      and augment 7 "Improves chance to counter." (listhelp_ability.bin). So 02AEDFDC is the counter chance and
      02AEDFC4, rolled against it by 003884F0, the counter flag; the shield and weapon parry are the evade bands.
  F2  00389140 (slot 29) sets result +0x18 bit 0 when the weapon row's +0x1C exceeds mt() % 100
      (003891B7-003891D9); slot 98 0038BE00 doubles 02AEE054 on that bit: the ranged critical. Bit 0's only
      writer is 003891D9 and slot 29 runs only in recipes 25 / 26 / 27, so slot 98 doubles only there.
  F3  00390F20 tests action-row word +0x2C bit 10 (0039110D: wake Sleep, clear Confuse) and bit 11 (0039118D:
      clear Invisible), i.e. byte +0x2D bits 2 and 3.
  F4  00388550 picks 1.8f over 0.7f for the combo chance on context +0x1B bit 5, merged id 13; augment 13 is
      "Improves chance of scoring multiple hits.", carried by Genji Gloves 0x1164.

Each edit strikes only the wrong words (every ~~ span opens and closes on one line, struck text verbatim) and
restates them, tagged *(corrected 2026-10-02, OPUS: ...)*. Function labels (e.g. ComputeParryChanceFromSpeed,
RollPrimaryFormulaResourceReactionMode2Chance) are names, not claims, and stay. No code-block lines are changed:
the ranged-weapon recipes' code line for slot 29 gets a tagged note after its block. No table column changes,
no heading changes. One section is inserted, only when its heading is absent, before an anchor heading that
occurs exactly once on its page.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
ST = "08-Combat-Formula/Step-Table/combat-formula-step-table.md"
SB = "08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md"
CB = "08-Combat-Formula/combos-and-the-guard-parry-flag.md"
RRF = "07-Combat-Action/Result-Record/the-result-record-field-map.md"
RW = "08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md"
AD = "08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md"
AR = "07-Combat-Action/Action-Definition-Row/the-action-definition-row.md"
EC = "08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md"

SEC = ("combat-formula-step-table.md, the section \"The hit pipeline's odds: knockback, counter, combo, the ranged "
       "critical and the post-modifiers\"")

# F1, as a tag reason
RC = ("`00388490` builds `02AEDFDC` only from the target's raw layer ids 6 and 7, augment 6 \"When attacked, "
      "automatically counter with weapon in hand.\" and augment 7 \"Improves chance to counter.\": Speed `+0x2D` / 2 "
      "with id 6, Speed × 2 with ids 6 and 7, else 0 (`0038849A`–`003884D8`), and `003884F0` rolls `02AEDFC4` "
      "against it; the shield and weapon parry are evade bands A and B, not this flag; " + SEC)
# F1, short form for second mentions on one page
RCS = ("`02AEDFC4` is the counter flag, rolled by `003884F0` against `00388490`'s counter chance, which only augment "
       "ids 6 \"automatically counter\" and 7 \"Improves chance to counter\" make nonzero; " + SEC)
# F2, as a tag reason
RX = ("`00389140` sets result `+0x18` bit 0 when the weapon row's `+0x1C` exceeds `mt() % 100` "
      "(`003891B7`–`003891D9`), and slot 98 `0038BE00` doubles `02AEE054` on that bit: the ranged critical, rolled "
      "only by recipes 25–27; " + SEC)
# F2, the recipes
RR = ("result `+0x18` bit 0 has one writer, slot 29 `00389140` at `003891D9` (a scan of `00380000`–`00395000` for "
      "`or dword [reg+0x18], 1` finds no other), and slot 29 runs only in recipes 25–27, so on recipes 20–24, 28, "
      "29, 64, 103 and 104 slot 98 is reached with the bit always clear; " + SEC)
# F3, as a tag reason
RP = ("`00390F20` tests word `+0x2C` bit 10 at `0039110D` (wake from Sleep, clear Confuse) and bit 11 at `0039118D` "
      "(clear Invisible), byte `+0x2D` bits 2 and 3, each only for a status in the target's word `+0x64` and not in "
      "`+0x3C`; " + SEC)
# F4, as a tag reason
R13 = ("`00388550` tests context `+0x1B` bit 5, merged id 13, to scale the combo rate by 1.8f instead of 0.7f "
       "(`0038855F`); augment 13 is \"Improves chance of scoring multiple hits.\", carried by Genji Gloves `0x1164`, "
       "and the 32 statuses are in neither layer (the-thirty-two-statuses.md, `BattleFormula_BuildEvaluationContext`), "
       "so the status reading is unsupported; " + SEC)

EDITS = [
    # ---- 02AEDFDC / 02AEDFC4: the counter chance and the counter flag, not parry (F1) ----
    (SB,
     "| `02AEDFC4` | 0 | 3 / 3 | **parry rolled** — ",
     "| `02AEDFC4` | 0 | 3 / 3 | ~~**parry rolled**~~ **counter rolled** *(corrected 2026-10-02, OPUS: " + RC + ")* — "),
    (SB,
     "| `02AEDFDC` | 0 | 4 / 1 | **parry chance** — ",
     "| `02AEDFDC` | 0 | 4 / 1 | ~~**parry chance**~~ **counter chance** *(corrected 2026-10-02, OPUS: " + RC + ")* — "),
    (SB,
     "| evaded — with parry (`[02AEDFC4]`) → kind **4**",
     "| evaded — with ~~parry~~ counter (`[02AEDFC4]`) *(corrected 2026-10-02, OPUS: " + RCS + ")* → kind **4**"),
    (SB,
     "| evaded — with parry → kind **2**",
     "| evaded — with ~~parry~~ counter *(corrected 2026-10-02, OPUS: " + RCS + ")* → kind **2**"),
    (SB,
     "| **parry rolled** |",
     "| ~~**parry rolled**~~ **counter rolled** *(corrected 2026-10-02, OPUS: " + RCS + ")* |"),
    (SB,
     "`02AEDFDC` (parry), `02AEDFD8` (knockback)",
     "`02AEDFDC` (~~parry~~ counter *(corrected 2026-10-02, OPUS: " + RCS + ")*), `02AEDFD8` (knockback)"),
    (CB,
     "**So only an\n  engaged target can parry.**",
     "**So only an\n  engaged target can ~~parry~~ counter.** *(corrected 2026-10-02, OPUS: " + RC + ")*"),
    (CB,
     "`02AEDFDC`, the parry threshold, is written by",
     "`02AEDFDC`, the ~~parry~~ counter threshold *(corrected 2026-10-02, OPUS: " + RCS + ")*, is written by"),
    (CB,
     "`02AEDFDC` the parry chance from speed\n"
     "(`BattleFormula_ComputeParryChanceFromSpeed` `00388490`), and the guard/parry flag is consumed by the\n"
     "outcome roller (`0038970A`, `00389779`: kinds 4 / 2 instead of 3 / 1) and by the preview into the\n"
     "result's flag word B bit 2 — [the scratch block](Scratch-Block/the-formula-scratch-block.md) §2.2–2.4.)*",
     "`02AEDFDC` the ~~parry~~ counter chance from speed\n"
     "(`BattleFormula_ComputeParryChanceFromSpeed` `00388490`), and the ~~guard/parry~~ counter flag is consumed by "
     "the\n"
     "outcome roller (`0038970A`, `00389779`: kinds 4 / 2 instead of 3 / 1) and by the preview into the\n"
     "result's flag word B bit 2 — [the scratch block](Scratch-Block/the-formula-scratch-block.md) §2.2–2.4.)* "
     "*(corrected 2026-10-02, OPUS: " + RC + ")*"),
    (RRF,
     "**1 / 2** band B evade (plain / with parry), **3 / 4** band A evade (plain / with parry), **5** band C evade",
     "**1 / 2** band B evade (plain / with ~~parry~~ counter), **3 / 4** band A evade (plain / with ~~parry~~ "
     "counter) *(corrected 2026-10-02, OPUS: " + RCS + ")*, **5** band C evade"),

    # ---- result +0x18 bit 0: the ranged critical, not a resource reaction (F2) ----
    (RRF,
     "bit 0 the mode-2 resource reaction chance rolled (`003891D9`), **bit 1 the combo continues** (`0038887A`), "
     "**bit 2 parry rolled** (`02AEDFC4`, `00385A2D`)",
     "bit 0 ~~the mode-2 resource reaction chance rolled~~ the ranged critical rolled (`003891D9`) *(corrected "
     "2026-10-02, OPUS: " + RX + ")*, **bit 1 the combo continues** (`0038887A`), **bit 2 ~~parry rolled~~ counter "
     "rolled** (`02AEDFC4`, `00385A2D`) *(corrected 2026-10-02, OPUS: " + RCS + ")*"),
    (SB,
     "| the mode-2 resource reaction chance rolled true |",
     "| ~~the mode-2 resource reaction chance rolled true~~ the ranged critical rolled true *(corrected 2026-10-02, "
     "OPUS: " + RX + ")* |"),
    (SB,
     "(`003075F9`) is **the mode-2 resource reaction chance rolled** (`003891D9`)",
     "(`003075F9`) is ~~**the mode-2 resource reaction chance rolled**~~ **the ranged critical rolled** (`003891D9`) "
     "*(corrected 2026-10-02, OPUS: " + RX + ")*"),
    # the code line "-> slot 29  00389140 resource-reaction roll" stays; a tagged note follows its block.
    (RW,
     "  -> BattleFormula_ApplyTargetResult (call at 00307436)\n```\n\n**Upstream:**",
     "  -> BattleFormula_ApplyTargetResult (call at 00307436)\n```\n\n"
     "*(corrected 2026-10-02, OPUS: slot 29 `00389140` in the block above is the ranged critical roll, not a "
     "resource-reaction roll; " + RX + ")*\n\n**Upstream:**"),
    (AD,
     "| 29 | `RollPrimaryFormulaResourceReactionMode2Chance` | name only |",
     "| 29 | `RollPrimaryFormulaResourceReactionMode2Chance` | ~~name only~~ **read**: the ranged critical *(corrected "
     "2026-10-02, OPUS: " + RX + ")* |"),

    # ---- slot 98 doubles only on recipes 25-27 (F2) ----
    (AD,
     "scalers of §12, 98 the conditional `×2` of §11, and 99 read now",
     "scalers of §12, 98 ~~the conditional `×2` of §11~~ the `×2` of §11, which can double only on recipes 25–27 "
     "and passes every other list's multiplier through unchanged *(corrected 2026-10-02, OPUS: " + RR + ")*, and 99 "
     "read now"),

    # ---- 00390F20 reads action-row word +0x2C bits 10 and 11, byte +0x2D bits 2 and 3 (F3) ----
    (AR,
     "`00390F20` tests bit 10 and `0030BB30` returns bit 14 (UQ-107)*",
     "`00390F20` tests ~~bit 10~~ bits 10 and 11 and `0030BB30` returns bit 14 (UQ-107)* *(corrected 2026-10-02, "
     "OPUS: " + RP + ")*"),
    (AR,
     "| `BattleStats_HasRequiredLicenseForAction` (`00323EC0`, at `00323F52`) | a flags byte.",
     "| `BattleStats_HasRequiredLicenseForAction` (`00323EC0`, at `00323F52`); "
     "`BattleFormula_ApplyTargetStatusActionPostModifiers` (`00390F20`, bits 2 and 3 through the word, `0039110D`, "
     "`0039118D`) *(corrected 2026-10-02, OPUS: the licence check is not the only reader; " + RP + ")* | a flags "
     "byte."),

    # ---- merged id 13 is the combo augment, not Disable (F4) ----
    (EC,
     "| 13 | **Disable** (status; augment 13 \"Improves chance of scoring multiple hits\") |",
     "| 13 | ~~**Disable** (status;~~ **the combo augment** (augment 13 \"Improves chance of scoring multiple hits\", "
     "Genji Gloves `0x1164`) *(corrected 2026-10-02, OPUS: " + R13 + ")* |"),
]

ANCHOR = "## 10. Falsification pass 2026-09-02 — two errors, both mine"
SECTIONS = [
    (ST, "## The hit pipeline's odds: knockback, counter, combo, the ranged critical and the post-modifiers "
         "(OPUS, 2026-10-02)", ANCHOR, "hit_odds_section.md"),
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
    for rel, heading, anchor, src in SECTIONS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        texts[rel] = t
        lines = t.replace("\r\n", "\n").split("\n")
        if heading in lines:
            print("ALREADY section", rel.split("/")[-1]); continue
        if lines.count(anchor) != 1:
            print("REFUSING section", rel.split("/")[-1], "anchor count", lines.count(anchor)); fails += 1; continue
        body = open(os.path.join(HERE, src), "rb").read().decode("utf-8").replace("\r\n", "\n").strip("\n")
        block = heading + "\n\n" + body + "\n\n"
        crlf = "\r\n" in t
        eol = "\r\n" if crlf else "\n"
        a = eol + anchor + eol
        if t.count(a) != 1:
            print("REFUSING section", rel.split("/")[-1], "anchor line"); fails += 1; continue
        texts[rel] = t.replace(a, eol + block.replace("\n", eol) + anchor + eol, 1)
        print(("PATCHED section " if apply else "WOULD PATCH section ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
