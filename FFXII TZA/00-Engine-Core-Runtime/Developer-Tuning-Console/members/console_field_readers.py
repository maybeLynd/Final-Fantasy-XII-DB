# console_field_readers.py (FABLE, Claude Opus 5.5, 2026-09-25)
# Readers of the developer console's settings singleton (0x10E8 bytes, cell 01F81428, getter 001D50D0) outside the
# console, the menu renderer and the defaults builder, WITH A RECEIVER CHECK. Seeds: every function that calls
# 001D50D0 (raw call index) or loads [01F81428] rip-relatively. For each [reg + off] access at a requested offset,
# the base register is traced backwards within the function (up to 40 instructions, through register moves) to
# its definition; the access is counted only if that definition is the getter's rax or a load of the cell.
# Excluded by address: 001CD0E0 (DebugMenu_Render - prints values), 001D1660 (console arm), 001CCB20 (defaults).
# Blind spot (stated, not fixed): a function that receives the object as an argument is not a seed.
# Usage: console_field_readers.py 0xC20 0xC71 ...    Control: +0xC34 must report 0017D360 (UQ-18).
import struct, capstone, json, bisect, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUN = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
RAW = os.path.join(ROOT, "Tools", "work", "FABLE", "pub140-scratch", "tools", "rawcalls.json")
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
vs, va, rs, ro = struct.unpack_from("<IIII", d, pe + 24 + opt + 8)
off = lambda v: ro + v - 0x120000 - va
F = []
for l in open(FUN, encoding="utf-8"):
    p = l.split("\t")
    try:
        F.append((int(p[0], 16), int(p[2]), p[1]))
    except (ValueError, IndexError):
        pass
F.sort(); E = [f[0] for f in F]; SZ = {f[0]: f[1] for f in F}; NM = {f[0]: f[2] for f in F}
def owner(a):
    k = bisect.bisect_right(E, a) - 1
    return F[k][0] if k >= 0 and a < F[k][0] + F[k][1] else None
raw = json.load(open(RAW))
seeds = set()
for k, v in raw.items():
    if int(k, 16) == 0x1D50D0:
        seeds |= {owner(int(a, 16)) for a in v}
for fe, n, nm in F:
    if 0 < n < 300000:
        b = d[off(fe):off(fe) + n]
        for i in range(len(b) - 7):
            if b[i] in (0x48, 0x4C) and b[i + 1] == 0x8B and (b[i + 2] & 0xC7) == 0x05 and \
               fe + i + 7 + struct.unpack_from("<i", b, i + 3)[0] == 0x01F81428:
                seeds.add(fe)
seeds.discard(None)
EXCL = {0x1CD0E0, 0x1D1660, 0x1CCB20}
OFFS = [int(x, 16) for x in sys.argv[1:]] or [0xC34]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
REG64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
def norm(r):
    return REG64.get(r, r)
def origin(ins, k, reg):
    reg = norm(reg)
    for j in range(k - 1, max(k - 40, -1), -1):
        x = ins[j]
        if x.mnemonic == "call":
            if reg == "rax":
                return "GETTER" if x.op_str == "0x1d50d0" else "call " + x.op_str
            if reg in ("rcx", "rdx", "r8", "r9", "r10", "r11"):
                return "clobbered by call"
            continue
        ops = x.op_str.split(", ")
        if x.mnemonic in ("mov", "lea") and len(ops) == 2 and norm(ops[0]) == reg:
            src = ops[1]
            if "rip +" in src:
                t = x.address + x.size + int(src.split("rip + ")[1].split("]")[0], 16)
                return "CELL" if t == 0x01F81428 else "rip %08X" % t
            if src in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
                reg = src
                continue
            return "%s %s" % (x.mnemonic, src)
    return "unresolved"
res = {}
for fe in sorted(seeds):
    if fe in EXCL:
        continue
    ins = list(md.disasm(d[off(fe):off(fe) + SZ[fe]], fe))
    for k, i in enumerate(ins):
        for o in OFFS:
            tag = "+ 0x%x]" % o
            if tag in i.op_str and "rip" not in i.op_str and "rsp" not in i.op_str:
                base = i.op_str.split("[")[1].split(" ")[0]
                org = origin(ins, k, base)
                res.setdefault(o, []).append((fe, i.address, i.mnemonic, i.op_str, org))
print("seed functions:", len(seeds))
for o in OFFS:
    good = [r for r in res.get(o, []) if r[4] in ("GETTER", "CELL")]
    bad = [r for r in res.get(o, []) if r[4] not in ("GETTER", "CELL")]
    print("+0x%03X  readers: %s" % (o, ", ".join("%08X@%08X %s" % (r[0], r[1], r[2]) for r in good) or "none"))
    if bad:
        print("        rejected: %s" % ", ".join("%08X@%08X(%s)" % (r[0], r[1], r[4]) for r in bad))
