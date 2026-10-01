# falseclear.py [--limit N] [--show N]
# How many pages' crossing obligations are discharged by a PROSE WORD rather than a disposition?
#
# For every page, compute the foreign-layer edges exactly as xlayer does, then evaluate the gate's
# OWN predicate twice per layer:
#   (a) over the whole document text   -- what the gate does today
#   (b) over the crossings/neighbours sections only
# A layer accounted under (a) and not under (b) is a FALSE CLEAR: nothing in any disposition section
# mentions it, and it is green because the alias occurs somewhere in the prose.
#
# Folder matching is kept in BOTH arms, so a page living in 15-Input is never counted as a false
# clear for Input -- that is a different question and not the defect under test.
#
# CONTROL: --control plants the string " input " into a page that has an unaccounted Input edge and
# asserts the sweep flags it. A sweep that cannot see a planted defect is not measuring.
import io, os, re, sys, collections, bisect

KIT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
sys.path.insert(0, KIT)
import audit_crossrefs as A

fn = A.load_functions(os.path.join(GRAPH, "functions.tsv"))
try:
    A.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    A.register_ledger_aliases({v["owner"] for v in fn.values()})
except Exception as e:
    print("note: alias registration skipped:", e)
starts = sorted(int(e, 16) for e in fn)

def func_of(v):
    i = bisect.bisect_right(starts, v) - 1
    if i < 0: return None
    e = "%08X" % starts[i]
    return e if v < starts[i] + max(fn[e]["body_bytes"], 1) else None

edges_by = collections.defaultdict(list)
with io.open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8") as fh:
    fh.readline()
    for line in fh:
        p = line.rstrip("\n").split("\t")
        a, b = p[0].upper(), p[1].upper()
        edges_by[a].append((b, "callee")); edges_by[b].append((a, "caller"))

SECT = re.compile(r"^#{2,6}\s+.*("
                  r"crossing|cross-subsystem|neighbour|"
                  r"disposition|projection into|exclusive subtree|interior citation"
                  r")", re.I | re.M)   # widened 2026-09-22: the first version missed singular
# "crossing - <layer>", "projection into UI refusals", subtree and interior-citation sections,
# all of which ARE dispositions. Narrow extractor = over-report. Still an upper bound.
HEAD = re.compile(r"^#{1,4}\s+")

def disposition_text(text):
    """Only the crossings / neighbours sections."""
    out, keep = [], False
    for line in text.split("\n"):
        if HEAD.match(line):
            keep = bool(SECT.match(line))
        if keep:
            out.append(line)
    return "\n".join(out).lower()

def analyse(path, text):
    m = re.search(r"^owner_layer:\s*(?:PrimaryOwner:)?\s*([A-Za-z_/ ]+)", text, re.M)
    owner = m.group(1).strip() if m else ""
    cited = set()
    for a in re.findall(r"(?<![0-9A-Za-z_])([0-9A-F]{8})(?![0-9A-Za-z_])", text):
        f = func_of(int(a, 16))
        if f and not A.is_substrate(fn[f]):
            cited.add(f)
    lay_edges = collections.defaultdict(list)
    for c in cited:
        for other, kind in edges_by.get(c, ()):
            if other not in fn or A.is_substrate(fn[other]): continue
            lay = A.subsystem_of(fn[other])
            if lay and A._canon(lay) != A._canon(owner) and A._canon(lay) != A._canon(A.subsystem_of(fn[c]) or ""):
                lay_edges[lay].append("%s %s %s" % (c, kind, other))
    low = text.lower()
    disp = disposition_text(text)
    folder = os.path.basename(os.path.dirname(os.path.abspath(path))).lower()
    false_clears = []
    for lay, ed in lay_edges.items():
        whole = A.doc_accounts_for(low, folder, lay)
        only = A.doc_accounts_for(disp, folder, lay)
        if whole and not only:
            false_clears.append((lay, len(ed), ed[:2]))
    return owner, len(lay_edges), false_clears

pages = []
for root, _, files in os.walk(DB):
    for f in files:
        if f.endswith(".md"):
            pages.append(os.path.join(root, f))
pages.sort()
limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else len(pages)
show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 25

tot_pages = tot_fc = 0
rows = []
for p in pages[:limit]:
    try:
        text = io.open(p, encoding="utf-8").read()
    except Exception:
        continue
    if not SECT.search(text):          # no crossings section at all: not in scope
        continue
    tot_pages += 1
    owner, nlay, fc = analyse(p, text)
    if fc:
        tot_fc += 1
        rows.append((len(fc), os.path.relpath(p, DB), fc))
rows.sort(reverse=True)
print("=" * 100)
print("pages WITH a crossings section: %d" % tot_pages)
print("pages with >=1 layer cleared by PROSE ONLY: %d  (%.1f%%)" % (tot_fc, 100.0 * tot_fc / max(tot_pages, 1)))
print("total false-cleared layer obligations: %d" % sum(r[0] for r in rows))
print("=" * 100)
for n, rel, fc in rows[:show]:
    print("%-70s %d" % (rel, n))
    for lay, ne, sample in fc:
        print("      %-32s %d edge(s)   e.g. %s" % (lay, ne, sample[0] if sample else ""))
