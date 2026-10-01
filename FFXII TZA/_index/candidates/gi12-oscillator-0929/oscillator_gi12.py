"""GI-12 checks for the per-model oscillator page (FABLE 2026-09-29). Static, shipping image only; exits 1 on any FAIL.

C1  rig frame 003E00C0: every direct call is attributed to the rig slot whose encoded id was last loaded into ecx
    from the rig register (`mov ecx, dword ptr [rdi + OFF]`, controller = OFF / 4). Prints the map as TSV and checks
    the solve order 10,8,1,2,9,11,13,15,14,5,5,16,6,7,12,3,16 and the apply order 11,10,2,9,13,15,8,1,14,5,12,7,3,6
    (the rig page's order plus controller 6 at the end), and that exactly the three applies after the
    display-deny test at 003E0680 are controllers 7, 3 and 6 (the regression for the 2026-09-29 correction:
    "the last TWO applies" would print 2 here).
C2  02B59D60 has no writer: no rip-relative write to [02B59D60, 02B59D64) in any listed function and no
    image-base-relative displacement 0x2A39D60..0x2A39D63. Positive controls: the same rip scan finds the one
    writer of 02B59D68 (003E0B40) and the displacement scan finds `[rbx + 0x29ca030]` (003B6181).
C3  writers of 02CA4380..02CA43A0 are exactly 0040B3B0, 0040AAD0 and 0040DB70.
C4  wind preset table 01EFFA30: six 0x20-byte entries decoded (preset n at 01EFFA30 + (n-1) * 0x20).
C5  raw E8/E9 callers of 0054B1F0 are exactly the sites inside 0052B5E0 and 0052BBD0; raw callers of the
    wind setter 0040AAD0 are 002E3D40, 002EAA60 and 002EAB40.
"""
import struct, sys, re, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    name = d[o:o + 8].rstrip(b"\0")
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, va, ro, rs))
text = [s for s in secs if s[0] == b".text"][0]


def off(va):
    rva = va - BASE
    for _n, a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


