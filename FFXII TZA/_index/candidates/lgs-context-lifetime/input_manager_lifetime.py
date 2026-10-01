"""input_manager_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. InputManager's release cell
read 'the vtable's only slot 001955F0 (not read here)'.

  I1 001955F0 is a scalar deleting destructor: it stores the vtable 008F3640 back at +0x00, and when flag bit 0 is set calls
     the sized operator delete 00809950(this, 0x40); it releases no member
  I2 the singleton cell 01F7FFE0 is written once in listed code - 00198784 in InputManager_CreateSingleton 00198750, after
     its null test at 0019875D - and otherwise only read (00197160, the getter 00198790); nothing clears it, so no
     destruction of the singleton through its cell appears. A caller destroying it through the getter's pointer is not
     excluded
  S  REGRESSION: the dtor cell carries I1 / I2 (FAILS before the patch)
Usage: python input_manager_lifetime.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
D = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x1955F0):off(0x1955F0) + 0x2B], 0x1955F0)]
M = [(m, o) for a, m, o in D]
check("I1", ("lea", "rax, [rip + 0x75e043]") in M and 0x1955FD + 0x75E043 == 0x8F3640 and ("mov", "qword ptr [rcx], rax") in M
      and ("test", "dl, 1") in M and ("mov", "edx, 0x40") in M and ("call", "0x809950") in M
      and sum(1 for m, o in M if m == "call") == 1,
      "001955F0: vtable back, sized delete(this, 0x40) on flag bit 0, no member release")
F = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    c = l.split("\t")
    try: F[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
acc = []
for f, s in F.items():
    o = off(f) if 0x121000 <= f < 0x900000 else None
    if o is None or s <= 0: continue
    for x in cs.disasm(d[o:o + s], f):
        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
        if m and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == 0x1F7FFE0:
            acc.append(("w" if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip") else "r", "%08X" % x.address, "%08X" % f))
w = [a for k, a, f in acc if k == "w"]
check("I2", w == ["00198784"] and ("r", "0019875D", "00198750") in acc and {f for k, a, f in acc} == {"00197160", "00198750", "00198790"},
      "01F7FFE0: one write %s after the null test; readers %s" % (w, sorted({f for k, a, f in acc})))
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/input_manager_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
ADD = (" || READ 2026-09-28 (OPUS, %s I1 I2): 001955F0 is the scalar deleting destructor - it restores the vtable 008F3640 and, "
       "with flag bit 0, calls the sized operator delete 00809950(this, 0x40); it releases no member. The singleton cell "
       "01F7FFE0 is written once (00198784, after the null test at 0019875D) and never cleared in listed code, so no "
       "destruction of the singleton through its cell appears; one through the getter's pointer is not excluded" % REC)
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "InputManager" and REC not in c[6]:
            c[6] = c[6].replace(" (not read here)", "") + ADD; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
check("S", REC in t["InputManager"][6], "the dtor cell carries I1 / I2")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
