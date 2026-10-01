# census_rederive.py — SWE2-DATA 2026-09-27. Disposition control for
# FRONTIER-RT-DATA-CENSUS-REDERIVE (rows AC-6, BO-2, UQ-377).
#
# Compares Database/Tools/work/graph/functions.tsv (the 2026-09-27 dump)
# against graph_gn/functions.tsv (the 2026-09-02 baseline) cell-by-cell,
# audits every database consumer for dependence on the changed cells,
# and recomputes the unlisted-block census under both dumps.
#
# Run from the repository root:
#   python "Database/FFXII TZA/_index/candidates/census-rederive-2026-09-27/census_rederive.py"
#
# checks:
#   C1 dump diff is confined to comment_len (158), body_bytes (1), tags (176 rows)
#   C2 no consumer reads comment_len; no consumer names the changed body_bytes row
#   C3 every changed tag sits in the GFZ.V121.CodeDomain.* namespace (a retag pass)
#   C4 the block splitter reconstructs the published census shape (superset relation)
#   C5 the fresh dump's residue differs only at 0057FE80's trailing block
#   C6 tag-prefix selectors in census consumers are enumerated (BO-2 sweep)

import os, re, struct, sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
DB   = os.path.join(ROOT, "Database", "FFXII TZA")
NEW  = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
OLD  = os.path.join(ROOT, "Database", "Tools", "work", "graph_gn", "functions.tsv")
EXE  = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
PUB  = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code", "unlisted-code-blocks.tsv")

fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("  " + str(detail) if detail else ""))
    if not ok: fails.append(name)

def load(path):
    rows = {}
    for l in open(path, encoding="utf-8", errors="replace"):
        f = l.rstrip("\n").split("\t")
        if len(f) > 8 and f[0] != "entry":
            rows[f[0]] = f
    return rows

ka, kb = load(NEW), load(OLD)
print("rows: new=%d old=%d" % (len(ka), len(kb)))

# --- C1: cell-level delta -------------------------------------------------
addr_new = set(ka) - set(kb)
addr_old = set(kb) - set(ka)
coldiff = Counter()
changed_rows = set()
added_tags, removed_tags = set(), set()
comment_len_rows, body_bytes_rows = set(), set()
for k in ka:
    if k not in kb: continue
    ca, cb = ka[k], [c.rstrip("\r") for c in kb[k]]
    for i in range(min(len(ca), len(cb))):
        if ca[i] != cb[i]:
            coldiff[i] += 1
            changed_rows.add(k)
            if i == 7: comment_len_rows.add(k)
            if i == 2: body_bytes_rows.add(k)
    ta = set(ca[8].split(";")) - {""}
    tb = set(cb[8].split(";")) - {""}
    added_tags |= ta - tb
    removed_tags |= tb - ta
check("C1a identical address sets", not addr_new and not addr_old,
      "new-only=%d old-only=%d" % (len(addr_new), len(addr_old)))
check("C1b delta confined to comment_len(158)/body_bytes(1)/tags(177 rows)",
      len(comment_len_rows) == 158 and body_bytes_rows == {"0057FE80"}
      and len(changed_rows) == 177 and set(coldiff) <= {2, 7, 8},
      "comment_len=%d body_bytes=%s changed_rows=%d coldiff=%s"
      % (len(comment_len_rows), sorted(body_bytes_rows), len(changed_rows), dict(coldiff)))

# --- C2: consumer dependence on changed cells ------------------------------
files = []
for root, dirs, names in os.walk(DB):
    for n in names:
        if n.endswith(".py"):
            p = os.path.join(root, n)
            try:
                if "functions.tsv" in open(p, encoding="utf-8", errors="replace").read():
                    files.append(p)
            except OSError:
                pass
SELF = os.path.abspath(__file__)
comment_users = [f for f in files if f != SELF and
                 "comment_len" in open(f, encoding="utf-8", errors="replace").read()]
addr_users = [f for f in files if f != SELF and
              "0057FE80" in open(f, encoding="utf-8", errors="replace").read().upper()]
check("C2a no consumer reads comment_len", not comment_users, comment_users[:3])
check("C2b no consumer names 0057FE80", not addr_users, addr_users[:3])
print("consumers of functions.tsv:", len(files))

# --- C3: all changed tags live in GFZ.V121.CodeDomain.* --------------------
bad = [t for t in added_tags | removed_tags if not t.startswith("GFZ.V121.CodeDomain.")]
check("C3 every changed tag is a CodeDomain retag", not bad, bad[:5])

# tag-prefix selectors that intersect the delta
def selector_literals(src):
    lits = set()
    for m in re.finditer(r'"([A-Za-z][\w.]{2,80})"\s+in\s+(?:tags?|tg)\b', src): lits.add(m.group(1))
    for m in re.finditer(r"'([A-Za-z][\w.]{2,80})'\s+in\s+(?:tags?|tg)\b", src): lits.add(m.group(1))
    return lits