funcs = {}
for ln in open(FUNCS, encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    if p[0] == "entry":
        continue
    funcs[int(p[0], 16)] = int(p[2])
starts = sorted(funcs)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
fails = []


def body(fn):
    o = off(fn)
    return md.disasm(d[o:o + funcs[fn]], fn)


def containing(a):
    i = bisect.bisect_right(starts, a) - 1
    return starts[i] if i >= 0 and a < starts[i] + funcs[starts[i]] else None


# C1
last = None
calls = []
for x in body(0x003E00C0):
    if x.mnemonic == "mov" and x.op_str.startswith("ecx, "):
        m = re.match(r"dword ptr \[rdi(?: \+ (0x[0-9a-f]+|[0-9]+))?\]$", x.op_str[5:])
        if m:
            last = int(m.group(1), 0) if m.group(1) else 0
            continue
    if x.mnemonic == "call" and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if t != 0x20E600:
            calls.append((x.address, t, last))
print("site\tcallee\tcontroller")
for a, t, s in calls:
    print("%08X\t%08X\t%s" % (a, t, "-" if s is None else s // 4))
ctl = [(a, t, s // 4) for a, t, s in calls if s is not None and t >= 0x00471000 and a > 0x003E0170]
solve = [c for a, t, c in ctl if a < 0x003E04A0]
apply_ = [c for a, t, c in ctl if a >= 0x003E04A0]
want_solve = [10, 8, 1, 2, 9, 11, 13, 15, 14, 5, 5, 16, 6, 7, 12, 3, 16]
want_apply = [11, 10, 2, 9, 13, 15, 8, 1, 14, 5, 12, 7, 3, 6]
print("C1 solve", solve, "OK" if solve == want_solve else "FAIL")
print("C1 apply", apply_, "OK" if apply_ == want_apply else "FAIL")
after_gate = [c for a, t, c in ctl if a > 0x003E0680]
print("C1 applies behind the display-deny test at 003E0680:", after_gate, "OK" if after_gate == [7, 3, 6] else "FAIL")
if solve != want_solve or apply_ != want_apply or after_gate != [7, 3, 6]:
    fails.append("C1")


# C2 / C3 rip-relative writes over every listed function
def rip_writes(lo, hi):
    out = []
    for fn in starts:
        if not (text[1] <= fn - BASE < text[1] + text[3]):
            continue
        for x in body(fn):
            if len(x.operands) < 1:
                continue
            op0 = x.operands[0]
            if op0.type == X86_OP_MEM and op0.mem.base != 0 and x.reg_name(op0.mem.base) == "rip":
                t = x.address + x.size + op0.mem.disp
                if lo <= t < hi and x.mnemonic not in ("cmp", "test", "lea", "push"):
                    out.append((x.address, fn, t, x.mnemonic))
    return out


w60 = rip_writes(0x02B59D60, 0x02B59D64)
w68 = rip_writes(0x02B59D68, 0x02B59D6C)
print("C2 rip writes to 02B59D60:", w60, "OK" if not w60 else "FAIL")
print("C2 control, writers of 02B59D68:", ["%08X in %08X" % (a, f) for a, f, t, m in w68],
      "OK" if [f for a, f, t, m in w68] == [0x003E0B40] else "FAIL")
disp_hits, ctl_hits = [], []
for fn in starts:
    if not (text[1] <= fn - BASE < text[1] + text[3]):
        continue
    for x in body(fn):
        for op in x.operands:
            if op.type == X86_OP_MEM:
                if 0x2A39D60 <= op.mem.disp < 0x2A39D64:
                    disp_hits.append(x.address)
                if op.mem.disp == 0x29CA030:
                    ctl_hits.append(x.address)
print("C2 image-base-relative disp 0x2A39D60:", disp_hits, "OK" if not disp_hits else "FAIL")
print("C2 control disp 0x29CA030 hits:", ["%08X" % a for a in ctl_hits], "OK" if ctl_hits else "FAIL")
if w60 or disp_hits or not ctl_hits or [f for a, f, t, m in w68] != [0x003E0B40]:
    fails.append("C2")
w43 = rip_writes(0x02CA4380, 0x02CA43A0)
wf = sorted({f for a, f, t, m in w43})
print("C3 writers of 02CA4380..02CA43A0:", ["%08X" % f for f in wf],
      "OK" if wf == [0x0040AAD0, 0x0040B3B0, 0x0040DB70] else "FAIL")
if wf != [0x0040AAD0, 0x0040B3B0, 0x0040DB70]:
    fails.append("C3")

# C4
names = ["->02CA4388", "amp base ->02CA4380", "amp rand ->02CA4384", "speed base ->02CA4398",
         "speed rand ->02CA439C", "->02CA438C"]
print("C4 preset\t" + "\t".join(names) + "\tmode ->02CA4394")
for p in range(1, 7):
    o = off(0x01EFFA30 + (p - 1) * 0x20)
    f = struct.unpack_from("<6f", d, o)
    i = struct.unpack_from("<i", d, o + 0x18)[0]
    print("C4 %d\t%s\t%d" % (p, "\t".join("%.4g" % v for v in f), i))


# C5 raw E8/E9 callers
def raw_callers(tgt):
    out = []
    lo, hi = off(BASE + text[1]), off(BASE + text[1]) + text[3]
    for i in range(lo, hi - 5):
        if d[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", d, i + 1)[0]
            src = BASE + text[1] + (i - lo)
            if src + 5 + rel == tgt:
                out.append((src, containing(src)))
    return out


c1 = raw_callers(0x0054B1F0)
print("C5 callers of 0054B1F0:", ["%08X in %s" % (a, "%08X" % f if f else "?") for a, f in c1])
if sorted({f for a, f in c1}) != [0x0052B5E0, 0x0052BBD0]:
    fails.append("C5a")
c2 = raw_callers(0x0040AAD0)
print("C5 callers of 0040AAD0:", ["%08X in %s" % (a, "%08X" % f if f else "?") for a, f in c2])
if sorted({f for a, f in c2}) != [0x002E3D40, 0x002EAA60, 0x002EAB40]:
    fails.append("C5b")
print("FAILS", len(fails), fails)
sys.exit(1 if fails else 0)
