"""created_flag_scope.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Narrows OPUS's own 2026-09-27 rows.

Four resourcesCreated rows (PTexture2DD3D11 +0xBC, PTexture3DD3D11 +0x8C, PTextureCubeMapD3D11 +0xA4, PConstantBufferD3D11 +0x48)
say 'the release is skipped while it is 0'. That holds on the routes that test it, not in general:
  G  the testers are one-instruction getters (cmp dword [rcx+off], 0 / setne al): 00625F00 +0xBC, 00625F10 +0x8C, 00625F20 +0xA4,
     00625EC0 +0x48; and the tested routes branch on them: 006505A0 (00650633 / 0065063A je / 00650648 jmp 0062BCB0; 00650609 ->
     0062BF40; 006505DE -> 0062C100) and 005D14D5 / 005D14DC je / 005D14E1 call 0062B7B0
  U  the release passes 0062BCB0 / 0062BF40 / 0062C100 / 0062B7B0 never read the flag - their one access to it is the store of 0 -
     and each class destroy (00611F80 / 00610EC0 / 00612B20 / 00611AD0, element_release.py O) calls its pass with no test
  So the flag gates the release on some routes; the destroy releases regardless (the passes' null checks skip empty slots).
  The other direct callers of the passes are not classified here.
  S  REGRESSION: the four rows no longer state the skip unqualified, and name the untested destroy (FAILS before)
Usage: python created_flag_scope.py [--patch]
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
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
def body(a, lim=0x800):
    out = []
    for x in cs.disasm(d[off(a):off(a) + lim], a):
        out.append((x.address, x.mnemonic, x.op_str))
        if x.mnemonic in ("ret", "int3") and x.address > a + 0x10: break
    return out
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
# type, flag offset, getter, release pass, destroy, (route call, je, route transfer)
C = [("PTexture2DD3D11", 0xBC, 0x625F00, 0x62BCB0, 0x611F80, (0x650633, 0x65063A, 0x650648)),
     ("PTexture3DD3D11", 0x8C, 0x625F10, 0x62BF40, 0x610EC0, (0x650609, 0x650610, 0x65061E)),
     ("PTextureCubeMapD3D11", 0xA4, 0x625F20, 0x62C100, 0x612B20, (0x6505DE, 0x6505E5, 0x6505F3)),
     ("PConstantBufferD3D11", 0x48, 0x625EC0, 0x62B7B0, 0x611AD0, (0x5D14D5, 0x5D14DC, 0x5D14E1))]
g = all(at(gt) == ("cmp", "dword ptr [rcx + 0x%x], 0" % fo) and at(gt + 7 if fo > 0x7F else gt + 4)[0] == "setne"
        and at(rc) == ("call", "0x%x" % gt) and at(je)[0] == "je" and at(tr)[1] == "0x%x" % rp for t, fo, gt, rp, dt, (rc, je, tr) in C)
check("G", g, "getters test the flag; 006505A0 and 005D14D5 branch on them before the pass")
u = []
for t, fo, gt, rp, dt, _ in C:
    acc = [(m, o) for a, m, o in body(rp) if "+ 0x%x]" % fo in o]
    dcalls = [(m, o) for a, m, o in body(dt) if m in ("call", "cmp", "test")]
    u.append(len(acc) == 1 and acc[0][0] == "mov" and acc[0][1].startswith("dword ptr [rbx + 0x%x], " % fo)
             and dcalls[1] == ("call", "0x%x" % rp) and dcalls[0][0] == "call")
check("U", all(u), "each pass's only flag access is the store of 0; each destroy calls its pass untested %s" % u)
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/d3d11-element-release/created_flag_scope.py"
fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
OLD = "the release is skipped while it is 0"
if "--patch" in sys.argv:
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        k = next((x for x in C if x[0] == c[0] and c[1].startswith("0x") and int(c[1], 16) == x[1]), None)
        if k and c[3] == "resourcesCreated" and c[5].endswith(OLD):
            t, fo, gt, rp, dt, (rc, je, tr) = k
            c[5] = c[5][:-len(OLD)] + ("~~%s~~ routes that test it skip the release while it is 0 (the getter %08X, e.g. %08X), but the "
                                       "release pass %08X never reads it (its one access is the store of 0) and the class destroy %08X "
                                       "calls the pass with no test (narrowed 2026-09-28, OPUS, %s G U); the other direct callers of "
                                       "the pass are not classified" % (OLD, gt, rc, rp, dt, REC))
            c[8] += " || NARROWED 2026-09-28 (OPUS, %s G U): the skip is per route, not a property of the release" % REC
            fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
rows = [cells(l) for l in fl if cells(l)[0] in [x[0] for x in C] and cells(l)[3] == "resourcesCreated"]
check("S", len(rows) == 4 and all(not r[5].endswith(OLD) and "with no test" in r[5] and REC in r[5] for r in rows),
      "the four rows scope the skip to the testing routes and name the untested destroy")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