changed = added_tags | removed_tags
tag_hits = {}
for f in files:
    src = open(f, encoding="utf-8", errors="replace").read()
    lits = selector_literals(src)
    hit = [l for l in lits if any(l in t or t in l for t in changed)]
    if hit: tag_hits[f] = hit
print("selectors intersecting changed tags:", {os.path.basename(k): v for k, v in tag_hits.items()})

# --- C4/C5: unlisted-block recount ------------------------------------------
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    if d[o:o + 8].rstrip(b"\0") == b".text":
        vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
TVA = 0x120000 + va
def off(v): return ro + v - TVA if TVA <= v < TVA + min(vs, rs) else None
NOPB = {0x00, 0x0F, 0x1F, 0x40, 0x44, 0x66, 0x80, 0x84, 0x90, 0xCC}

def bodies(rows):
    return sorted((int(k, 16), int(v[2])) for k, v in rows.items())

def split(listed):
    """published rule: gap = bytes between listed bodies; strip 0xCC edges;
    an int3 run splits the residue iff it ends at a 16-aligned address;
    a segment made of pure alignment padding (int3/00/nop encodings) is not a block."""
    blocks = []
    end = listed[0][0] + listed[0][1]
    for a, s in listed[1:]:
        if a > end:
            o1, o2 = off(end), off(a)
            if o1 is not None and o2 is not None:
                gap = d[o1:o2]
                bs, be = 0, len(gap)
                while bs < be and gap[bs] == 0xCC: bs += 1
                while be > bs and gap[be - 1] == 0xCC: be -= 1
                segs, cur = [], None
                j = bs
                while j < be:
                    if gap[j] == 0xCC:
                        k = j
                        while k < be and gap[k] == 0xCC: k += 1
                        if (end + k) % 16 == 0:
                            if cur is not None: segs.append((cur, j))
                            cur = k
                        j = k
                    else:
                        if cur is None: cur = j
                        j += 1
                if cur is not None and cur < be: segs.append((cur, be))
                for x, y in segs:
                    if y > x and not all(c in NOPB for c in gap[x:y]):
                        blocks.append((end + x, y - x))
            end = max(end, a + s)
        else:
            end = max(end, a + s)
    return blocks

old_b = split(bodies(kb))
new_b = split(bodies(ka))
pub = set()
for l in open(PUB, encoding="utf-8"):
    if l.startswith("#") or not l.strip(): continue
    f = l.rstrip("\n").split("\t")
    try: pub.add(int(f[0], 16))
    except (ValueError, IndexError): pass
ms = set(a for a, _ in old_b)
check("C4 old-dump blocks are a strict subset of the published census",
      ms <= pub and len(ms) >= 1400, "mine=%d published=%d missing=%d" % (len(ms), len(pub), len(pub - ms)))
oset, nset = dict(old_b), dict(new_b)
moved = [(a, oset.get(a), nset.get(a)) for a in sorted(set(oset) ^ set(nset))]
check("C5 fresh dump moves only the 0057FE80 trailing block",
      all(a in (0x5806B9, 0x5807B8) for a, _, _ in moved) and len(set(new_b)) == len(set(old_b)),
      "moved=%s" % (moved,))
print("old blocks %d / %d bytes -> new %d / %d bytes"
      % (len(old_b), sum(s for _, s in old_b), len(new_b), sum(s for _, s in new_b)))

# --- C6: BO-2 selector inventory (printed for the record) -------------------
print("genuine tag-prefix selectors on functions.tsv:")
for f in files:
    src = open(f, encoding="utf-8", errors="replace").read()
    lits = sorted(selector_literals(src))
    if lits:
        print("   %-72s %s" % (f.replace(os.sep, "/").split("FFXII TZA/")[-1], lits))

# fragment-level gain/loss for every selector literal ever used against the
# tags column (including convergence filters that never appear as "X in tag")
SEL_FRAGS = ("DearImGui", "JsonBox", "LibVPX", "RedBlackTree", "WebM_MKV",
             "NativeLeaf", "CodeDomain.NativeAdapter.", "Phyre.Reflection",
             "CxxStandardLibrary", "Native", "Phyre", "Lifecycle", "Teardown",
             "Funclet", "Unwind", "EHCall", "StaticObjectInit", "StaticLifetime",
             "NamedRegistry", "ContextAudit")
print("selector-fragment row gain/loss across the dump delta:")
for frag in SEL_FRAGS:
    gain = sum(1 for k in ka if k in kb and frag in ka[k][8] and frag not in kb[k][8])
    loss = sum(1 for k in ka if k in kb and frag not in ka[k][8] and frag in kb[k][8])
    if gain or loss:
        print("   %-24s +%d -%d" % (frag, gain, loss))

print("FAILS", len(fails))
sys.exit(1 if fails else 0)
