"""callee_pool.py [--max-callers 2] [--json OUT] - the frontier functions OPUS can explain as CALLEES on OPUS-led pages
(OPUS, 2026-10-03).

The F family's frontier splits three ways:
- entry-only: a page cites the function at its entry; that page's lead owns the work, f_pack packs it;
- SWE2-EC7's hub band: functions with >= 3 interior-cited (A) callers, `rank_hub29.py` batches;
- the rest: uncited functions with 1 or 2 A callers.

This tool lists the third group where at least one A caller is explained on an OPUS-led page. That page is the natural
home for an interior row ("callee of X"). It excludes UC-1 frontier bodies (no route yet, OPUS-REQ-FABLE-UC1-GAMECODE-
ROUTE-1003) and every function an open non-OPUS board task names. Output: per host page, the callee functions.
"""
import bisect
import collections
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA"))
KIT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
sys.path.insert(0, HERE)
import check_dispositions as CD  # noqa: E402
import uc1_band  # noqa: E402
import retool  # noqa: E402

LEAD_RE = re.compile(r"^(OPUS|FABLE|ASTRA|SWE2-[A-Z0-9]+|SWE2CONTRACT|SWE2FRONTIER|FRONTIER|Database)\b")


def lead_of(rel, cache={}):
    if rel not in cache:
        subj = subprocess.run(["git", "-C", DBR, "log", "--format=%s", "--", rel], capture_output=True, text=True).stdout
        c = collections.Counter(m.group(1) for s in subj.splitlines() for m in [LEAD_RE.match(s)] if m)
        cache[rel] = c.most_common(1)[0][0] if c else "-"
    return cache[rel]


def main():
    mx = int(sys.argv[sys.argv.index("--max-callers") + 1]) if "--max-callers" in sys.argv else 2
    sizes = CD.load_functions()
    r = CD.evaluate(DBR, sizes)
    explained = set(r["explained_set"])
    uc1f = uc1_band.frontier_starts() & set(sizes)
    entries = sorted(sizes)
    pages = collections.defaultdict(set)       # function -> pages citing it at an interior address
    cited = set()                              # any citation (entry or interior)
    for p in CD.docs(DBR):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(p, DBR).replace("\\", "/")
        for hx in CD.CITE.findall(t):
            v = int(hx, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i >= 0 and entries[i] <= v < entries[i] + sizes[entries[i]]:
                cited.add(entries[i])
                if v != entries[i] and CD._bearing(t):
                    pages[entries[i]].add(rel)
    board = json.load(open(os.path.join(DBR, "_index", "_inbox", "TEAM.json"), encoding="utf-8"))
    named = set()
    for t in board["tasks"]:
        if t.get("status") in ("READY", "ACTIVE", "BLOCKED") and "OPUS" not in str(t.get("agent") or t.get("assigned_to")):
            for hx in re.findall(r"\b([0-9A-F]{8})\b", json.dumps(t)):
                named.add(int(hx, 16))
    calls = retool.scan()["calls"]
    frontier = [a for a in sizes if a not in explained and a not in uc1f]
    pool = collections.defaultdict(list)
    stats = collections.Counter()
    for f in frontier:
        if f in cited:
            stats["cited somewhere (entry-only or text)"] += 1; continue
        if f in named:
            stats["named by an open non-OPUS task"] += 1; continue
        callers = {c for c, _site in calls.get(f, ())}
        acallers = sorted(c for c in callers if c in explained and pages.get(c))
        if not acallers:
            stats["no explained caller"] += 1; continue
        if len(acallers) > mx:
            stats["EC7 hub band (>%d A callers)" % mx] += 1; continue
        hosts = sorted({p for c in acallers for p in pages[c] if lead_of(p) == "OPUS"})
        if not hosts:
            stats["callers explained only on non-OPUS pages"] += 1; continue
        stats["POOL"] += 1
        pool[hosts[0]].append(("%08X" % f, sizes[f], ["%08X" % c for c in acallers]))
    for k, v in stats.most_common():
        print("%-45s %d" % (k, v))
    for p, fs in sorted(pool.items(), key=lambda kv: -len(kv[1])):
        print("%3d  %s" % (len(fs), p))
    if "--json" in sys.argv:
        json.dump(pool, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
