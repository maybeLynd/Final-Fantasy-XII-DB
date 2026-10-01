"""PPhysicsCharacterCamera +0x48 / +0x58 / +0x68: three inline Vector3 members (OPUS, 2026-09-27). Control. Static.

  V1 the three script-accessor adapters return the member's ADDRESS: 006A3960 `lea rax, [rcx+0x48]`, 006A3970
     `lea rax, [rcx+0x58]`, 006A3950 `lea rax, [rcx+0x68]`, each followed by ret (inline members, not pointers)
  V2 the registration body 00694260 binds getCameraPosition / getCameraTarget / getCameraDirection (00694720,
     006947F8, 006948C9) and stores ONE caller vtable into each of the three caller objects (02E4A5F0, 02E4A650,
     02E4A6B0, 0x60 apart): rbp = 00D7B030 (006947AA), whose RTTI is
     PMethodCallerConcrete<PPhysicsCharacterCamera, const sce::Vectormath::Scalar::Aos::Vector3 &>
  V3 the members are 0x10 apart, and the store's existing rows of this type are all 16 bytes (the scalar AoS Vector3:
     x, y, z and a pad word)
Not claimed: what the camera does with them (meaning axis); any access to the pad words.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
def rtti(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]
    otd = off(BASE + struct.unpack_from("<I", d, off(col) + 12)[0])
    return d[otd + 16:otd + 300].split(b"\0")[0].decode("latin-1")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

A = {0x6A3960: 0x48, 0x6A3970: 0x58, 0x6A3950: 0x68}
check("V1 the adapters are lea rax, [rcx+off] / ret",
      all([v for k, v in sorted(ins(a, 8).items())][:2] == ["lea rax, [rcx + 0x%x]" % o, "ret "] for a, o in A.items()))

R = ins(0x694260, 1850)
def rip_target(a):
    x = next(cs.disasm(d[off(a):off(a) + 15], a))
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
names = {a: d[off(rip_target(a)):off(rip_target(a)) + 32].split(b"\0")[0].decode() for a in (0x694720, 0x6947F8, 0x6948C9)}
stores = {a: rip_target(a) for a in (0x6947B1, 0x694882, 0x694953)}
vt = rip_target(0x6947AA)
check("V2 one Vector3-returning caller vtable is stored into each accessor's caller object",
      list(names.values()) == ["getCameraPosition", "getCameraTarget", "getCameraDirection"]
      and R.get(0x6947AA, "").startswith("lea rbp,") and all(R.get(a, "").endswith(", rbp") for a in stores)
      and sorted(stores.values()) == [0x2E4A5F0, 0x2E4A650, 0x2E4A6B0]
      and rtti(vt) == ".?AV?$PMethodCallerConcrete@VPPhysicsCharacterCamera@PPhysics@Phyre@@AEBVVector3@Aos@Scalar@Vectormath@sce@@"
                      "@PCallerImplementation0@PCallerImplementation@PInternal@Phyre@@",
      "%08X %s" % (vt, rtti(vt)[:60]))

sizes = set()
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) > 4 and c[4] == "sce::Vectormath::Scalar::Aos::VVector3" and c[0] != "PPhysicsCharacterCamera":
        sizes.add(int(c[2]))
check("V3 the members are 0x10 apart and the store's other rows of this type are all 16 bytes",
      sorted(A.values()) == [0x48, 0x58, 0x68] and sizes == {16}, str(sizes))
print("FAILS", fails)
sys.exit(1 if fails else 0)
