"""image_ref_domain.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Consumes
ASTRA-RETURN-OPUS-REFERENCE-INVERSE-DOMAIN (_experiments/evidence/image-reference-roundtrip-domain/).

  D1 the two leaves over the base cell 01F83530: decode 0020E600 = mov eax, ecx (zero-extends) / add rax, qword [01F83530]
     (0020E602) / ret; encode 0020E620 = sub ecx, dword [01F83530] (0020E620, the DWORD read) / mov eax, ecx (0020E626) / ret.
     So the base's two readers are 0020E602 (qword) and 0020E620 (dword) - 0020E626 is the `mov`, not a read
  D2 the domain (modular, for a stable base B): encode(decode(u)) = u for every u32 u; decode(encode(p)) = p only when
     (p - B) mod 2^64 < 2^32 - a 4 GiB window above B; p and p + 2^32 encode the same; decode(0) = B, so there is no null
     rule in the leaves. Checked on selected values, not native or live observations
  S  REGRESSION: ImageRelativeReferenceBase's row cites 0020E620 for the dword read and states the window (FAILS before)
Usage: python image_ref_domain.py [--patch]
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def body(a, k): return [x for x in cs.disasm(d[off(a):off(a) + 16], a)][:k]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
dec = body(0x20E600, 3); enc = body(0x20E620, 3)
rip = lambda x: x.address + x.size + x.operands[-1].mem.disp
ok1 = ([(x.mnemonic, x.op_str.split(" [")[0]) for x in dec] == [("mov", "eax, ecx"), ("add", "rax, qword ptr"), ("ret", "")]
       and rip(dec[1]) == 0x1F83530 and dec[1].address == 0x20E602
       and [(x.mnemonic, x.op_str.split(" [")[0]) for x in enc] == [("sub", "ecx, dword ptr"), ("mov", "eax, ecx"), ("ret", "")]
       and rip(enc[0]) == 0x1F83530 and enc[0].address == 0x20E620 and enc[1].address == 0x20E626)
check("D1", ok1, "readers of 01F83530: 0020E602 (qword add) and 0020E620 (dword sub); 0020E626 is `mov eax, ecx`")
M64, M32 = (1 << 64) - 1, (1 << 32) - 1
D = lambda Bs, u: (Bs + (u & M32)) & M64
E = lambda Bs, p: ((p & M32) - (Bs & M32)) & M32
Bs = 0x0000_7FF6_1234_0000
ok2 = (all(E(Bs, D(Bs, u)) == u for u in (0, 1, 0x7FFFFFFF, 0xFFFFFFFF))
       and D(Bs, E(Bs, Bs + 0x10)) == Bs + 0x10 and D(Bs, E(Bs, Bs + M32)) == Bs + M32
       and D(Bs, E(Bs, Bs + (1 << 32))) != Bs + (1 << 32) and E(Bs, Bs + 5) == E(Bs, Bs + 5 + (1 << 32))
       and D(Bs, 0) == Bs)
check("D2", ok2, "encode(decode(u)) = u; decode(encode(p)) = p only within [B, B + 2^32); decode(0) = B")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/image-reference-domain/image_ref_domain.py"
fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "ImageRelativeReferenceBase" and c[1] == "0x000" and "0020E620" not in c[8]:
            c[8] = c[8].replace("0020E626 (dword)", "~~0020E626 (dword)~~ 0020E620 (dword, the `sub`; 0020E626 is `mov eax, ecx` - corrected 2026-09-28, OPUS, %s D1)" % REC)
            c[5] += (" || DOMAIN 2026-09-28 (OPUS, %s D2; ASTRA image-reference-roundtrip-domain): decode 0020E600 adds a zero-extended "
                     "u32 to the base, encode 0020E620 subtracts the base's low 32 bits. For a stable base B they are exact inverses "
                     "only inside [B, B + 2^32): outside it, p and p + 2^32 encode the same. decode(0) = B, so the leaves have no "
                     "null rule. Whether B is the module base, and what callers pass, is not established here" % REC)
            fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
row = next(cells(l) for l in fl if cells(l)[0] == "ImageRelativeReferenceBase" and cells(l)[1] == "0x000")
check("S", "0020E620 (dword" in row[8] and "B + 2^32" in row[5], "the row cites 0020E620 and states the window")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
