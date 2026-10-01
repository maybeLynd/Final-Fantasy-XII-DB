"""bn1_bullet_version.py - BN-1: the linked Bullet physics is the 2.77 line (FABLE, Claude Opus 5.5, 2026-09-26; found by a
delegated read-only pass, the image side re-checked here and the upstream side re-read from its fetched copies).

Evidence class: STATIC (the image) plus upstream source comparison (github.com/bulletphysics/bullet3 history, which
includes the old svn trunk). The upstream facts, by commit:
  - 3629df72fd92 (2010-02-25, BT_BULLET_VERSION 276, "final Bullet 2.76 release"): btStridingMeshInterface::serialize
    names the short index chunk "btShortIntIndexData";
  - d5ea1d569f74 (2010-02-27, still 276) renames it "btShortIntIndexTripletData";
  - 6fcb48f91813 (2010-07-21, 277, the 2.77 bump): the same, two index cases (PHY_INTEGER, PHY_SHORT);
  - f10846ed7ac5 (2011-01-07, 278) adds a third case, PHY_UCHAR, emitting "btCharIndexTripletData", and every later
    release keeps it (2.79 .. 2.82).
The image side, checked here:
  V1 "btShortIntIndexTripletData" occurs once in the image; "btShortIntIndexData" and "btCharIndexTripletData" occur
     nowhere. So the image is after 2010-02-27 and before 2011-01-07.
  V2 the image's btStridingMeshInterface::serialize 008365C0 names the triplet chunk (00836762) and switches on
     the index type with exactly two arms: PHY_INTEGER (2) and PHY_SHORT (3) (008366DA..008366E6).
  V3 independent upper bound: the RTTI still nests InplaceSolverIslandCallback inside
     btDiscreteDynamicsWorld::solveConstraints. Upstream moved it to file scope on 2011-12-12 (606d65d95b96).
  Control: the same string search finds zlib's "inflate 1.2.11" banner.
So the only release in the window is 2.77. A trunk snapshot from the same window (to 2011-01-07) also fits, and the image
cannot separate the two.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
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
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def rip(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); s = x.op_str
    return x.address + x.size + int(s.split("rip + ")[1].split("]")[0], 16) if "rip + " in s else None
def cstr(v): o = off(v); return d[o:d.find(b"\0", o)].decode("latin-1")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
c = {s: d.count(s) for s in (b"btShortIntIndexTripletData\0", b"btShortIntIndexData\0", b"btCharIndexTripletData\0")}
check("V1 the triplet name once, the 2.76 name and the 2.78+ name nowhere; control: zlib's banner is found",
      c[b"btShortIntIndexTripletData\0"] == 1 and c[b"btShortIntIndexData\0"] == 0 and c[b"btCharIndexTripletData\0"] == 0
      and d.count(b"inflate 1.2.11") >= 1, str({k[:-1].decode(): v for k, v in c.items()}))
check("V2 008365C0 names the triplet chunk and has two index arms (PHY_INTEGER 2, PHY_SHORT 3)",
      cstr(rip(0x836762)) == "btShortIntIndexTripletData" and at(0x8366DA) == "mov ecx, dword ptr [rbp + 3]"
      and at(0x8366DD) == "sub ecx, 2" and at(0x8366E6) == "cmp ecx, 1", "%s | %s" % (cstr(rip(0x836762)), at(0x8366E6)))
check("V3 the island callback is still local to solveConstraints (upstream moved it out on 2011-12-12)",
      d.count(b".?AUInplaceSolverIslandCallback@?1??solveConstraints@btDiscreteDynamicsWorld@@") == 1)
print("FAILS", fails)
sys.exit(1 if fails else 0)
