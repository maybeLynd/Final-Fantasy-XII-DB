"""lgs_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

LegacyPs2GsTextureContext (0x240) was recorded as 'one heap instance at 0209A670' with release 'none identified - 0026E20C
clears the global ... no deallocation of the 0x240 block was found'. Both are wrong. The release is the builders' own
first call:
  L1 003EC860(cell, callback) is a destroy-cell helper: if *cell, call callback(*cell) (when non-null), then free *cell
     through 003697F0 and store 0 into the cell
  L2 both builders release the previous instance before allocating the next: 0026E760 calls 003EC860(&0209A670, 0026EDB0)
     at 0026E77B; 0026E7D0 calls it on 0209A670 at 0026E7E7 and on 0209A668 at 0026E804, then builds a SECOND context
     (003EC8D0(6, 0x240) at 0026E827, 002F6AB0 at 0026E837) and stores it at 0209A668 (0026E841)
  L3 0026EDB0 is the context's destructor: it calls the function pointer at +0x128 when non-null (0026EDBA..0026EDC9),
     then runs 0016D6A0 - the ICF-folded `ret 0` - on each of the two 0x68 chunk records at +0x40 (0026EDCB..0026EDE4)
  L4 the constructor stores 002F5450 at +0x128 (002F6B2E lea rax / 002F6B35)
  L5 002F5450 frees the context's owned blocks through 003EC8A0 (free *cell via 003697F0, then null it): +0x1D8, each
     record's +0xC0 in the +0x1D0 array (count +0x220, stride 0xE0), the two 0x18-stride pairs at +0x1E0 / +0x1E8, +0x1C8,
     +0x1D0, +0x210, +0x1C0, +0x218; and releases +0x168 via 003ECA70 and +0x150 via 00468060
  L6 +0x1C0 is an OWNED POINTER: 002F6F5D allocates count * 0x70 (003EC8D0 tag 6) and 002F6F76 stores the result there;
     the row's 'ADDRESS TERM, NOT A POINTER' (2026-09-19) is wrong - the one `add` read uses it as a base
  S  REGRESSION: the store's LegacyPs2GsTextureContext dtor cell names 003EC860 / 0026EDB0 / 002F5450, its instance cell
     names 0209A668, and +0x1C0 is void* (FAILS before the patch)
Usage: python lgs_lifetime.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)) if m else None
def body(a, n): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + n], a)]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
H = {a: (m, o) for a, m, o in body(0x3EC860, 0x32)}
check("L1", H[0x3EC869] == ("mov", "rcx, qword ptr [rcx]") and H[0x3EC876] == ("call", "rdx") and H[0x3EC880] == ("call", "0x3697f0")
      and H[0x3EC885] == ("mov", "qword ptr [rbx], 0"), "003EC860: callback(*cell), free via 003697F0, null the cell")
l2 = (at(0x26E76D)[2] == 0x26EDB0 and at(0x26E774)[2] == 0x209A670 and at(0x26E77B)[:2] == ("call", "0x3ec860")
      and at(0x26E7E0)[2] == 0x209A670 and at(0x26E7E7)[:2] == ("call", "0x3ec860") and at(0x26E7FD)[2] == 0x209A668
      and at(0x26E804)[:2] == ("call", "0x3ec860") and at(0x26E81B)[:2] == ("mov", "edx, 0x240") and at(0x26E827)[:2] == ("call", "0x3ec8d0")
      and at(0x26E837)[:2] == ("call", "0x2f6ab0") and at(0x26E841)[2] == 0x209A668 and at(0x26E841)[0] == "mov")
check("L2", l2, "0026E760 / 0026E7D0 release 0209A670 (and 0209A668) before building; 0026E7D0 builds a second context at 0209A668")
D = {a: (m, o) for a, m, o in body(0x26EDB0, 0x42)}
check("L3", D[0x26EDBA] == ("mov", "rax, qword ptr [rcx + 0x128]") and D[0x26EDC9] == ("call", "rax") and D[0x26EDCB] == ("add", "rbx, 0x40")
      and D[0x26EDCF] == ("mov", "edi, 2") and D[0x26EDD7] == ("call", "0x16d6a0") and D[0x26EDDC] == ("add", "rbx, 0x68")
      and d[off(0x16D6A0):off(0x16D6A0) + 3] == b"\xc2\x00\x00",
      "0026EDB0: call [+0x128], then 0016D6A0 (ret 0) on the two 0x68 records at +0x40")
check("L4", at(0x2F6B2E)[0] == "lea" and at(0x2F6B2E)[2] == 0x2F5450 and at(0x2F6B35)[:2] == ("mov", "qword ptr [rsi + 0x128], rax"),
      "the constructor stores 002F5450 at +0x128")
T = body(0x2F5450, 229)
freed = [o for a, m, o in T if m == "lea" and re.match(r"r(cx|bx), \[rdi \+", o)]
check("L5", [int(re.search(r"0x[0-9a-f]+", o).group(0), 16) for o in freed] == [0x1D8, 0x1E0, 0x1C8, 0x1D0, 0x210, 0x1C0, 0x218]
      and ("lea", "rcx, [rbx + 8]") in [(m, o) for a, m, o in T]
      and sum(1 for a, m, o in T if (m, o) == ("call", "0x3ec8a0")) == 9
      and ("imul", "rcx, rax, 0xe0") in [(m, o) for a, m, o in T] and ("mov", "esi, 2") in [(m, o) for a, m, o in T]
      and ("mov", "ecx, dword ptr [rcx + 0x168]") in [(m, o) for a, m, o in T] and ("call", "0x3eca70") in [(m, o) for a, m, o in T]
      and ("mov", "rcx, qword ptr [rdi + 0x150]") in [(m, o) for a, m, o in T]
      and ("call", "0x3697f0") in [(m, o) for a, m, o in body(0x3EC8A0, 0x23)],
      "002F5450 frees +0x1D8, the per-record +0xC0 blocks, the +0x1E0/+0x1E8 pairs, +0x1C8, +0x1D0, +0x210, +0x1C0, +0x218")
check("L6", at(0x2F6F4F)[:2] == ("mov", "ecx, 6") and at(0x2F6F54)[:2] == ("imul", "edx, r15d, 0x70") and at(0x2F6F5D)[:2] == ("call", "0x3ec8d0")
      and at(0x2F6F76)[:2] == ("mov", "qword ptr [rsi + 0x1c0], rax"), "+0x1C0 holds 003EC8D0(6, count * 0x70)")
TY = os.path.join(DB, "_types", "types.tsv"); FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/lgs-context-lifetime/lgs_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "LegacyPs2GsTextureContext" and "0209A668" not in c[3]:
            c[3] += (" || A SECOND INSTANCE (2026-09-28, OPUS, %s L2): 0026E7D0 builds another 0x240 context and stores it at 0209A668 "
                     "(0026E841), after releasing both cells" % REC)
            c[6] = ("~~" + c[6] + "~~ RELEASED BY THE NEXT BUILD (2026-09-28, OPUS, %s L1-L5): each builder first calls the destroy-cell "
                    "helper 003EC860(&cell, 0026EDB0) (0026E77B on 0209A670; 0026E7E7 / 0026E804 on 0209A670 / 0209A668), which "
                    "runs the destructor 0026EDB0, frees the block through 003697F0 and nulls the cell. 0026EDB0 calls the "
                    "teardown callback at +0x128 (002F5450, stored by the constructor) - which frees the owned blocks at +0x1C0 / "
                    "+0x1C8 / +0x1D0 (and each record's +0xC0) / +0x1D8 / +0x1E0 / +0x1E8 / +0x210 / +0x218 and releases +0x168 / "
                    "+0x150 - then the two chunk records' no-op destructor 0016D6A0. 0026E20C's null store is a separate "
                    "defaults reset, not the release" % REC)
            tl[i] = "\t".join(c) + e
        if c[0] == "LegacyPs2GsNestedChunkRecord68" and "0016D6A0" not in c[6]:
            c[6] = ("0016D6A0, the ICF-folded `ret 0`, run on each element by the context's destructor 0026EDB0 (0026EDD7): it "
                    "releases nothing, and the chunk pointers are borrowed from the pack (2026-09-28, OPUS, %s L3)" % REC)
            tl[i] = "\t".join(c) + e
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] != "LegacyPs2GsTextureContext": continue
        o = int(c[1], 16)
        if o == 0x128 and "TEARDOWN CALLBACK" not in c[5]:
            c[5] += (" || TEARDOWN CALLBACK (2026-09-28, OPUS, %s L3 L4): the constructor stores 002F5450 here (002F6B2E / 002F6B35) "
                     "and the destructor 0026EDB0 calls it first; 002F5450 frees the context's owned blocks" % REC)
            fl[i] = "\t".join(c) + e
        if o == 0x1C0 and c[4] == "uint64":
            c[4] = "void*"; c[3] = "ownedBlock01C0"
            c[5] = ("~~" + c[5] + "~~ AN OWNED HEAP POINTER (corrected 2026-09-28, OPUS, %s L5 L6): 002F6F5D allocates count * 0x70 "
                    "through 003EC8D0 (tag 6) and 002F6F76 stores it here; the teardown 002F5450 frees it (002F5504 / 003EC8A0). The "
                    "one `add rbx, [rdx+0x1c0]` read uses it as a base. The map-ctrl-pack page describes the same 0x70-stride "
                    "allocation" % REC)
            c[8] += " || CORRECTED 2026-09-28 (OPUS, %s): WAS addend01C0 uint64, 'ADDRESS TERM, NOT A POINTER' (OPUS 2026-09-19)" % REC
            fl[i] = "\t".join(c) + e
        if o in (0x1C8, 0x1D0, 0x1D8, 0x210, 0x218) and "RELEASED BY 002F5450" not in c[5]:
            c[5] += " || RELEASED BY 002F5450 through 003EC8A0 (2026-09-28, OPUS, %s L5)" % REC
            fl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
f = {int(cells(l)[1], 16): cells(l) for l in fl if cells(l)[0] == "LegacyPs2GsTextureContext"}
check("S", all(k in t["LegacyPs2GsTextureContext"][6] for k in ("003EC860", "0026EDB0", "002F5450")) and "0209A668" in t["LegacyPs2GsTextureContext"][3]
      and f[0x1C0][4] == "void*", "the store names the release chain, the second instance and +0x1C0 as a pointer")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
