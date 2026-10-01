"""SWE2-AUDIT-SEM: every removed member vs the A set measured NOW (check_dispositions.measure_a over the current tree),
the false entry vs the census, the 23 cascade returns vs A and every members file, and the SEAD arithmetic."""
import sys, os, collections, subprocess
G = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
sys.path.insert(0, G); sys.path.insert(0, os.path.join(DB, "18-Audio", "members"))
import check_dispositions as cd, uc1_band
sizes = cd.load_functions()
a_set = cd.measure_a(DB, sizes)[0]
uc1 = uc1_band.frontier_starts()
print("census entries", len(sizes), "A now", len(a_set), "UC-1 frontier bodies", len(uc1))
R = os.path.join(DB, "_index", "candidates", "ec7-refused-family-repair-0929", "removed-members.tsv")
rows = [l.rstrip("\r\n").split("\t") for l in open(R, encoding="utf-8")][1:]
by = collections.Counter(r[4] for r in rows)
print("removed rows by reason:", dict(by))
for reason in by:
    addrs = [int(r[3], 16) for r in rows if r[4] == reason]
    inA = sum(a in a_set for a in addrs); inc = sum(a in sizes for a in addrs); inU = sum(a in uc1 for a in addrs)
    print("  %-40s n=%3d  A-now %3d  in census %3d  UC-1 frontier %d" % (reason[:40], len(addrs), inA, inc, inU))
    if reason != "A-measured":
        for a in addrs:
            print("     %08X A=%s census=%s uc1=%s" % (a, a in a_set, a in sizes, a in uc1))
# SEAD arithmetic at the parent commit
old = subprocess.run(["git", "-C", DB, "show", "839236205^:Database/FFXII TZA/18-Audio/members/sead-library-span.tsv"],
                     capture_output=True, text=True).stdout
oldm = {int(l.split()[0], 16) for l in old.splitlines() if l.strip() and not l.startswith("#")}
new = {int(l.split()[0], 16) for l in open(os.path.join(DB, "18-Audio", "members", "sead-library-span.tsv")) if l.strip() and not l.startswith("#")}
sr = {int(r[3], 16): r[4] for r in rows if "sead" in r[2]}
print("SEAD old %d new %d; old-new %d; new-old %d; removed-list %d; old-new == removed-list: %s"
      % (len(oldm), len(new), len(oldm - new), len(new - oldm), len(sr), (oldm - new) == set(sr)))
