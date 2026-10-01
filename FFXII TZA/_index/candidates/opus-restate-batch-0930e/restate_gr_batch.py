"""restate_gr_batch.py - the ready-to-apply register restatement of the answered GR rows (OPUS, 2026-09-30), for SWE2-DATA;
since 2026-09-30 also SD rows whose records are OPUS-lane (SD-7, SD-107), since this script reads each commit from git.

Same contract as restate_batch.py (the SD batch): each new status cell leads with the ANSWERED statement from its record
and keeps the old cell verbatim after "*Previous status, kept as history:*"; nothing is struck. The commit cited for each
row is read from git at run time (the last commit touching the record), so a row whose record is not yet published fails
the dry run instead of citing nothing.

  python -B restate_gr_batch.py            dry run (FAILS n last)
  python -B restate_gr_batch.py --apply    rewrite exactly those register lines (only when the dry run is clean)

GR-18 is left out: it is PARTIAL with a named runtime residue and has its own request (OPUS-REQ-DATA-GR18-ROW-0930).
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REG = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")

ROWS = {
    "GR-1": ("gr1-wait-slot-settled-0930", "OPUS",
             "never read as the settled flag: the interpreter clears it when arming a wait, and every native-command read of "
             "the scratch window slot +0x18..+0x27 (r8 = slot + 0x18) follows that command's own write"),
    "GR-2": ("gr2-free-target-values-0930", "OPUS",
             "as authored, 1 marks ordinary enemies (the default), 3 allied third parties and event combatants, 4 system objects "
             "(save crystals, anchors, chests), 5 non-combatant town and prison NPCs, and 6 stationary boss parts; 2 and 7 are "
             "never authored by the two verbs (7 is the refresh's value for flagged enemy rows)"),
    "GR-3": ("hud-blocks-identified-0930", "SWE2-ORACLE",
             "the combo popup (battle-HUD block _5380, pool B) shows the count 2 to 12 in one or two digits with a slam-in and "
             "a fading echo over about 0.53 s, holds 2 s following the unit and fades; at the cap of 12 it grows to 120 % and pulses"),
    "GR-4": ("gr4-gr5-action-row-readers-0930", "SWE2-STRUCT",
             "one reader, BattleAction_GetPresentationParameter 0030A190: the Quickening / Concurrence cinematic effect id "
             "(120 + id - 0xD0) while the special sequence is on screen"),
    "GR-5": ("gr4-gr5-action-row-readers-0930", "SWE2-STRUCT",
             "no reader: only the five MP-cost byte reads cover +0x0A; on rows 182-207 the byte repeats the matching summon row's +0x0A"),
    "GR-6": ("gr6-action-row-24-0930", "OPUS",
             "a bit-15-clear +0x24 word is the action's effect id (374 rows, values 0-396); on the 62 summon-class rows "
             "(+0x0C bit 30) it is the special-sequence load id"),
    "GR-7": ("gr7-kind10-reader-0930", "OPUS",
             "kind 10 is BattleUnit +0xB90, a 'used on me' mask; its only reader is AiOrder_EvaluateTargetSelector 00301AD0 "
             "(opcode 0x36 / 0x37, mode 3), used only by the enemy .ard order sets; +0x3A is an AI reaction class"),
    "GR-8": ("gr8-unit-record-64-0930", "SWE2-STRUCT",
             "+0x20..+0x3F is never accessed; +0x00 u32 recipe damage stash, +0x04 / +0x08 miss / immune bits, +0x0C marked "
             "targets, +0x10 the drawn id for action 0x9F, +0x14 periodic HP-credit tick, +0x18 walking-MP carry, +0x1C movement flags"),
    "GR-9": ("gr9-order-subgroup-entry-0930", "OPUS",
             "nothing outside an enemy's own order set enters its subgroups: +0x6B5 is set non-zero only from the committed "
             "order id, whose only run-time source is the player's battle menu; the 155 sets' unreached subgroups are authored "
             "and never entered"),
    "GR-10": ("gr10-camera-record-2-0930", "OPUS",
              "record 2 is the ordinary field camera; the intervention target is on screen from setinterventioncamera(1, n) "
              "until the verb's clear or a manager-0 unload, whenever no event camera (records 4-7) is active"),
    "GR-13": ("gr13-15-shop-list-widget-0930", "SWE2-STRUCT",
              "the premise is wrong - 0057DAD0 rows are layout A and the driver reads them correctly; the zero-price sentinel "
              "is set only for selector 0x0F; category 7 is loot"),
    "GR-14": ("gr13-15-shop-list-widget-0930", "SWE2-STRUCT",
              "no: 005651E0 runs only in the inventory list procedures (ids 0x405-0x40F), and shop lists never receive message 26"),
    "GR-15": ("gr13-15-shop-list-widget-0930", "SWE2-STRUCT",
              "inventory lists take kinds 0-7 (the widget-id table 00D233A0), shop lists 32 / 19 / 31 (Buy / Sell / Bazaar), and "
              "equip lists kind 1 as a constant or the chosen slot 0-4"),
    "GR-17": ("gr17-reward-table-lifetime-0930", "SWE2-ORACLE",
              "no window along direct control flow: the .ard reward tables are freed only in the same call that zero-fills "
              "every battle unit, and the release's effect chain is closed by c_all.efx carrying none of the reaching opcodes "
              "(record gr17-effect-residue-0930)"),
    "GR-19": ("gr19-drop-position-gate-0930", "OPUS",
              "a kill drops loot only where the death spot is a clear, walkable place for the party leader: the shared spot "
              "test 003377C0 answers 0 when any actor of the leader's collision group stands within its radius, and otherwise "
              "requires a navigation region (00384130) and walkability for its movement class at the spot and four offsets (00336390)"),
    "GR-11": ("gr11-camera-context-0930", "OPUS",
              "the install copies the outgoing leader's movement-body placement record (+0x30..+0xDF) into context +0x7A0, "
              "but the camera uses only position and heading: the interpolator 00259510 and the field-tick blend 00259620 "
              "read the pose blocks only at +0x00..+0x1F, and 00259620 and the teardown 0025A6A0 rewrite +0x6F0 whole from a "
              "stack local of which only the first 0x20 bytes are written, so +0x710..+0x79F hold stack residue and no code "
              "reads them as values"),
    "GR-12": ("gr12-actions-9c-9d-0930", "SWE2-CONTRACT for OPUS",
              "neither does anything: 0x9B-0x9D are the effect-free category-13 rows of a cut battle-menu Gambits sub-list "
              "(named only in the de and fr text); an issued 0x9C or 0x9D is refused before commit for a party unit "
              "(003060E0 returns 5, 00306480 gives reason 0x0F), the kind-24 list that would issue them is always built "
              "empty, and no order set names them; 00273270's 0x0000FFFF preset never survives 00329220's memset"),
    "SD-7": ("sd7-sd107-closure-0930", "SWE2-STRUCT for OPUS",
             "no caller: every [vtable+0x78] dispatch site is typed to a non-application object, no register-target call "
             "loads its target from [reg+0x78], and the only image qword equal to 0017D1A0 is its own vtable entry, so "
             "GameApplication slot 15 is called nowhere and the input manager's +0x39 poll gate is set only by 001989D0"),
    "SD-107": ("sd7-sd107-closure-0930", "SWE2-STRUCT for OPUS",
               "no: of the stores that can reach a text element's kind byte +0xA3, the only constant-1 store (002475D0) acts "
               "on widget bases, the two other direct byte writers act on PPFX effect objects, and the 72 remaining "
               "dword or qword stores at +0xA0 touch +0xA3 only as a field's top byte on objects without a text element's "
               "layout, so no traced code builds a kind-1 text element (static; a whole-element copy would need a kind-1 "
               "source first)"),
    "UQ-384": ("swe2struct-uq384-385-0930", "SWE2-STRUCT for OPUS",
               "[01FC35F8] holds 02CC1CD0 (= 02CC0410 + 0x18C0), the embedded PrimitiveRendererD3D11 (vtable 00D86960, RTTI, 45 "
               "slots), written only at 0021037B from GiVmax slot 1's rdx (the Gi execute callback 001F4A10 supplies the render "
               "context's +0x18C0); static storage built in place by 00615840 and 006C8750; the replay calls 17 of its slots "
               "from 24 sites; PACKED reaches 12 handler arms and A+D 14, and FGE, FIX, FOG, FOGCOL, int Q and ZBUF_1/ZBUF_2 are "
               "stored and never read"),
    "UQ-385": ("swe2struct-uq384-385-0930", "SWE2-STRUCT for OPUS",
               "none of the 19 is a VU JAL or JR sub-program target and none is data-referenced: all 19 are VU1 microprogram "
               "entries (of UQ-213's 57), each address formed only by a rip lea passed as a registrar's program argument (48 "
               "sites) and started by MSCAL through the program table 02068E30; no VU microcode is embedded (MPG carries one "
               "x64 pointer)"),
    "MS-4": ("swe2struct-residue3-0930", "SWE2-STRUCT for OPUS",
             "the container's message 0x20 comes from its own relay child 002BA240: once its own load group has finished "
             "and the loader 02B457E0 has sent code 0x100, the container sends itself 0x22, which creates, parents and "
             "activates the relay; the relay retires at once and on its destroy notice sends {0x20, 0, 0} to its ancestors "
             "through 00275440, the container first; the container's 0x20 arm (003CB7DB) then opens the preload page "
             "003CB4F0 with message 14 carrying the current field's sub-location index (003BFDF0; the container's mode is 5, "
             "so the mode-6 branch never applies); its own message 14 is only the activation helper's static copy, ignored "
             "(OPUS opus-ms4-0930)"),
}


def commit_of(rec):
    return subprocess.run(["git", "-C", DB, "log", "-1", "--format=%h", "--", os.path.join(DB, "_index", "candidates", rec)],
                          capture_output=True, text=True).stdout.strip()


def main():
    apply = "--apply" in sys.argv
    lines = open(REG, "rb").read().decode("utf-8").split("\n")
    fails, done = 0, set()
    for k, l in enumerate(lines):
        m = re.match(r"\| ((?:GR|SD|UQ|MS)-\d+) \|", l)
        if not m or m.group(1) not in ROWS:
            continue
        rid = m.group(1)
        rec, who, ans = ROWS[rid]
        cr = l.endswith("\r")
        head, sep, status = l.rstrip("\r").rpartition(" | ")
        status = status.rstrip(" |")
        if status.startswith("**ANSWERED"):
            print("SKIP %s already ANSWERED" % rid); done.add(rid); continue
        sha = commit_of(rec)
        if not sha:
            print("FAIL %s record %s not published yet" % (rid, rec)); fails += 1; done.add(rid); continue
        new = "**ANSWERED 2026-09-30 (%s `%s`, record [`%s`](candidates/%s/README.md); restated by SWE2-DATA): %s.**" % (who, sha, rec, rec, ans)
        if "|" in new:
            print("FAIL %s new text carries a pipe" % rid); fails += 1
        print("%s  new: %s" % (rid, new[:150]))
        lines[k] = head + sep + new + " *Previous status, kept as history:* " + status + " |" + ("\r" if cr else "")
        done.add(rid)
    if set(ROWS) - done:
        print("FAIL rows not found: %s" % sorted(set(ROWS) - done)); fails += 1
    if apply and not fails:
        open(REG, "wb").write("\n".join(lines).encode("utf-8"))
        print("APPLIED")
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
