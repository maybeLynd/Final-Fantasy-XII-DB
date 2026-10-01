"""Assign every rebuilt edge of the three grouped pairs to exactly one far-end group and print counts.

A group is a set of far-end functions (the `other` column). Every edge must land in exactly one group;
the script fails loudly otherwise, so the counts in the drafts are copied from here, not added by hand.
"""
import io, json, sys, collections

d = json.load(io.open(r"C:/x/p22/drafts/tools/edges_full.json", encoding="utf-8"))

GROUPS = {
 "04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md|CombatFormula": [
  ("F1 stats->unit lookup 0031B860", {"0031B860"}),
  ("F2 other stats<->unit lookups", {"0031E800", "00320A40", "00320A70", "00320AB0"}),
  ("F3 stats record writers and rebuild", {"0023AC80", "002F8E50", "002F9180", "002FEF30", "00300520",
       "00300530", "00300BC0", "00300C90", "00300CE0", "0030F340"}),
  ("F4 result evaluation / resolution / application", {"002FEE20", "0030DAE0", "00308B90", "003112F0",
       "003847C0", "003848E0", "003849B0", "00385680", "00385BA0", "00385E50", "00385F60", "00386A50",
       "00386A70", "00386AE0", "00390AB0", "00469EC0", "00384E50"}),
  ("F5 runtime action-id / persistent state", {"00386C10", "00387090", "00387A50", "00387B00"}),
  ("F6 table-dispatched roll and recipe bodies", {"00387FD0", "003884F0", "00388660", "00388320",
       "00388D50", "00389370", "003896B0", "00389820", "00389950", "00389C60", "0038B150", "0038B220",
       "0038BC00", "0038D400", "0038DA00", "0038EBE0", "0038ED40", "00390390", "00390680"}),
  ("F7 per-unit scan 00384F40", {"00384F40"}),
 ],
 "04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md|Items_Equipment_Shops_License": [
  ("I1 equipment-slot writers", {"0031A300", "0031A410", "0031A510", "0031A630", "0031A710"}),
  ("I2 license writer and checks", {"00323910", "00323EC0", "00323C60", "00323D10", "00323BB0", "00324020"}),
  ("I3 gil movers", {"002FD530", "002FD880", "002FEEB0", "00310870"}),
  ("I4 inventory and equipment snapshot", {"003008A0", "00309FB0", "0030FAA0", "0030FBE0", "0030FD10", "00325F40"}),
  ("I5 loadout evaluation and compatibility", {"0030A4E0", "00309480", "003231F0", "002F9F20", "003096F0", "00317930"}),
  ("I6 class-D (bazaar) id flags", {"0030B180", "0030B4B0", "0030B510", "0030B570", "0030B630"}),
 ],
 "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md|Script_VM_Native_Bridge": None,
}

ok = True
for key, groups in GROUPS.items():
    rows = d[key]
    print("=== %s: %d edges, %d distinct far ends" % (key, len(rows), len({r["other"] for r in rows})))
    if groups is None:   # group by the page-side (cited) accessor: every far end is a verb handler
        c = collections.Counter(r["cited"] for r in rows)
        for k, v in c.most_common():
            far = sorted({r["other"] for r in rows if r["cited"] == k})
            print("  %-10s %3d edges, %d far ends" % (k, v, len(far)))
        print("  sum %d" % sum(c.values()))
        continue
    seen = collections.Counter()
    tot = 0
    for name, fars in groups:
        es = [r for r in rows if r["other"] in fars]
        dirs = collections.Counter(r["direction"] for r in es)
        cited = collections.Counter(r["cited"] for r in es)
        tot += len(es)
        for r in es:
            seen[(r["cited"], r["direction"], r["other"])] += 1
        print("  %-48s %3d edges  (%s)  far ends %d  page-side %d" % (
            name, len(es), ", ".join("%s %d" % kv for kv in sorted(dirs.items())), len({r['other'] for r in es}), len(cited)))
    missing = [r for r in rows if (r["cited"], r["direction"], r["other"]) not in seen]
    dup = [k for k, v in seen.items() if v > 1]
    print("  sum %d of %d; unassigned %d; double-assigned %d" % (tot, len(rows), len(missing), len(dup)))
    for r in missing:
        print("    UNASSIGNED", r["cited"], r["direction"], r["other"], r["other_name"])
    ok &= (tot == len(rows) and not missing and not dup)
print("GROUP CONTROL:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
