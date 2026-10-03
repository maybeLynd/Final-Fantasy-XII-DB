"""scope_guard.py PAGE... [--fns ADDR,ADDR...] [--json] - may a cloud session work on these database pages without duplicating
anyone? (OPUS, 2026-10-01)

PAGE is relative to 'FFXII TZA/' (e.g. 16-UI/the-selection-the-menu-publishes.md). Verdicts per page:
  BLOCK  an open board task (READY/ACTIVE/BLOCKED/...) not owned by OPUS names the page; the page is dirty (uncommitted
         edits by any lane); the page is an overlay carrier (FRONTIER-applied); a non-OPUS commit touched it in the last
         24 h (another lane is working there); an open non-OPUS board task names one of --fns (function addresses).
  WARN   a non-OPUS commit touched it 24-72 h ago (usually a sweep; read it); another identity's inbox (FABLE, ASTRA, ASTRA-QUEUE, SWE2-* / Devin lanes) mentions the page; OPUS reads the
         mention before launching.
  CLEAR  none of the above.
Exit status 0 only when every page is CLEAR or WARN. Run it immediately before every launch and again before ingesting
the result (a lane may have started in between)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402

SWEEP_RE = re.compile(r"contradictions from the cloud readiness map settled|held readiness edits released"
                      r"|counts and stale items settled|consolidated publish: progress-report cluster", re.I)

_BREADTH = {}


def _breadth(sha):
    """How many .md pages a commit touched (cached)."""
    if sha not in _BREADTH:
        import subprocess
        out = subprocess.run(["git", "-C", cl.DB, "show", "--name-only", "--format=", sha], capture_output=True,
                             text=True).stdout
        _BREADTH[sha] = sum(1 for l in out.splitlines() if l.endswith(".md"))
    return _BREADTH[sha]


args = sys.argv[1:]
fns = []
if "--fns" in args:
    k = args.index("--fns"); fns = [x.upper() for x in args[k + 1].split(",") if x]; args = args[:k] + args[k + 2:]
as_json = "--json" in args
pages = [a for a in args if not a.startswith("--")]
open_tasks = [t for t in cl.tasks() if str(t.get("status", "")).upper() in cl.OPEN]
dirty = cl.dirty_paths()
census = cl.carriers()
res, bad = [], 0
for p in pages:
    rel = p.replace("\\", "/")
    base = os.path.basename(rel)
    stem = base[:-3] if base.endswith(".md") else base
    reasons, warns = [], []
    if not os.path.isfile(os.path.join(cl.DB, rel)):
        reasons.append("no such page")
    for t in open_tasks:
        s = json.dumps(t, ensure_ascii=False)
        # 2026-10-03: OPUS's own review requests (a reviewer reads rows, it does not edit the page) do not block OPUS
        if str(t.get("requester", "")).upper() == "OPUS" and t.get("scope") == "review":
            continue
        if stem in s and "OPUS" not in cl.owner(t).upper():
            reasons.append("board %s %s (%s)" % (t.get("id"), t.get("status"), cl.owner(t)))
    for t in open_tasks:
        if "OPUS" in cl.owner(t).upper():
            continue
        s2 = json.dumps(t, ensure_ascii=False).upper()
        hit = [f for f in fns if f in s2]
        if hit:
            reasons.append("board %s %s (%s) names %s" % (t.get("id"), t.get("status"), cl.owner(t), ",".join(hit[:4])))
    if ("FFXII TZA/" + rel) in dirty:
        reasons.append("dirty in the working tree")
    if base in census:
        reasons.append("overlay carrier (census)")
    peers = cl.recent_peer_commits("FFXII TZA/" + rel, 24)
    if os.environ.get("OPUS_SWEEPS_OK") == "1":
        # FABLE's --sweeps-ok rule (fable_fpack.py SWEEP_RE, 2026-10-02), mirrored: a finished one-shot sweep that does
        # not mention interior work does not block. Claims, dirty pages and every other peer commit still block.
        # 2026-10-03 (OPUS): also by BREADTH, not only by subject - a finished peer commit that touched 15 or more pages
        # is a mass sweep (front-matter key retirement, readiness batches), not work on this page. Subject patterns
        # missed five such sweeps (19-110 pages each) and blocked every OPUS-led page they touched.
        peers = [x for x in peers if not ((SWEEP_RE.search(x) or _breadth(x.split("\t")[0]) >= 15)
                                          and "interior" not in x.lower())]
    if peers and os.environ.get("OPUS_ACTIVE_ONLY") == "1":
        # 2026-10-03, the user's rule: a recent peer commit is FINISHED work, not someone actively working here. Only
        # an open board claim, uncommitted edits (dirty) or an overlay carrier block; this becomes a WARN, and the
        # page's lead gets a notice naming what OPUS added so nothing is repeated.
        warns.append("peer commits <24h (finished work; notify the page lead after publishing): %s"
                     % "; ".join(x[:110] for x in peers[:3]))
    elif peers:
        reasons.append("peer commits <24h: %s" % "; ".join(x[:110] for x in peers[:3]))
    else:
        older = cl.recent_peer_commits("FFXII TZA/" + rel, 72)
        if older:
            warns.append("peer commits 24-72h: %s" % "; ".join(x[:110] for x in older[:2]))
    mi = cl.inbox_mentions(stem)
    if mi:
        warns.append("inbox mentions: " + ", ".join(sorted(mi)))
    v = "BLOCK" if reasons else ("WARN" if warns else "CLEAR")
    bad += v == "BLOCK"
    res.append({"page": rel, "verdict": v, "reasons": reasons, "warnings": warns})
if as_json:
    print(json.dumps(res, indent=1))
else:
    for r in res:
        print("%-5s %s" % (r["verdict"], r["page"]))
        for x in r["reasons"] + r["warnings"]:
            print("      - " + x)
    print("GUARD %d page(s): %d BLOCK" % (len(res), bad))
sys.exit(1 if bad else 0)
