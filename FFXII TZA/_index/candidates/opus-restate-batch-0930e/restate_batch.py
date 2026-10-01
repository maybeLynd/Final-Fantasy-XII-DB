"""restate_batch.py - the ready-to-apply register restatement for OPUS-REQ-DATA-RESTATE-BATCH-0930E (OPUS, 2026-09-30).

For SWE2-DATA, the register owner. Ten rows whose answers are published records; each new status cell leads with the
ANSWERED statement and keeps the old cell verbatim after "*Previous status, kept as history:*" (the EO-1 precedent), so
no strike is added and no text is lost.

  python -B restate_batch.py            dry run: prints each row's old status lead and the new lead, checks every record
                                        path is tracked, every cited commit exists, and no new text carries a pipe
  python -B restate_batch.py --apply    writes _index/OPEN-QUESTIONS.md (mixed EOLs kept: only the ten lines change)

After --apply: run check_questions.py (grep its output for INCONSISTENT), tick the page boxes listed at the end, then
publish with publish_paths.sh. Nothing here decides a row; every sentence is its record's own answer.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REG = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")
C = "candidates/"

ROWS = {
    "SD-3": ("442815afc", "sd3-bit21-pause-0930",
             "aggregate capability-policy bit 21 decides whether the pause menu opens at once (bit clear), is deferred "
             "until 01FD4954 is set (row 1 holds the bit), or is refused (only another row holds it); and its writers are "
             "not only the Save/Load handlers - the movie player, 002CEB40 and others write it too (the record's W1)"),
    "SD-23": ("acb04148d` + `9af526c00", "sd23-sound-slots-38-39-0930` + `sd23-state7-dynamicsound-0930",
              "slot 38 marks a sound that plays no record of its own but delegates to a chosen child (VariationSound answers "
              "true); slot 39 marks a sound allowed to enter state 7, the terminal state - it finishes when its last child "
              "ends (CycleSound answers false)"),
    "SD-166": ("b3f5172c9", "sd166-arena-7-0930",
               "no code path in the shipped game selects arena 7 for an allocation after boot; only two debug verbs could, "
               "and no shipped script calls them"),
    "SD-181": ("2e1bb015e", "sd181-sp1-loader-0930",
               "02ADD060 holds slot 16 (SP1, the sound-emitter block) of the current map's "
               "ps2data/plan_master/map_ctrl/<area>/<map>/bin/<map>.mpk, stored by the pack completion 00378BC0 at 00378E9D"),
    "SD-190": ("8de16e58c", "sd190-tween-turn-bit-0930",
               "003E6A70's result bit 0 means the character's render record has an authored move-and-turn tween whose turn "
               "phase is still running; the direct-delta path needs it together with actor +0x0D bit 1 and a live record "
               "(the 003E68B0 gate at 0025E31D)"),
    "SD-191": ("f06af26c0", "sd191-party-swap-verbs-0930",
               "the party-swap verbs occur only in the 26 summon scripts (sum_a to sum_m, 0000 and 0001: the 13 Espers) and "
               "the special-attack script spc_z0000 - 738 calls in 27 files, the nine language copies agreeing - so flag B "
               "(02B40534) is down only inside summon entries and exits and that sequence; no field or story script calls them"),
    "SD-193": ("79ba50e5c", "sd193-turn-step-0930",
               "003EC040 is not an easing curve: it turns the heading (render record +0x124) toward the target at a constant "
               "angular step per call"),
    "SD-182": ("8acf79ac7", "sd182-nav-transform-pair-0930",
               "authored: the map pack carries both matrices, +0x50 is the inverse of +0x10 in the file bytes, and the "
               "engine points at those bytes and never writes them"),
    "SD-183": ("8acf79ac7", "sd183-steering-modes-0930",
               "the mode is BattleUnit +0x80 bits 0-4 with a countdown in bits 5-14, a steering override with a lifetime "
               "that 00339F00 runs only while the countdown is non-zero; modes 1 and 4 (0033CEF0) turn toward the goal and "
               "move inside a cone, 2 is 0033D200 and 6 an orbit (0033BAA0, bit 15 its direction); the writers are 0033CC80 "
               "(from the avoidance search 0033A720, modes 1-5), 003343D0 (mode 6) and 0033E1F0 (mode 0)"),
    "SD-62": ("dedfaf0d7", "sd62-registry-list-links-0930",
              "the root 01F2E330 chains class descriptors on +0x10 (node +0x50, writer 00639160) and non-root owner objects on "
              "+0x28 (node +0x00); its own +0x00 is a never-linked node; 01F2E780 is a 0x30-byte name-hash tree of class "
              "descriptors (node +0x08, key +0x20 hash / +0x28 name, insert 006388C0, remove 00638F00); the PWorld / "
              "getInstanceCount slots belong to a separate method record at 01F2E7B0, linked into PWorld's descriptor +0x90 "
              "list by 00635B80 (OPUS's F3 attribution corrected, opus-sd62-f3-adjudication-0930)"),
    "SD-184": ("8acf79ac7", "sd184-facing-sources-0930",
               "shipped data does store headings outside [-pi, pi] (setposparty facings up to 5.846853 rad), but the "
               "normaliser's defective fast path fires from none of them; the only shipped source that can reach it is the "
               "evt_t0505 debug accumulator"),
}
BOXES = {  # the page box each restated row closes (tick in the same publish; the page owner's wording)
    "SD-3": "15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md",
    "SD-23": "18-Audio (the sound-variant-selection page's SD-23 box)",
    "SD-166": "24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md",
    "SD-181": "06-Movement-And-Navigation/.../clamping-a-point-into-a-volume.md",
    "SD-182": "06-Movement-And-Navigation/the-unit-shape-distance-primitives.md (box at line ~171)",
    "SD-183": "06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md (box ~269)",
    "SD-184": "06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md (box ~914)",
    "SD-190": "06-Movement-And-Navigation (the movement-mode page's SD-190 box)",
    "SD-191": "06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md (box ~472)",
    "SD-193": "06-Movement-And-Navigation (setting-the-movement-mode page's SD-193 box)",
    "SD-62": "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md (box ~374)",
}


def lead(rid):
    sha, rec, ans = ROWS[rid]
    who = "SWE2-ORACLE" if sha in ("8acf79ac7", "dedfaf0d7") else "OPUS"
    recs = " + ".join("[`%s`](%s%s/README.md)" % (r.strip("` "), C, r.strip("` ")) for r in rec.split("` + `"))
    return "**ANSWERED 2026-09-30 (%s `%s`, record %s; restated by SWE2-DATA): %s.**" % (who, sha, recs, ans)


def main():
    apply = "--apply" in sys.argv
    raw = open(REG, "rb").read().decode("utf-8")
    lines = raw.split("\n")
    fails, done = 0, set()
    for k, l in enumerate(lines):
        m = re.match(r"\| (SD-\d+) \|", l)
        if not m or m.group(1) not in ROWS:
            continue
        rid = m.group(1)
        cr = l.endswith("\r")
        body = l.rstrip("\r")
        head, sep, status = body.rpartition(" | ")
        status = status.rstrip(" |")
        new = lead(rid)
        if "|" in new.replace("\\|", ""):
            print("FAIL %s new text carries a pipe" % rid); fails += 1
        if status.startswith("**ANSWERED"):
            print("SKIP %s already ANSWERED" % rid); done.add(rid); continue
        sha = ROWS[rid][0].split("`")[0]
        for s in re.findall(r"[0-9a-f]{9}", ROWS[rid][0]):
            if subprocess.run(["git", "-C", DB, "cat-file", "-e", s + "^{commit}"], capture_output=True).returncode:
                print("FAIL %s commit %s missing" % (rid, s)); fails += 1
        for r in ROWS[rid][1].split("` + `"):
            p = os.path.join(DB, "_index", C, r.strip("` "))
            if not subprocess.run(["git", "-C", DB, "ls-files", p], capture_output=True, text=True).stdout.strip():
                print("FAIL %s record %s untracked" % (rid, r)); fails += 1
        print("%s  old: %s" % (rid, status[:110]))
        print("%s  new: %s" % (rid, new[:160]))
        lines[k] = head + sep + new + " *Previous status, kept as history:* " + status + " |" + ("\r" if cr else "")
        done.add(rid)
    missing = set(ROWS) - done
    if missing:
        print("FAIL rows not found: %s" % sorted(missing)); fails += 1
    if apply and not fails:
        open(REG, "wb").write("\n".join(lines).encode("utf-8"))
        print("APPLIED %d rows" % len(done))
    print("page boxes to tick:"); [print("  %s: %s" % kv) for kv in sorted(BOXES.items())]
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
