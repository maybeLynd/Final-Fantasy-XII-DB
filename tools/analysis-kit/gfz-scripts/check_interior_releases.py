#!/usr/bin/env python3
"""Which declared destructors run at a PARENT's interior offset, and what lives there?

THE TEST THE OTHER ONE COULD NOT DO. check_released_interiors.py asks whether a type's own
census shows a declared destructor at its base. That misses the case that motivated it:
ManagerSub7FB0Record has no census of its own, and the release that takes its address
(`mov rcx, rbx` into 00245020) is visible only in the PARENT's census, as an access at the
parent's interior offset.

So invert it. Walk every census for rows whose function is a destructor the store declares -
245 addresses - at a NON-ZERO displacement. Each is a release operating somewhere inside a
parent. Then ask what the store says lives at that offset:

  * a declared EMBED child at exactly that offset -> the child is released at its own base,
    and if the child's own destructor cell claims no independent storage the two disagree;
  * no declared child -> a release runs at an offset the layout does not name, which is
    either an undeclared sub-object or a parent freeing its own member.

WHAT A HIT IS NOT. A destructor walking its own object's fields produces exactly this shape
when the field IS the thing being freed - a pointer member released by its owner. The
discriminator is whether the access takes the ADDRESS of the offset (`lea`, or a base handed
straight on) or LOADS from it; this tool reports the row's kind so the reader can tell, and
does not decide.

CONTROLS, both required or the output is refused:
  * POSITIVE - Widget's destructor 00244F00 must be found inside ManagerSub0209BE80_8FA0 at
    +0xAC0 and inside ManagerSub0209BE80_AB30 at +0xC0, the two embedded widgets already
    established by find_embedded_widgets.py.
  * NEGATIVE - no hit may be reported at displacement 0; that is the other tool's question and
    overlap would double-count.
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
EMBED = re.compile(r"EMBED\s+(\w+)\s*\+\s*0x([0-9A-Fa-f]+)")
NO_STORAGE = re.compile(r"no independent storage|interior to|inline in|storage is in the image|"
                        r"built on the caller|dies with the caller|never released", re.I)
CONTROLS = [("ManagerSub0209BE80_8FA0", 0xAC0, "00244F00"),
            ("ManagerSub0209BE80_AB30", 0xC0, "00244F00")]


def main():
    types = list(csv.DictReader(io.open(D + "types.tsv", encoding="utf-8"), delimiter="\t"))
    # AN ADDRESS IN A `none -` CELL IS NOT A DESTRUCTOR, and scraping every address out of the
    # column made this tool report one. VmResultEntry's cell reads `none - interior to
    # ActorStorageRecord, whose +0xA8 is an interior pointer planted by the region map
    # 00266AD0`, so 00266AD0 entered the release set and its `lea r8, [rdx + 0x120]` was
    # reported as a destructor taking MovementContext's address. It plants interior pointers;
    # it frees nothing. A cell that opens by declaring there is no destructor contributes no
    # destructor, whatever else it mentions.
    DECLARES_NONE = re.compile(r"^\s*(none|no destructor|not established|unresolved)", re.I)
    releases = {}
    for r in types:
        cell = r.get("dtor") or ""
        if DECLARES_NONE.match(cell):
            continue
        for a in ADDR.findall(cell):
            releases.setdefault(a.upper(), set()).add(r["type"])
    # what the store declares at (parent, offset)
    child_at = {}
    dtor_cell = {}
    for r in types:
        dtor_cell[r["type"]] = r.get("dtor") or ""
        for alt in (r.get("route") or "").split("|"):
            m = EMBED.search(alt)
            if m:
                child_at[(m.group(1), int(m.group(2), 16))] = r["type"]

    by_type, unresolved = CA.load()
    hits = collections.defaultdict(list)
    for t, rows in by_type.items():
        for row in rows:
            fn = (row.get("function") or "").strip().upper()
            if fn not in releases:
                continue
            try:
                d = int(row["disp"], 16)
            except (ValueError, TypeError, KeyError):
                continue
            if d == 0:
                continue
            hits[(t, d)].append((fn, row.get("kind", ""), row.get("site", ""),
                                 (row.get("instruction") or "").strip()))

    got = {(t, d, fn) for (t, d), v in hits.items() for fn, _k, _s, _i in v}
    ok_pos = all((c[0], c[1], c[2]) in got for c in CONTROLS)
    ok_neg = all(d != 0 for (_t, d) in hits)
    for c in CONTROLS:
        print("CONTROL positive  %s +0x%X <- %s   %s"
              % (c[0], c[1], c[2], "PASS" if (c[0], c[1], c[2]) in got else "FAIL"))
    print("CONTROL negative  nothing reported at displacement 0   %s"
          % ("PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  controls pass - the absences below are meaningful")
    print("  " + CA.coverage_line(by_type, unresolved))
    print("  declared destructor addresses: %d\n" % len(releases))

    named, unnamed = [], []
    for (t, d), v in sorted(hits.items()):
        child = child_at.get((t, d))
        (named if child else unnamed).append((t, d, child, v))

    print("A DECLARED DESTRUCTOR RUNS AT A PARENT'S INTERIOR OFFSET: %d site group(s)"
          % (len(named) + len(unnamed)))
    print("\n== the offset holds a DECLARED child: %d" % len(named))
    for t, d, child, v in named:
        flag = " <== and its own dtor cell claims no independent storage" \
            if NO_STORAGE.search(dtor_cell.get(child, "")) and \
            not ADDR.search(dtor_cell.get(child, "")) else ""
        print("   %-30s +0x%-5X -> %s%s" % (t, d, child, flag))
        for fn, kind, site, instr in v[:2]:
            print("        %s %-4s %s  %s" % (fn, kind, site, instr[:56]))
    print("\n== no declared child at that offset: %d" % len(unnamed))
    for t, d, _c, v in unnamed[:20]:
        fn, kind, site, instr = v[0]
        print("   %-30s +0x%-5X  %s %-4s %s  %s" % (t, d, fn, kind, site, instr[:46]))
    if len(unnamed) > 20:
        print("   ... %d more" % (len(unnamed) - 20))
    print("\nA hit is a question. A destructor freeing its own pointer member produces this")
    print("shape legitimately; the `kind` column says whether the offset's ADDRESS was taken")
    print("or its VALUE loaded, and that is what distinguishes the two.")


if __name__ == "__main__":
    sys.exit(main() or 0)
