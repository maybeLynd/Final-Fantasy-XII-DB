"""bank090_split.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

CharacterLightingTuningBank (static 02CB80A0, 0xC0) +0x90 was one 8-byte row 'mixed090' - one field or two NOT resolved -
because 001D1660 stores a qword there once. Every other access is 4 bytes wide:
  W  a whole-image census of rip-relative operands into 02CB8130..02CB8137 (every body in functions.tsv): all are 4-byte
     movss at +0x90 or +0x94, except ONE `mov qword ptr [+0x90], 0` at 001D194F, followed by `mov dword ptr [+0x98], 0`
     at 001D195A - a zero-initialisation of consecutive float cells, not an 8-byte field
  U  the only other mover, 006084B0's copy of the bank (rax = 02CB80A0), moves it in 16-byte units at +0x80 / +0x90 /
     +0xA0 / +0xB0, which never divide +0x90 from +0x94
  K  the console catalogue maps id 108 'Diffuse intensity:' to 02CB8130 and id 109 'Specular intensity:' to 02CB8134,
     beside id 110 'Cube map intensity:' at 02CB8138 (the store's cubeMapIntensity +0x98)
  S  REGRESSION: the store has +0x90 float and +0x94 float and no 8-byte row at +0x90 (FAILS before the patch)
Usage: python bank090_split.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.abspath(os.path.join(DB, ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
FIELDS = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/lighting-bank-090/bank090_split.py"
B = 0x120000; BANK = 0x2CB80A0
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
idx = [i for i, l in enumerate(fl) if cells(l)[0] == "CharacterLightingTuningBank" and cells(l)[1] == "0x090"]

if "--patch" in sys.argv:
    i = idx[0]; c = cells(fl[i]); eol = fl[i][len(fl[i].rstrip("\r\n")):]
    if c[4] == "float": print("already"); sys.exit(0)
    w = len(c)
    def row(o, name, mean): return "\t".join(["CharacterLightingTuningBank", o, "4", name, "float", mean, "SEMANTICALLY IDENTIFIED",
        "PROVEN", "SPLIT 2026-09-28 (OPUS, %s W U K): every access is a 4-byte movss except one qword zero-init. || WAS 0x090 8 "
        "mixed090 u8[8]: %s || %s" % (REC, c[5], c[8])] + [""] * (w - 9)) + eol
    fl[i:i + 1] = [row("0x090", "diffuseIntensity", "console id 108 'Diffuse intensity:' (02CB8130) - stepped as a float by "
                       "001D1660 (001D1FE6 / 001D1FFA / 001D200F) and displayed by 001CD0E0 (001CE60F). FABLE 2026-09-18: a "
                       "float that id 28 does not own"),
                   row("0x094", "specularIntensity", "console id 109 'Specular intensity:' (02CB8134) - stepped as a float by "
                       "001D1660 (001D201C / 001D2030 / 001D2045) and displayed by 001CD0E0 (001CE619)")]
    open(FIELDS, "wb").write("".join(fl).encode("utf-8")); print("split +0x90 into two float rows"); sys.exit(0)

sizes = {}
for l in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8"):
    x = l.split("\t")
    try: sizes[int(x[0], 16)] = int(x[2])
    except (ValueError, IndexError): pass
acc = []
for f, s in sorted(sizes.items()):
    o = off(f) if 0x121000 <= f < 0x900000 else None
    if o is None or s <= 0: continue
    for x in cs.disasm(d[o:o + s], f):
        for op in x.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = x.address + x.size + op.mem.disp
                if t < BANK + 0x98 and t + op.size > BANK + 0x90:
                    acc.append((x.address, t - BANK, op.size, x.mnemonic, x.op_str))
odd = [a for a in acc if not (a[2] == 4 and a[3] == "movss" and a[1] in (0x90, 0x94))]
check("W", len(acc) == 13 and odd == [(0x1D194F, 0x90, 8, "mov", "qword ptr [rip + 0x2ae67d6], 0")],
      "%d rip-relative accesses into +0x90..+0x97; the only non-movss one: %s" % (len(acc), [("%08X" % a[0], hex(a[1]), a[2]) for a in odd]))
z = next(cs.disasm(d[off(0x1D195A):off(0x1D195A) + 16], 0x1D195A))
check("W2", (z.mnemonic, z.op_str) == ("mov", "dword ptr [rip + 0x2ae67d4], 0") and z.address + z.size + 0x2ae67d4 == BANK + 0x98,
      "001D195A zeroes +0x98 right after: the qword is an initialisation of float cells")
u = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x60887E):off(0x60887E) + 0x120], 0x60887E)}
check("U", u.get(0x60887E) == ("lea", "rdx, [rip + 0x26af74b]") and 0x60887E + 7 + 0x26af74b + 0xD0 == BANK
      and u.get(0x608888) == ("lea", "rax, [rdx + 0xd0]")
      and all(u.get(a) == ("movups", "xmm%d, xmmword ptr [rax + %s]" % (r, k)) for a, r, k in
              ((0x60895A, 0, "0x80"), (0x608968, 1, "0x90"), (0x608976, 0, "0xa0"), (0x608984, 1, "0xb0"))),
      "006084B0 copies the bank in 16-byte units at +0x80 / +0x90 / +0xA0 / +0xB0")
page = open(os.path.join(DB, "00-Engine-Core-Runtime", "Developer-Tuning-Console", "console-command-names.md"), encoding="utf-8").read()
check("K", re.search(r"\| 108 \| Diffuse intensity: \|[^\n]*`02CB8130` \|", page) is not None
      and re.search(r"\| 109 \| Specular intensity: \|[^\n]*`02CB8134` \|", page) is not None
      and re.search(r"\| 110 \| Cube map intensity: \|[^\n]*`02CB8138` \|", page) is not None,
      "console ids 108 / 109 / 110 at 02CB8130 / 02CB8134 / 02CB8138")
F = {cells(l)[1]: cells(l) for l in fl if cells(l)[0] == "CharacterLightingTuningBank"}
check("S", F.get("0x090", [0] * 5)[4] == "float" and F["0x090"][2] == "4" and F.get("0x094", [0] * 5)[4] == "float",
      "+0x90 and +0x94 are float rows (the store has %s)" % (F.get("0x090", [0] * 5)[2:5]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
