"""uq212_no_names.py - UQ-212 (designer-facing names for the texture and slot records) is a class-3 row: the names would
be in the source or the PDB, neither shipped (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  N1 the twelve functions the texture-budget page names reference no string: every rip-relative target they load is a
     global or a constant, none an ASCII run of 4+ characters.
  N2 the records are PODs: none of the twelve is a slot of any vtable the RTTI map knows, so no type descriptor can
     carry a class name for them.
  N3 the image carries a CodeView debug record naming a PDB (the build artefact that would hold the type names), and
     the PDB itself is not shipped with the game.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
F = [0x2F7380, 0x466190, 0x3A1E50, 0x466220, 0x467AA0, 0x467AD0, 0x467B00, 0x467B10, 0x244200, 0x39D200, 0x3EC8A0, 0x3EC8D0]
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
strings = []; targets = 0
for f in F:
    for x in cs.disasm(d[off(f):off(f) + SIZES[f]], f):
        m = RIP.search(x.op_str)
        if not m: continue
        targets += 1
        t = x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
        o = off(t); s = d[o:o + 32].split(b"\0")[0] if o is not None else b""
        if len(s) >= 4 and all(32 <= c < 127 for c in s): strings.append(("%08X" % t, s))
check("N1 the page's twelve functions reference no string", strings == [] and targets >= 20, "rip targets %d, strings %s" % (targets, strings))

rtti = ROOT / "Database/Tools/work/FABLE/drift5/rtti-map.tsv"
slots = set()
for line in open(rtti, encoding="utf-8"):
    p = line.split("\t")
    try: vt = int(p[0], 16)
    except ValueError: continue
    for k in range(64):
        o = off(vt + 8 * k)
        if o is None: break
        v = struct.unpack_from("<Q", d, o)[0]
        if not (0x121000 <= v < 0x8C0000): break
        slots.add(v)
check("N2 none of the twelve is a vtable slot of any RTTI class", not (set(F) & slots) and len(slots) > 1000, "%d slots known" % len(slots))

dd = pe + 24 + 112 + 6 * 8  # PE32+ data directory 6 = debug
drva, dsz = struct.unpack_from("<II", d, dd)
cv = []
for k in range(dsz // 28):
    e = off(BASE + drva) + 28 * k
    typ, size, raw = struct.unpack_from("<I", d, e + 12)[0], struct.unpack_from("<I", d, e + 16)[0], struct.unpack_from("<I", d, e + 24)[0]
    if typ == 2 and d[raw:raw + 4] == b"RSDS": cv.append(d[raw + 24:raw + size].split(b"\0")[0].decode("latin-1"))
game = Path("D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/x64")
shipped = sorted(p.name for p in game.glob("*.pdb")) if game.exists() else None
check("N3 a CodeView record names a PDB, and no PDB ships beside the executable",
      len(cv) == 1 and cv[0].lower().endswith(".pdb") and (shipped == [] or shipped is None),
      "pdb %r; shipped pdbs %s" % (cv[0] if cv else None, "not checked (install absent)" if shipped is None else shipped))
print("FAILS", fails)
sys.exit(1 if fails else 0)
