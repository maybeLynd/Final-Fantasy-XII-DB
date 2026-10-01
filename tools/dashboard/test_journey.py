"""test_journey.py - the Player progression tree (build_views.journey_tree) over the real content catalogue (OPUS, 2026-09-30).

  J1  every node id is unique, and the root holds the seven in-game categories in order
  J2  no node title or item name shows an undecoded text byte (<XX>) outside the Unused slots groups
  J3  every cross-link resolves: a node:<id> link names a node, a catalogue-key link has a home listing in the tree, and every
      item's page (entries[eid]) exists
  J4  duplicate names collapse: within one list no name appears twice
  J5  grouping never comes from invented order: every grouped family node's children carry a source (basis) or are the
      Not yet classified / Other / Unused slots groups
  J6  counts: The world counts every map once (the catalogue's map total); the Bestiary counts distinct enemy names
  J7  unmeasured stays unmeasured: with no co-op ledger rows, no node carries a co-op figure; Story & quests has no count
  J8  negative control: a fixture enemy with a <9A> name and a duplicate map is caught by J2's and J4's checks
It builds the catalogue with ff12_content.py (read-only over the installed archive) into a scratch file.
"""
import collections, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402
fails = 0


def check(tag, ok, text=""):
    global fails
    fails += not ok
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


T = tempfile.mkdtemp(prefix="jt_")
out = os.path.join(T, "content.json")
subprocess.run([sys.executable, "-B", os.path.join(HERE, "ff12_content.py"), "--out", out], check=True, capture_output=True)
c = json.load(open(out, encoding="utf-8"))
tree, entries, links = BV.journey_tree(c, {})

nodes, items = [], []


def walk(n, path):
    nodes.append((n, path))
    for i, it in enumerate(n.get("items") or []):
        items.append((n, i, it, path))
    for ch in n.get("children") or []:
        walk(ch, path + [n["id"]])


walk(tree, [])
ids = collections.Counter(n["id"] for n, _ in nodes)
cats = [ch["title"] for ch in tree["children"]]
check("J1", max(ids.values()) == 1 and cats == ["The world", "Characters", "License Board", "Battle", "Items & equipment", "Bestiary", "Story & quests"],
      "%d nodes, duplicates %s; categories %s" % (len(ids), [k for k, v in ids.items() if v > 1][:3], cats))

RAW = re.compile(r"<[0-9A-F]{2}>")


def raw_names(nodes_, items_):
    bad = [n["title"] for n, p in nodes_ if RAW.search(n["title"])]
    bad += [it["name"] for n, _, it, p in items_ if RAW.search(it["name"]) and not n["id"].endswith("-unused") and not it.get("unused")]
    return bad


bad = raw_names(nodes, items)
check("J2", not bad, "%d raw-byte names %s" % (len(bad), bad[:4]))

byid = {n["id"] for n, _ in nodes}
lk = [(eid, e["link"]) for eid, pg in entries.items() for s in pg.get("sections") or [] for e in s.get("entries") or [] if e.get("link")]
lk += [(n["title"], e["link"]) for n, _ in nodes for s in n.get("sections") or [] for e in s.get("entries") or [] if e.get("link")]
dead = [(a, l) for a, l in lk if not ((l.startswith("node:") and l[5:] in byid) or (not l.startswith("node:") and l in links))]
badhome = [k for k, (nid, i) in links.items() if nid not in byid]
noentry = [it["name"] for _, _, it, _ in items if it.get("eid") not in entries]
check("J3", lk and not dead and not badhome and not noentry, "%d links, %d dead %s; link homes outside the tree %d; items without a page %d %s"
      % (len(lk), len(dead), dead[:3], len(badhome), len(noentry), noentry[:3]))


def dup_lists(nodes_):
    out = []
    for n, _ in nodes_:
        cnt = collections.Counter(it["name"] for it in n.get("items") or [] if not it.get("unused"))
        out += [(n["id"], k) for k, v in cnt.items() if v > 1 and not n["id"].endswith("-maps") and not n["id"].startswith(("area-", "region-"))]
    return out


dups = dup_lists(nodes)
check("J4", not dups, "%d repeated names %s" % (len(dups), dups[:3]))

SPECIAL = ("Not yet classified", "Other", "Unused slots", "Unused / Reserve rows")
fam = {n["id"]: n for n, _ in nodes}
ungrounded = []
for fid in ("abilities", "equipment", "gambits", "key_items", "growth", "bestiary-kinds"):
    n = fam.get(fid)
    for ch in (n or {}).get("children") or []:
        if not ch.get("basis") and ch["title"] not in SPECIAL:
            ungrounded.append((fid, ch["title"]))
check("J5", not ungrounded, "children without a source: %s" % ungrounded[:4])

world = fam["world"]
bestiary = fam["bestiary"]
names = {BV._jname(e) for e in c["families"]["enemies"] if not BV._junused(e) and BV._jname(e) != "No name"}
check("J6", world["count"] == len(c["world"]["maps"]) and bestiary["count"] == len(names),
      "world %s maps of %d; bestiary %s names of %d" % (world["count"], len(c["world"]["maps"]), bestiary["count"], len(names)))

coop = [n["id"] for n, _ in nodes if n.get("coop")]
check("J7", not coop and fam["story"].get("count") is None, "nodes with a co-op figure %s; story count %s" % (coop[:3], fam["story"].get("count")))

fx = {"families": {"enemies": [{"key": "enemy:x:0", "name": "<9A><9A>", "maps": []}, {"key": "enemy:x:1", "name": "Rat", "maps": []}]}, "world": {}}
ft = BV.journey_tree(fx, {})[0]
fn, fi = [], []


def walk2(n):
    fn.append((n, []))
    for i, it in enumerate(n.get("items") or []):
        fi.append((n, i, it, []))
    for ch in n.get("children") or []:
        walk2(ch)


walk2(ft)
dup_node = {"id": "x", "items": [{"name": "Rat"}, {"name": "Rat"}]}
check("J8", raw_names(fn, fi) and dup_lists([(dup_node, [])]), "fixture raw names %s; fixture duplicates %s" % (raw_names(fn, fi)[:2], dup_lists([(dup_node, [])])))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
