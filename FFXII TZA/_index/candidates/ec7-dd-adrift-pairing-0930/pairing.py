"""pairing.py KIT HEAD_DB BASE_DB BASE_REV - pair every A member of an A-refused row with the DD change that made it A.
For each A member: the evidence-bearing pages at HEAD citing inside it; for each, whether at BASE the page was
bearing and the cite present, and the first commit after BASE_REV that made the page bearing (status change) or added
the cite. Reads only."""
import bisect, collections, io, os, subprocess, sys

KIT, DB, BASE, BREV = sys.argv[1:5]
sys.path.insert(0, KIT)
import check_dispositions as CD  # noqa
R = "C:/Users/Kristian/source/repos/XIIOnline"
sizes = CD.load_functions()
entries = sorted(sizes)
r = CD.evaluate(DB, sizes)
a_set = CD.measure_a(DB, sizes)[0]
refused_A = {w for w, why in r["refusals"] if "already measured as A" in why}


def git(*a):
    return subprocess.run(["git", "-C", R] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def bearing_at(rev, rel):
    t = git("show", "%s:Database/FFXII TZA/%s" % (rev, rel))
    return (CD._bearing(t) if t else None), t


def flip_commit(rel, cite):
    revs = git("log", "--reverse", "--format=%h", "%s..HEAD" % BREV, "--", "Database/FFXII TZA/" + rel).split()
    for c in revs:
        b, t = bearing_at(c, rel)
        if b and cite in t:
            s = git("log", "-1", "--format=%an|%s", c).strip()
            return c, s
    return None, None


rows = CD.parse_families(DB)
out = []
for doc, parts in rows:
    if len(parts) < 5:
        continue
    who = "%s :: %s" % (os.path.basename(doc), parts[0])
    if who not in refused_A:
        continue
    mem = CD.read_members(doc, parts[2])
    for m in mem:
        if m not in a_set:
            continue
        cites = []
        for p in CD.docs(DB):
            t = io.open(p, encoding="utf-8", errors="replace").read()
            if not CD._bearing(t):
                continue
            for h in set(CD.CITE.findall(t)):
                v = int(h, 16)
                if m < v < m + sizes[m]:
                    cites.append((os.path.relpath(p, DB).replace("\\", "/"), "%08X" % v))
        pages = collections.OrderedDict()
        for rel, c in sorted(cites):
            pages.setdefault(rel, c)
        for rel, c in pages.items():
            b0, t0 = bearing_at(BREV, rel)
            cause = ("page re-statused to evidence-bearing" if (not b0 and t0 and c in t0) else
                     "interior cite added on a bearing page" if (b0 and c not in t0) else
                     "page new since base" if not t0 else
                     "re-status + new cite" if (not b0) else "already bearing and cited at base (?)")
            fc, fs = flip_commit(rel, c)
            out.append((parts[0], "%08X" % m, rel, c, cause, fc or "-", (fs or "")[:110]))
for o in out:
    print("\t".join(o))
