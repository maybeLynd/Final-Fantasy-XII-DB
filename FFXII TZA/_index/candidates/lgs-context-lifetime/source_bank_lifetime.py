"""source_bank_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. LegacyPs2GsSourceTextureRecord's
release cell, narrowed further (after lgs_children_lifetime.py R3 showed the context's teardown does not free it).

  B1 the container initialiser 00467D20 frees the PREVIOUS record bank before allocating the next: add rcx, 8 / call 003EC8A0
     (00467DBA / 00467DC6) - free *(container+8) and null it - then 003EC8D0(6, count * 0x60) (00467DD2..00467DDD). A rebuild
     of a container therefore releases its old bank
  B2 a container destructor exists: 00467B30 calls the container's +0x10 callback when set, then frees +8 through 003EC8A0
     (tail-jump 00467B4D); 00467B20 is a destroy-cell on (arg + 0x20) with 00467B30 as the callback (lea rdx -> 00467B30,
     jmp 003EC860). Neither has a direct caller in .text, so they are reached indirectly
  Not established: what releases the 0x20 container the context holds at +0x150, or its bank at teardown.
  S  REGRESSION: the dtor cell carries B1 / B2 (FAILS before the patch)
Usage: python source_bank_lifetime.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
check("B1", at(0x467DBA)[:2] == ("add", "rcx, 8") and at(0x467DC6)[:2] == ("call", "0x3ec8a0") and at(0x467DD2)[:2] == ("lea", "edx, [rcx + rcx*2]")
      and at(0x467DDA)[:2] == ("shl", "edx, 5") and at(0x467DDD)[:2] == ("call", "0x3ec8d0"),
      "00467D20 frees the previous bank (container+8) before allocating count * 0x60")
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]; thi = tlo + text[3]
callers = []
for i in range(off(tlo), off(tlo) + text[3] - 5):
    if d[i] in (0xE8, 0xE9):
        v = tlo + i - off(tlo); t = v + 5 + struct.unpack_from("<i", d, i + 1)[0]
        if t in (0x467B20, 0x467B30):
            try:
                x = next(cs.disasm(d[i:i + 5], v))
                if x.mnemonic in ("call", "jmp"): callers.append("%X" % v)
            except StopIteration: pass
check("B2", at(0x467B20)[:2] == ("add", "rcx, 0x20") and at(0x467B24)[2] == 0x467B30 and at(0x467B2B)[:2] == ("jmp", "0x3ec860")
      and at(0x467B36)[:2] == ("mov", "rax, qword ptr [rcx + 0x10]") and at(0x467B42)[:2] == ("call", "rax")
      and at(0x467B44)[:2] == ("lea", "rcx, [rbx + 8]") and at(0x467B4D)[:2] == ("jmp", "0x3ec8a0") and not callers,
      "00467B30 = container dtor (callback, free +8); 00467B20 = destroy-cell with it; direct callers %s" % callers)
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/source_bank_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
ADD = (" || NARROWED 2026-09-28 (OPUS, %s B1 B2): the bank IS freed on rebuild - the container initialiser 00467D20 frees the "
       "previous bank at container+8 through 003EC8A0 (00467DC6) before allocating the next (00467DDD) - and a container "
       "destructor exists, 00467B30 (the container's +0x10 callback, then free +8), wrapped by the destroy-cell 00467B20; neither "
       "has a direct caller. What releases the context's +0x150 container, or its bank at teardown, stays not established" % REC)
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "LegacyPs2GsSourceTextureRecord" and REC not in c[6]:
            c[6] += ADD; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
check("S", REC in t["LegacyPs2GsSourceTextureRecord"][6], "the dtor cell carries B1 / B2")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
