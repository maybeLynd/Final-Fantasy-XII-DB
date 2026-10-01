"""Census of the bank-local index handed to the two handle-A play wrappers.

For every direct call/jmp to 00249C60 or 00249CA0 inside a listed function, walk back at most 12
instructions for the last write to ecx and keep it when it is an immediate. Join each immediate to the
slot table of se000.seb (i32[128] at +0x10, -1 = empty), the bank handle A names.
"""
import struct, sys, collections, bisect
import capstone

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work"
EXE = ROOT + r"\exe\FFXII_TZA.exe"
FUNCS = ROOT + r"\graph\functions.tsv"
SEB = r"D:\FFXII_TZA_extract\ps2data\sound\se\block\se000.seb"
BASE = 0x120000
TARGETS = {0x00249C60, 0x00249CA0}

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vs, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, s, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        a = int(p[0], 16); n = int(p[2])
    except (ValueError, IndexError):
        continue
    funcs.append((a, n, p[1], p[3] if len(p) > 3 else ""))

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
rows = []
for a, n, name, owner in funcs:
    fo = off(a)
    if fo is None or a in TARGETS:
        continue
    code = d[fo:fo + n]
    # cheap prefilter: any E8/E9 rel32 landing on a target
    hit = False
    for i in range(len(code) - 4):
        if code[i] in (0xE8, 0xE9):
            t = a + i + 5 + struct.unpack_from("<i", code, i + 1)[0]
            if t in TARGETS:
                hit = True
                break
    if not hit:
        continue
    ins = list(md.disasm(code, a))
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp"):
            continue
        try:
            t = int(x.op_str, 16)
        except ValueError:
            continue
        if t not in TARGETS:
            continue
        imm = None
        for y in reversed(ins[max(0, k - 12):k]):
            ops = y.op_str.split(",")
            dst = ops[0].strip()
            if dst in ("ecx", "rcx", "cl", "cx"):
                if y.mnemonic == "mov" and len(ops) == 2:
                    s = ops[1].strip()
                    try:
                        imm = int(s, 16) if s.startswith("0x") else int(s)
                    except ValueError:
                        imm = None
                elif y.mnemonic == "xor" and ops[1].strip() == dst:
                    imm = 0
                break
        rows.append((a, x.address, t, imm, owner))

seb = open(SEB, "rb").read()
slots = struct.unpack_from("<128i", seb, 0x10)
filled = {i for i, v in enumerate(slots) if v != -1}

print("# sites", len(rows), "immediate", sum(1 for r in rows if r[3] is not None),
      "computed", sum(1 for r in rows if r[3] is None), "callers", len({r[0] for r in rows}))
print("# se000.seb filled slots", len(filled), "max", max(filled))
by = collections.defaultdict(list)
for r in rows:
    if r[3] is not None:
        by[r[3]].append(r)
print("index\tsites\tin_se000\towners")
for imm in sorted(by):
    own = collections.Counter(r[4] for r in by[imm])
    print("0x%02X\t%d\t%s\t%s" % (imm, len(by[imm]), "yes" if imm in filled else "NO",
                                  ", ".join("%s %d" % kv for kv in sorted(own.items(), key=lambda kv: (-kv[1], kv[0])))))
