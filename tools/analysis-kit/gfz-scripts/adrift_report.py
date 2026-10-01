"""adrift_report.py - which declared function families check_dispositions REFUSES because members became A, and which
evidence-bearing page's interior citation made each member A (OPUS, 2026-09-30).

  python -B adrift_report.py [--db "FFXII TZA"]

A family row is refused whole when one member is measured A (an evidence-bearing page - status DOCUMENTED/AUDITED or
readiness at BEHAVIORALLY UNDERSTOOD or above - cites an address strictly inside that member's body); every other member
then falls back to the frontier. That happens after every re-status to DOCUMENTED ("A-drift"). The cure is exact:
remove the A members from the row's members file (or re-run the family's selector, which excludes A by design) and set
the declared count to match. This report names, per refused row, the A members, the pages and interior addresses that
made them A, the members file, and the selector the row's note names, so the repair needs no diagnosis.
Reads only. Uses check_dispositions' own functions, so it cannot disagree with the gate about what is A.
"""
import argparse, bisect, io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_dispositions as CD  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="FFXII TZA")
    a = ap.parse_args()
    db = a.db
    sizes = CD.load_functions()
    if isinstance(sizes, tuple):
        sizes = sizes[0]
    entries = sorted(sizes)
    a_set = CD.measure_a(db, sizes)[0]
    # who made each A member A: evidence-bearing pages citing inside the body
    why = {}
    for p in CD.docs(db):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        if not CD._bearing(t):
            continue
        for h in CD.CITE.findall(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if e < v < e + sizes[e] and e in a_set:
                why.setdefault(e, set()).add((os.path.relpath(p, db).replace("\\", "/"), "%08X" % v))
    n = 0
    for doc, parts in CD.parse_families(db):
        if len(parts) < 5:
            continue
        name, letter, rel, count = parts[0], parts[1], parts[2], parts[3]
        try:
            members = CD.read_members(doc, rel)
        except Exception:
            continue
        hit = [m for m in members if m in a_set]
        if not hit:
            continue
        n += 1
        note = "|".join(parts[4:])
        sel = re.search(r"\(([\w/.-]*select_[\w-]+\.py)\)", note)
        print("REFUSED  %s :: %s  [%s, declared %s, %d member(s) A]" % (os.path.relpath(doc, db).replace("\\", "/"), name.strip()[:60],
                                                                     letter, count.strip(), len(hit)))
        print("   members file: %s%s" % (rel.strip(), ("   selector: " + sel.group(1)) if sel else "   (no selector named: exact A removal)"))
        for m in hit:
            src = sorted(why.get(m, ()))
            print("   %08X  A via %s" % (m, "; ".join("%s @%s" % s for s in src[:3]) + (" (+%d)" % (len(src) - 3) if len(src) > 3 else "")))
    print("refused rows with A members: %d" % n)


if __name__ == "__main__":
    main()
