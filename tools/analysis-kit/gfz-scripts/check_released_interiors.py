#!/usr/bin/env python3
"""Is a type that declares NO independent storage nonetheless reached by a destructor?

WHY, AND IT IS NOT HYPOTHETICAL. 62 game types carry a destructor cell of the form `none -
interior to X`, `none - no independent storage`, `none - storage is in the image`. Each is a
resolved negative and each rests on the same claim: this object is not released on its own.
On 2026-09-20 one of them was WRONG. ManagerSub7FB0Record's +0x000 was declared `Widget*` and
its release read as following that pointer; the code does `mov rcx, rbx` - the RECORD's own
address - into 00245020, twice, never loading a pointer. The record IS released at its own
base, and a ctype in the pointer graph said otherwise.

THE TEST USES THE STORE AGAINST ITSELF. Every declared destructor address in _types/types.tsv
is a known release. If one of them appears in the census of a type whose destructor cell says
that type has no independent storage, at displacement 0, then something releases that object at
its own base and the cell needs re-reading.

WHAT A HIT IS NOT. A destructor legitimately walks interiors: a parent's release touching a
child at the child's base is the parent freeing itself, and the child's cell may be right. What
the hit says is that the two claims - `no independent storage` and `a declared destructor runs
at this base` - have not been reconciled on the row, and one of them was wrong once.

CONTROLS, both required or the output is refused:
  * POSITIVE - Widget's destructor 00244F00 must be found on ManagerSub0209BE80_57E0 at base 0,
    the case that started this; its cell is not a no-storage one, so it is checked directly
    rather than through the report.
  * NEGATIVE - ImageAddressArenaRecord must not appear: nothing declared releases it.
"""
import collections
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import census_artifacts as CA  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")
NO_STORAGE = re.compile(r"no independent storage|interior to|inline in|storage is in the image|"
                        r"built on the caller|dies with the caller|caller-supplied|"
                        r"never released|no allocation of its own", re.I)
CONTROL_POS = ("ManagerSub0209BE80_57E0", "00244F00")
CONTROL_NEG = "ImageAddressArenaRecord"


def main():
    types = list(csv.DictReader(io.open(D + "types.tsv", encoding="utf-8"), delimiter="\t"))
    game = [r for r in types if r.get("category") != "22-Middleware-PhyreEngine"]

    # every destructor the store names, whoever owns it
    releases = {}
    for r in types:
        for a in ADDR.findall(r.get("dtor") or ""):
            releases.setdefault(a.upper(), set()).add(r["type"])
    nostore = {r["type"]: (r.get("dtor") or "") for r in game
               if not ADDR.search(r.get("dtor") or "") and NO_STORAGE.search(r.get("dtor") or "")}

    by_type, unresolved = CA.load()
    hits = collections.defaultdict(list)
    ctrl_pos = False
    for t, rows in by_type.items():
        for row in rows:
            fn = (row.get("function") or "").strip().upper()
            if fn not in releases:
                continue
            try:
                d = int(row["disp"], 16)
            except (ValueError, TypeError, KeyError):
                continue
            if d != 0:
                continue
            if t == CONTROL_POS[0] and fn == CONTROL_POS[1]:
                ctrl_pos = True
            if t in nostore:
                hits[t].append((fn, sorted(releases[fn]), row.get("site", ""),
                                (row.get("instruction") or "").strip()))

    ok_neg = CONTROL_NEG not in hits
    print("CONTROL positive  Widget's dtor 00244F00 on %s at base 0 -> %s   %s"
          % (CONTROL_POS[0], "found" if ctrl_pos else "absent",
             "PASS" if ctrl_pos else "FAIL"))
    print("CONTROL negative  %s -> %s   %s"
          % (CONTROL_NEG, "absent" if ok_neg else "REPORTED", "PASS" if ok_neg else "FAIL"))
    if not (ctrl_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  both controls pass - the absences below are meaningful")
    print("  " + CA.coverage_line(by_type, unresolved))
    searchable = sorted(t for t in nostore if t in by_type)
    print("  declared destructor addresses in the store: %d" % len(releases))
    print("  game types declaring no independent storage: %d, of which %d have a census and "
          "were searched" % (len(nostore), len(searchable)))
    print("  THE OTHER %d HAVE NO ARTIFACT AND WERE NOT TESTED AT ALL."
          % (len(nostore) - len(searchable)))
    print("  AND THIS SWEEP SEARCHES A TYPE'S OWN CENSUS, so it would NOT have caught the case")
    print("  that motivated it: ManagerSub7FB0Record has no artifact, and its release was found")
    print("  in the PARENT's census plus a read of 00296680..002966AA. A zero here is bounded")
    print("  by both facts and is not a statement about all the cells.\n")

    print("TYPES DECLARING NO INDEPENDENT STORAGE THAT A DECLARED DESTRUCTOR REACHES AT BASE 0:"
          " %d" % len(hits))
    for t in sorted(hits):
        print("\n  %s" % t)
        print("      cell: %s" % nostore[t][:110])
        seen = set()
        for fn, owners, site, instr in hits[t]:
            if (fn, site) in seen:
                continue
            seen.add((fn, site))
            print("      %s (declared destructor of %s) at %s  %s"
                  % (fn, ", ".join(owners), site, instr[:60]))
    print("\nA hit is a question, not a defect: a parent's release legitimately touches a child")
    print("at the child's base. What it says is that two claims on one row - `no independent")
    print("storage` and `a declared destructor runs here` - have not been reconciled.")


if __name__ == "__main__":
    sys.exit(main() or 0)
