"""rc6_packs.py - RC-6 (ORACLE, 2026-09-30).  Why console-table entries 670 (rbl0102) and 1003 (gil0301) differ from the
pack map_ref.bin gives their field (rbl0121.mpk, gil0303.mpk).

Instrument independent of the size-matched census names: the image's own pack path table, g_pathTables[4] (kind 4,
installed unconditionally by ResourcePath_Init 002DF9A0, the same array in every region), whose row n is the path of
pack index n.  map_ref.bin's own-pack index for a field (map-ref-field-packs.tsv column own_idx, decoded from the
file's rows) is then named by the image rather than by file sizes.
Checks:
  K1 the console table (01DF6E68, 16-byte entries) joined with the kind-4 name of each field's own pack index:
     how many populated entries agree, and which console codes have no row anywhere in the kind-4 table;
  K2 the kind-4 rows around the two packs (the rbl01 run and the gil03 run);
  K3 map_ref rows for the neighbouring fields (own pack index, block, w2, w3);
  K4 the shipped archive: entries naming rbl0102 / gil0303, and the map codes embedded in gil0303.mpk and gil0301.mpk.
Controls: K1 must reproduce SWE2-CONTRACT's join (599 agree, 2 disagree, at 670 and 1003); kind-4 row 1 must be
ous0101.mpk and row 0 ous0100.mpk (area-nmb-index.md's first entries)."""
import collections, contextlib, io, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img
with contextlib.redirect_stdout(io.StringIO()):
    import rc5_paths as R          # ResourcePath_Init replay (region arms) and string helpers
sys.path.insert(0, os.path.join(os.path.dirname(img.EXE), "..", "..", "..", "..", "agent_flow", "tools"))
import vbfextract
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TSV = os.path.join(DB, "03-World-Area-Field", "Map-Pack", "members", "map-ref-field-packs.tsv")
T, N = 0x01DF6E68, 1314
FAILS = []

arrays = {R.regions[e][0][4] for e in range(13)}
if len(arrays) != 1:
    FAILS.append("kind 4 differs by region")
a4 = arrays.pop()
n4 = (R.bound(a4) - a4) // 8
k4 = {}
for r in range(n4):
    s = R.row(a4, r)
    if s:
        k4[r] = s.split("\\")[-1]
if k4.get(0) != "ous0100.mpk" or k4.get(1) != "ous0101.mpk":
    FAILS.append("kind 4 row control")
codes = {}
for i in range(N):
    p = struct.unpack("<Q", img.rd(T + 16 * i, 8))[0]
    if p:
        codes[i] = R.cstr(p)
mr = {}
for line in io.open(TSV, encoding="utf-8").read().splitlines():
    if line.startswith("#") or line.startswith("field"):
        continue
    p = line.split("\t")
    mr[int(p[0])] = p
agree, dis = 0, []
for i, c in sorted(codes.items()):
    own = k4.get(int(mr[i][1])) if i in mr else None
    if own and own[:-4] == c:
        agree += 1
    else:
        dis.append((i, c, own, mr[i][1] if i in mr else None))
print("K1 kind-4 pack table: array %08X, %d rows before the next installed array, %d named" % (a4, n4, len(k4)))
print("K1 console entries populated %d: agree with the kind-4 name of the field's own pack %d; disagree %s" % (len(codes), agree, dis))
if agree != 599 or [d[0] for d in dis] != [670, 1003]:
    FAILS.append("K1 control: SWE2-CONTRACT join not reproduced")
names_set = {v[:-4] for v in k4.values()}
print("K1 console codes with no kind-4 pack row at all:", sorted((i, c) for i, c in codes.items() if c not in names_set))
print("K2 kind-4 rows 702..725 (rbl01 run, row = 702 + map number where named):")
for r in range(702, 726):
    print("    %d %s" % (r, k4.get(r)))
print("K2 kind-4 rows 677..681 (gil03 run):", [(r, k4.get(r)) for r in range(677, 682)])
print("K2 rows naming rbl0102: %s ; gil0303: %s" % ([r for r, v in k4.items() if "rbl0102" in v], [r for r, v in k4.items() if "gil0303" in v]))
own_count = collections.Counter(int(p[1]) for p in mr.values())
print("K3 fields owning pack index 723 (rbl0121): %s ; 680 (gil0303): %s ; 704 (the empty rbl0102 slot): %d" %
      ([f for f, p in mr.items() if p[1] == "723"], [f for f, p in mr.items() if p[1] == "680"], own_count[704]))
empty_rbl01 = [r for r in range(702, 726) if r not in k4]
print("K3 fields whose own pack index is an EMPTY rbl01 kind-4 slot %s:" % empty_rbl01,
      [(f, int(p[1]), "console %s" % codes.get(f)) for f, p in sorted(mr.items()) if int(p[1]) in empty_rbl01])
print("K3 console codes of the other fields owning rbl0121 (723):", [(f, codes.get(f)) for f in (122, 683, 1230)])
for f in list(range(666, 672)) + list(range(1000, 1008)):
    p = mr[f]
    print("    field %d own_idx %s (%s) block %s w2 %s w3 %s | console %s" % (f, p[1], k4.get(int(p[1])), p[4], p[8], p[9], codes.get(f)))
vf = io.open(VBF, "rb")
names, blocks = vbfextract.load_index(vf)
for code in ("rbl0102", "gil0303"):
    print("K4 archive entries naming %s: %s" % (code, [x for x in names if code in x.lower()]))
for pk in ("ps2data/plan_master/map_ctrl/gil03/gil0303/bin/gil0303.mpk", "ps2data/plan_master/map_ctrl/gil03/gil0301/bin/gil0301.mpk"):
    b = vbfextract.read_entry(vf, names, blocks, pk)
    print("K4 %s: %d bytes, map codes inside %s" % (pk.split("/")[-1], len(b), sorted({c.decode() for c in re.findall(rb"[a-z]{3}\d{4}", b)})))
print("FAILS", len(FAILS), FAILS)
