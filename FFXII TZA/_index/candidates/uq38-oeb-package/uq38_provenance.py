"""uq38_provenance.py - UQ-38's residue as OUT OF EVIDENCE BOUNDARY, part 3 (FABLE, Claude Opus 5.5, 2026-09-28).

UQ-38 asks how each of the 267 register-bank members was authored: as a whole translated routine or as a C routine
with translated fragments. Both are C compiled by the same MSVC, so the answer is a fact about the source. The direct
carriers are the source tree and FF12X64.pdb's module and line records, which say which source file each function came
from. This checks that nothing shipped carries that per-member provenance instead:
  P1  no member references a source-path string (__FILE__-style). Control: 949 functions image-wide do, e.g.
      00267930 -> ..\\..\\katano\\ateldecode.c, so the detector sees such strings
  P2  no member lies between two functions that cite the same source file (MSVC links an object's functions
      contiguously, so a bracketed member would inherit that file). Control: 00267990, between 00267930 and 00267BB0,
      is bracketed by ateldecode.c
  P3  the image has no COFF symbol table, and its one debug record is CodeView RSDS naming ...FF12X64.pdb. The PDB
      ships nowhere: ../nas-label-scans/lost_build_scan.py L2 (run separately; it walks the install and the extract)
The static criteria the row already measured do not separate the two classes: bank-access density, calls outside the
set, register carry across bank stores (../uq38-carry-criterion/, retired), and the interface criteria I1-I3.
"""
import os, re, struct, sys, bisect, collections
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
TSV = os.path.join(HERE, "../uq38-carry-criterion/uq38_carry.tsv")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
symptr, nsym = struct.unpack_from("<II", d, pe + 12)
secs = []; o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, rs, ra)); o += 40
def foff(rva):
    for va, rs, ra in secs:
        if va <= rva < va + rs: return ra + rva - va
def cstr(v):
    f = foff(v - 0x120000)
    if f is None: return None
    b = d[f:f + 200]; e = b.find(b"\0"); s = b[:e if e >= 0 else 200]
    return s.decode("latin-1") if s and all(32 <= c < 127 for c in s) else None
members = [l.split("\t")[0] for l in open(TSV, encoding="utf-8").read().split("\n")[1:] if l.strip()]
refs = collections.defaultdict(set)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3 and p[2].startswith("lea"):
        m = re.search(r"=>([0-9A-F]{8})", p[2])
        if m: refs[p[1]].add(m.group(1))
SRC = re.compile(r"\.(c|cc|cpp|cxx|h|hpp|inl)$", re.I)
fpath = collections.defaultdict(set)
for f, aa in refs.items():
    for a in aa:
        s = cstr(int(a, 16))
        if s and SRC.search(s): fpath[f].add(s)
mem_p = [f for f in members if f in fpath]
ok("P1", len(members) == 267 and not mem_p and len(fpath) > 300 and "..\\..\\katano\\ateldecode.c" in fpath.get("00267930", ()),
   "%d members, %d reference a source-path string; image-wide %d functions do (control 00267930 -> %s)"
   % (len(members), len(mem_p), len(fpath), sorted(fpath.get("00267930", ["-"]))[0]))
keys = sorted(fpath, key=lambda x: int(x, 16)); kv = [int(k, 16) for k in keys]
def bracket(f):
    v = int(f, 16); i = bisect.bisect_left(kv, v)
    lo = keys[i - 1] if i > 0 else None
    hi = keys[i + 1] if i < len(keys) and keys[i] == f else (keys[i] if i < len(keys) else None)
    return sorted(fpath[lo] & fpath[hi]) if lo and hi else []
br = [f for f in members if bracket(f)]
ok("P2", not br and bracket("00267990") == ["..\\..\\katano\\ateldecode.c"],
   "members bracketed by a source file: %d; control 00267990 bracketed by %s" % (len(br), bracket("00267990")))
dd_rva, dd_size = struct.unpack_from("<II", d, pe + 24 + (112 if struct.unpack_from("<H", d, pe + 24)[0] == 0x20B else 96) + 6 * 8)
recs = []; f0 = foff(dd_rva)
for k in range(dd_size // 28):
    ch, ts, ma, mi, typ, sz, rva, ptr = struct.unpack_from("<IIHHIIII", d, f0 + 28 * k)   # IMAGE_DEBUG_DIRECTORY
    recs.append((typ, sz, ptr))
cv = [d[p:p + s] for t, s, p in recs if t == 2]
pdb = cv[0][24:].split(b"\0")[0].decode("latin-1") if cv and cv[0][:4] == b"RSDS" else ""
ok("P3", symptr == 0 and nsym == 0 and len(cv) == 1 and pdb.endswith("FF12X64.pdb"),
   "COFF symbols: pointer %d, count %d; debug records %s; CodeView names %s" % (symptr, nsym, [t for t, s, p in recs], pdb))
print("FAILS", fails); sys.exit(1 if fails else 0)
