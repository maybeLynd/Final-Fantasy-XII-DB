"""ui_atlas.py: widget procedures in 0x00550000-0x00580000 labelled by three independent kinds of evidence gathered over each
procedure's callee subtree (depth <= 3, stopping at other widget procedures and at functions with more than 12 callers):
layout-key families read (16-UI/Layout-Parameter-System/members/layout-key-readers.tsv), resource files requested by constant
(02-.../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv) and the menu effect registry API called.
Also: who installs the procedure (rip lea) and the frontier count of its subtree."""
import bisect, collections, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
GFZ = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, GFZ)
import check_dispositions as cd
import frontier_census as fc
import call_graph as cg
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FUNCS = os.path.abspath(os.path.join(GFZ, "..", "..", "work", "graph", "functions.tsv"))
EXE = os.path.abspath(os.path.join(GFZ, "..", "..", "work", "exe", "FFXII_TZA.exe"))
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
ks = sorted(sizes)
def own(s):
    i = bisect.bisect_right(ks, s) - 1
    return ks[i] if i >= 0 and ks[i] <= s < ks[i] + sizes[ks[i]] else None
# call graph rebuilt from the EXE + functions.tsv, calls AND tail jumps (was tools/rawcalls.json;
# edges.tsv drops tail jumps, so it is not a substitute)
callers, callees, _sites = cg.call_maps(EXE, FUNCS)
ncallers = collections.Counter({t: len(cs) for t, cs in callers.items()})
front = fc.frontier_set(DB, sizes)          # the live frontier; was arch_frontier.txt + c_frontier.txt
procs = set(int(l.split("\t")[0], 16) for l in open(DB + r"\16-UI\Widget-Object-Model\widget-message-handlers.tsv", encoding="utf-8") if re.match(r"[0-9A-F]{8}\t", l))
import os
LO, HI = (int(os.environ.get("ATLAS_LO", "550000"), 16), int(os.environ.get("ATLAS_HI", "580000"), 16))
region = sorted(p for p in procs if LO <= p < HI)
keyfam = collections.defaultdict(set)
for l in open(DB + r"\16-UI\Layout-Parameter-System\members\layout-key-readers.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if c[0] == "key" or "BlackBand" in c[0]: continue   # fade band heights are read by the shared fades, not by a screen
    k = re.sub(r"^m", "", c[0]); m = re.match(r"([A-Z][a-z]+(?:[A-Z][a-z]+)?)", k)
    keyfam[int(c[2], 16)].add(m.group(1) if m else k)
files = collections.defaultdict(set)
for l in open(DB + r"\02-Resource-And-Asset-Pipeline\VBF-Archive-And-Authored-Tables\members\constant-resource-requests.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if c[0] == "api" or c[6] == "-": continue
    loader = own(int(c[7], 16)) if c[7] != "-" else int(c[2], 16)
    files[loader].add(c[6].split("\\")[-1])
REG = {0x3B29B0: "fx-reset", 0x3B2D80: "fx-spawn", 0x3B2AA0: "fx-remove", 0x3B2F50: "fx-set"}
def subtree(root):
    seen = {root}; frontier = [root]
    for _ in range(3):
        nxt = []
        for f in frontier:
            for c in callees[f]:
                if c in seen or c not in sizes: continue
                if c in procs and c != root: continue
                if ncallers[c] > 12: continue
                seen.add(c); nxt.append(c)
        frontier = nxt
    return seen
out = []
for p in region:
    st = subtree(p)
    kf = set().union(*(keyfam[f] for f in st)) - {"FontBase", "BlackBand", "PartyBlack"}
    fl = set().union(*(files[f] for f in st))
    fx = sorted(set(REG[c] for f in st for c in callees[f] if c in REG))
    out.append((p, len(st), len(st & front), sorted(kf), sorted(fl), fx))
for p, n, nf, kf, fl, fx in out:
    print("%08X  subtree %3d frontier %3d | keys %s | files %s | %s" % (p, n, nf, ",".join(kf)[:60], ",".join(fl)[:90], ",".join(fx)))

# ---- table output with installers, message ids and an evidence label ----
import os
hand = {}
for l in open(DB + r"\16-UI\Widget-Object-Model\widget-message-handlers.tsv", encoding="utf-8"):
    c = l.rstrip("\n").split("\t")
    if re.match(r"[0-9A-F]{8}$", c[0]): hand[int(c[0], 16)] = c[6] if len(c) > 6 else ""
# installers: one pass over every listed function for rip-relative `lea` operands that name a procedure
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
_d = open(EXE, "rb").read()
_pe = struct.unpack_from("<I", _d, 0x3C)[0]; _ns = struct.unpack_from("<H", _d, _pe + 6)[0]; _opt = struct.unpack_from("<H", _d, _pe + 20)[0]
for _i in range(_ns):
    _o = _pe + 24 + _opt + _i * 40
    if _d[_o:_o + 8].rstrip(b"\0") == b".text":
        _va = struct.unpack_from("<I", _d, _o + 12)[0]; _ro = struct.unpack_from("<I", _d, _o + 20)[0]
_md = Cs(CS_ARCH_X86, CS_MODE_64); _md.detail = True
inst = collections.defaultdict(set)
_want = set(region)
for _e in ks:
    _off = _ro + (_e - 0x120000 - _va)
    if _off < 0 or _off + sizes[_e] > len(_d): continue
    for _ins in _md.disasm(_d[_off:_off + sizes[_e]], _e):
        if _ins.mnemonic != "lea": continue
        _op = _ins.operands[1]
        if _op.type == X86_OP_MEM and _op.mem.base and _ins.reg_name(_op.mem.base) == "rip":
            _t = _ins.address + _ins.size + _op.mem.disp
            if _t in _want and _t != _e:
                inst[_t].add("%08X" % _e if names.get(_e, "").startswith("FUN_") else names.get(_e, "%08X" % _e))
exec(open(os.path.join(HERE, "ui_atlas_label.py"), encoding="utf-8").read().split("rows = [l.rstrip")[0].split('import sys, collections')[1])   # defines FAM
def label(kf, fl, fx, p):
    ks = set(kf); fs = " ".join(fl).lower(); nm = " ".join(inst[p])
    if "Save" in nm: return "save / load UI (installer name)"
    m = []
    if "LicenseBoard" in ks or "lic_" in fs or "license" in fs: m.append("license board")
    if "WorldMap" in ks or "MapName" in ks or "w_" in fs or "meshdata" in fs: m.append("world map")
    if "loca" in fs: m.append("location map")
    if ks & {"GambitAction", "GambitTarget", "GambitIcon", "GambitTutorial"}: m.append("gambits")
    if "ShopItem" in ks or "shop" in fs: m.append("shop")
    if "handbook" in fs or "handback" in fs: m.append("handbook")
    if "menuquest" in fs: m.append("quest list")
    if "ItemSort" in ks: m.append("item sort")
    if ks & {"ConfirmWindow", "ConfirmCaption"}: m.append("confirm window")
    m += [name for fams, name in FAM if ks & fams and name not in m]
    if not m: return ""
    if len(m) > 2: return "several screens: " + " + ".join(m)
    return " + ".join(m)
rows = []
sub = {p: subtree(p) for p, *_ in out}
lab0 = {p: label(kf, fl, fx, p) for p, n, nf, kf, fl, fx in out}
for _ in range(3):   # a procedure installed by a labelled procedure or one of its direct callees is recorded as that screen's child
    for p in lab0:
        if lab0[p] or p in (0x5C5230, 0x17CDE0): continue   # the ICF return-0 stub and its thunk are shared null procedures
        for q_, l_ in list(lab0.items()):
            if l_ and "child" not in l_ and not l_.startswith("several") and any((int(x, 16) == q_ or int(x, 16) in callees[q_]) for x in inst[p] if re.match(r"[0-9A-F]{8}$", x)):
                lab0[p] = l_ + " (child: installed by the procedure or its direct callee)"; break
for p, n, nf, kf, fl, fx in out:
    rows.append((p, n, nf, kf, fl, fx, lab0[p], sorted(inst[p]), hand.get(p, "")))
cov = set(); allf = set()
for r in rows:
    allf |= (sub[r[0]] & front)
    if r[6]: cov |= (sub[r[0]] & front)
print("unique frontier in all subtrees", len(allf), "in labelled subtrees", len(cov), file=sys.stderr)
with open(os.environ.get("ATLAS_OUT", os.path.join(HERE, "ui_atlas.tsv")), "w", encoding="utf-8", newline="\n") as f:
    f.write("procedure\tsubtree\tfrontier\tlabel\tinstalled_by\tmessage_ids\tlayout_key_families\tconstant_files\teffect_registry\n")
    for r in rows:
        f.write("%08X\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r[0], r[1], r[2], r[6] or "-", " ".join(r[7]) or "-", r[8] or "-", ",".join(r[3]) or "-", ",".join(r[4]) or "-", ",".join(r[5]) or "-"))
lab = collections.Counter(r[6] or "unlabelled" for r in rows)
print("procs", len(rows), dict(lab), "subtree frontier labelled", sum(r[2] for r in rows if r[6]), "unlabelled", sum(r[2] for r in rows if not r[6]), file=sys.stderr)
