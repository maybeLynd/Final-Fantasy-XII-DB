"""gr2_check.py - GR-2: what each free-target type value denotes as authored (OPUS, 2026-09-30).
Re-runs gr2_census.py (SD-160's decoder loop over every shipped .ebp; each call of setfreetargettype 0x265 stores its
argument, each btlAtelSetUnitType 0x3005 stores {1, 5, 3, 4}[v] through 002396B0) and checks the per-value result.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = subprocess.run([sys.executable, "-B", os.path.join(HERE, "gr2_census.py")], capture_output=True, text=True).stdout
fails = 0
def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
calls = {(int(t), v): int(n) for t, v, n in re.findall(r"^type (\d) <- (\S+) +(\d+) calls", out, re.M)}
tops = {int(t): s for t, s in re.findall(r"^type (\d): .*?top: (.*)$", out, re.M)}
check("C1", "rows: 63432" in out and sum(calls.values()) == 63432, "63,432 calls of the two verbs, every one a pushed constant")
check("C2", set(t for t, _ in calls) == {1, 3, 4, 5, 6}, "values authored: %s (2 and 7 never)" % sorted(set(t for t, _ in calls)))
check("C3", calls.get((1, "btlAtelSetUnitType")) == 59814 and "monster_00" in tops.get(1, "") and "unique_monster_00" in tops.get(1, ""),
      "type 1: the default for enemies (btlAtelSetUnitType(0), 59,814 calls; monster_NN, unique monsters, trial, lot)")
check("C4", "disp_tama01" in tops.get(3, "") and "THIRD_" in tops.get(3, ""), "type 3: allied third parties and event combatants (SD-160)")
check("C5", "system_crystal_actor" in tops.get(4, "") and "system_anchor_actor" in tops.get(4, ""),
      "type 4: system objects - save crystals, anchor actors, treasure chests, a corpse - plus a few monsters")
check("C6", "TWN_" in tops.get(5, "") and "PRISON_" in tops.get(5, ""), "type 5: town and prison NPCs (neither friend nor foe)")
check("C7", "BOSS_" in tops.get(6, "") and "STAY_" in tops.get(6, "") and calls.get((6, "setfreetargettype")) == 45,
      "type 6: stationary boss parts (45 calls: the Demon Wall, a boss weapon, Daedalus)")
print("FAILS %d" % fails)
