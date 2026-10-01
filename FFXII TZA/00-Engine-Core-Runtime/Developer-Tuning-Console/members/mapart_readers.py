# (FABLE, Claude Opus 5.5, 2026-09-25) - published copy; runs from any working directory.
# mapart_readers.py - who reads the map-art context's +0x2D0..+0x304 floats (UQ-15). Seeds: functions calling the getter
# 001A9930 (raw call index) and functions loading [01F81168] rip-relatively. In each seed, every memory operand
# [reg + off] with off in 0x2D0..0x304 is listed with mnemonic and width. Control: the console arm function (the
# one containing 001D2E18) must appear with a write to +0x2D0.
import struct, capstone, json, bisect
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
vs, va, rs, ro = struct.unpack_from("<IIII", d, pe + 24 + opt + 8)
off = lambda v: ro + v - 0x120000 - va
F = []
for l in open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8"):
    p = l.split("\t")
    try:
        F.append((int(p[0], 16), int(p[2]), p[1]))
    except (ValueError, IndexError):
        pass
F.sort(); E = [f[0] for f in F]; NM = {f[0]: f[2] for f in F}; SZ = {f[0]: f[1] for f in F}
def owner(a):
    k = bisect.bisect_right(E, a) - 1
    return F[k][0] if k >= 0 and a < F[k][0] + F[k][1] else None
raw = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
seeds = set()
for k, v in raw.items():
    if int(k, 16) == 0x1A9930:
        seeds |= {owner(int(a, 16)) for a in v}
for fe, n, nm in F:
    if n <= 0 or n > 300000:
        continue
    b = d[off(fe):off(fe) + n]
    for i in range(len(b) - 7):
        if b[i] in (0x48, 0x4C) and b[i + 1] == 0x8B and (b[i + 2] & 0xC7) == 0x05:
            if fe + i + 7 + struct.unpack_from("<i", b, i + 3)[0] == 0x01F81168:
                seeds.add(fe)
seeds.discard(None)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
rows = []
for fe in sorted(seeds):
    for ins in md.disasm(d[off(fe):off(fe) + SZ[fe]], fe):
        for o in range(0x2D0, 0x308, 4):
            if ("+ 0x%x]" % o) in ins.op_str and "rsp" not in ins.op_str and "rip" not in ins.op_str and "rbp" not in ins.op_str:
                w = "write" if ins.op_str.startswith(("dword ptr", "qword ptr", "xmmword ptr")) and ins.mnemonic in ("movss", "mov", "movups", "movaps", "movsd", "movq") else "read/rmw"
                rows.append((fe, NM[fe], ins.address, ins.mnemonic, ins.op_str, o, w))
print("seed functions:", len(seeds))
ctl = [r for r in rows if r[0] <= 0x1D2E18 < r[0] + SZ[r[0]] and r[5] == 0x2D0]
print("control (console arm touching +0x2D0):", "PASS" if ctl else "FAIL")
for r in rows:
    if r[0] <= 0x1D2E18 < r[0] + SZ[r[0]]:
        continue
    print("%08X %-40s %08X %-7s %-40s +0x%X %s" % r)
