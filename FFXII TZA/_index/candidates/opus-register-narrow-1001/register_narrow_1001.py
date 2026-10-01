"""register_narrow_1001.py - register cell corrections, OPUS for SWE2-DATA (2026-10-01, FABLE inactive, user-authorized):
AL-8's evidence path to a tracked copy; SWE2-AUDIT-SEM's narrowings in GR-19 (C1, C2), SD-125 (C1), SD-128 (N3) and GR-2
(C1-C5). Old wording struck in place; the status lead word is untouched. EOL-preserving, pipe-free."""
import io
P = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\OPEN-QUESTIONS.md"
LF = chr(10)
R1 = "[review](candidates/auditsem-review-gr19-gr11-0930/REVIEW.md)"
R2 = "[review](candidates/auditsem-review-sd125-128-0930/REVIEW.md)"
R3 = "[review](candidates/auditsem-review-gr2-0930/REVIEW.md)"
EDITS = {
 "AL-8": [("map in `Tools/work/rtti/unit_record_fields.tsv`",
           "map in `candidates/al8-unit-record-fields-1001/unit_record_fields.tsv` (byte-identical tracked copy, 2026-10-01, "
           "OPUS for SWE2-DATA, of the gitignored work-tree file)")],
 "GR-19": [("when x is NaN)", "when ~~x is~~ any coordinate is NaN, C1)"),
           ("So a kill leaves no loot when the enemy dies where the leader could not stand: in another colliding body's reach, inside static geometry, off the map grid or off walkable ground.",
            "~~So a kill leaves no loot when the enemy dies where the leader could not stand: in another colliding body's "
            "reach, inside static geometry, off the map grid or off walkable ground.~~ *(Narrowed 2026-10-01, OPUS for "
            "SWE2-DATA, on SWE2-AUDIT-SEM's C2, " + R1 + ":)* So a kill leaves no loot when the enemy dies where the leader "
            "could not stand: another actor in the leader's movement-body layer within the leader's radius (the separation "
            "pass's pairing rule, not a contact test), a hit in `LQUERY` (`00391410`) at the point, a point off the "
            "navigation grid, or a refusal from the point query `0032A6A0` at the point or a corner; what the two queries "
            "test is not named, and how the defeated unit's own body is kept out of the gather is not read.")],
 "SD-125": [("With the effective flag 0 (FLEEING) and the bit clear, it closes the menu (`0027704E`: bit `0x200` + `00244F00`). So while fleeing, the command menu closes itself unless the top list is showing.",
             "~~With the effective flag 0 (FLEEING) and the bit clear, it closes the menu (`0027704E`: bit `0x200` + "
             "`00244F00`). So while fleeing, the command menu closes itself unless the top list is showing.~~ *(Narrowed "
             "2026-10-01, OPUS for SWE2-DATA, on SWE2-AUDIT-SEM's C1, " + R2 + ":)* Once its `001EDEC0(menu+0xB4)` gate "
             "passes and `+0x2FF0` bit 8 is clear, an effective flag of 0 (FLEEING) with the bit clear closes the menu "
             "(`0027704E`: bit `0x200` + `00244F00`); with the bit set, the menu applies its ordinary not-fleeing close "
             "rules instead. So while fleeing, the command menu closes itself unless the top list is showing; on the top "
             "list it stays subject to the usual close conditions.")],
 "SD-128": [("Per node it computes a fade level (",
             "Per node it computes a ~~fade~~ level (a per-unit render channel, read as fade; the channel, the character "
             "render record's channel 11, is named nowhere - SWE2-AUDIT-SEM's N3, " + R2 + ", 2026-10-01) (")],
}
APPEND = {
 "GR-2": (" *Narrowed 2026-10-01 (OPUS for SWE2-DATA, on SWE2-AUDIT-SEM's ACCEPT-WITH-NARROWING " + R3 + ", `gr2_sem.py` "
          "FAILS 0):* the nibble has six writers - `setfreetargettype`, `npc_to_gimmick` (`0x048E`, stores 4 at 2,036 "
          "us-copy sites, nearly all `treasure_NN`, type 4's largest authored source), `gimmick_to_npc` (`0x048F`, stores "
          "5, unused), the unit refresh, the battle-unit binder `00265A20` (stores 1) and the record initialiser "
          "`002666F8` (0, then 4 or 5); no script passes 0, 2 or 7, and no writer read produces 2; "
          "`btlAtelSetUnitType(3)` gives type 4 only while the spawn record has bit 5, else the next refresh turns it "
          "into 1; the refresh rewrites the nibble from the unit's mode, so a live value can differ from the script's; "
          "type 3 includes the five `disp_tama` objects (35 of the 68 distinct sites); type 6 is three boss-fight "
          "scripts' value, \"stationary\" being the `STAY_` naming of two; every count is nine language copies."),
}
t = io.open(P, encoding="utf-8", newline="").read()
L = t.split(LF)
for rid in list(EDITS) + list(APPEND):
    h = [i for i, l in enumerate(L) if l.startswith("| %s |" % rid)]
    assert len(h) == 1, rid
    i = h[0]
    for old, new in EDITS.get(rid, []):
        assert L[i].count(old) == 1, (rid, old[:50])
        assert "|" not in new
        L[i] = L[i].replace(old, new)
    if rid in APPEND:
        cr = L[i].endswith(chr(13))
        body = L[i].rstrip(chr(13))
        assert body.endswith(" |")
        assert "|" not in APPEND[rid]
        L[i] = body[:-2] + APPEND[rid] + " |" + (chr(13) if cr else "")
io.open(P, "w", encoding="utf-8", newline="").write(LF.join(L))
print("ok")
