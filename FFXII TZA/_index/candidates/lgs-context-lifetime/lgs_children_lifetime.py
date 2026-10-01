"""lgs_children_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The release cells of three types
that hang off the now-read context teardown (lgs_lifetime.py) or its helper 003EC8A0.

  R1 003EC8A0 frees *cell through 003697F0 and stores 0 (read in lgs_lifetime.py L5) - RenderCommandBuffer's builders
     004FE420 / 004FE3D0 call it on the previous block, so that release IS the free of the previous block
  R2 LegacyPs2GsReferenceDescriptor: the context's teardown 002F5450 frees +0x1C0 / +0x1C8 / +0x1D0 / +0x1D8 / +0x1E0 /
     +0x1E8 / +0x210 / +0x218 and never touches +0x178 - consistent with the array being an interior pointer into the
     loaded block (its allocation cell): it has no release of its own; its storage goes with that block
  R3 LegacyPs2GsSourceTextureRecord: the teardown hands the container at +0x150 to 00468060, which tail-jumps (non-null) to
     00467CB0; that walks the list at 02EBB6A0 and, for each node whose +0x30 is the container, calls 00536140 - unlink,
     count-1, the list's element callback [list+0x18] on node+0x10, and free of the NODE via 003EC8A0. Neither the 0x20
     container nor its record bank at container+8 is freed on this path: their release is not established
  S  REGRESSION: the three types' dtor cells carry these statements (FAILS before the patch)
Usage: python lgs_children_lifetime.py [--patch]
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
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a, n): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + n], a)]
def mo(a, n): return [(m, o) for _, m, o in body(a, n)]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
F8A = mo(0x3EC8A0, 0x23)
check("R1", ("mov", "rcx, qword ptr [rcx]") in F8A and ("call", "0x3697f0") in F8A and ("mov", "qword ptr [rbx], 0") in F8A
      and ("call", "0x3ec8a0") in mo(0x4FE420, 0x40) + mo(0x4FE3D0, 0x50),
      "003EC8A0 = free *cell (003697F0) + null; RenderCommandBuffer's builders call it")
T = body(0x2F5450, 229)
touched = sorted({int(re.search(r"0x[0-9a-f]+", o).group(0), 16) for a, m, o in T if re.search(r"\[rdi \+ 0x[0-9a-f]+\]", o)})
check("R2", 0x178 not in touched and {0x1C0, 0x1C8, 0x1D0, 0x1D8, 0x1E0, 0x210, 0x218} <= set(touched),
      "the teardown touches %s and never +0x178" % [hex(t) for t in touched])
A = mo(0x468060, 0x10); C = body(0x467CB0, 0x49); U = mo(0x536140, 0x42)
head = next(a + 7 + int(o.split("0x")[1].rstrip("]"), 16) for a, m, o in C if m == "lea" and o.startswith("rdi, [rip +"))
check("R3", A[:2] == [("test", "rcx, rcx"), ("jne", "0x467cb0")] and head == 0x2EBB6A0
      and ("cmp", "qword ptr [rax + 0x30], rbx") in [(m, o) for _, m, o in C] and ("call", "0x536140") in [(m, o) for _, m, o in C]
      and not any(m == "call" and o in ("0x3697f0", "0x3ec8a0") for _, m, o in C)
      and ("dec", "dword ptr [rcx + 0x14]") in U and ("call", "rax") in U and ("call", "0x3ec8a0") in U
      and ("mov", "rcx, qword ptr [rdi + 0x150]") in [(m, o) for _, m, o in T] and ("call", "0x468060") in [(m, o) for _, m, o in T],
      "00468060 -> 00467CB0 frees only the list-02EBB6A0 nodes that name the container (00536140); container and bank not freed")
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/lgs-context-lifetime/lgs_children_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
ADD = {
 "RenderCommandBuffer": " || READ 2026-09-28 (OPUS, %s R1): 003EC8A0 frees the cell's block through 003697F0 and nulls the cell, so the "
                        "builders' first call IS the release of the previous block" % REC,
 "LegacyPs2GsReferenceDescriptor": " || NONE OF ITS OWN 2026-09-28 (OPUS, %s R2): the context's teardown 002F5450 frees its owned blocks "
                        "and never touches +0x178, consistent with this array being an interior pointer into the loaded block; its "
                        "storage goes with that block" % REC,
 "LegacyPs2GsSourceTextureRecord": " || BOUNDED 2026-09-28 (OPUS, %s R3): the context's teardown hands the container at +0x150 to "
                        "00468060 -> 00467CB0, which only unlinks and frees the nodes of the list at 02EBB6A0 that name it (00536140); "
                        "neither the container nor this record bank is freed on that path, so their release stays not established" % REC}
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in ADD and "2026-09-28 (OPUS, %s" % REC not in c[6]:
            c[6] += ADD[c[0]]; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
check("S", all(REC in t[k][6] for k in ADD), "three dtor cells updated")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
