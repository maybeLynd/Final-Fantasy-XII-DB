"""HM-1: the executable's letter-to-kind step (OPUS, 2026-09-27). Control. Static, shipping EXE + the PS2 disc file list.

A model id is {u16 number N; u16 ASCII letter}. The engine turns it into a file with 002ED6F0(id, &kind, &index): a
jump table on letter - 'C' (0x43..0x77) sets *kind and *index = stride * N; any other letter takes the default arm.
  K1 the id format, from the engine's own builder: 002EB7A0 returns 0x630000 / 0x6E0001 / 0x770002 - letter << 16 | N
  K2 the decoder's table, read from its jump table and arms: c 14/25, n 19/25, s 23/25, m 34/11, b 22/2, g 13/2,
     C 15/1, N 20/1, S 24/1, M 18/1, t 25/1, w 16/1 (kind/stride); default kind 1, index N; each arm returns stride-1
  K3 the model loader 002E6700 hands the node's id (+0x14) to 002ED6F0 and the resulting (kind, index) to 0032E400,
     the .fst size read size[kind][id] (file-size-tables page), whose kind k is the disc file list's section k (UQ-70)
  K4 in the disc file list every kind K2 names is an exact tiling of stride-sized blocks: a .cm at each block head,
     .ca files elsewhere, one model number per block - so stride * N is the Nth .cm, the reading H4 found from data
  K5 all 22 highmodelreplace.bin records resolved by the engine's rule: the source (lower-case) and every replacement
     (upper-case) land on .cm files of one model number - H2 and H4 now follow from the executable, not from a fit
Not claimed: what callers do with the return value (stride-1, the .ca slots per model); which model the second-skeleton
record holds (HM-1's remaining item).
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
PS2 = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data")
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

ids = [int(x.op_str.split(", ")[1], 16) for x in dis(0x2EB7A0, 52) if x.mnemonic == "mov" and x.op_str.startswith("ecx, 0x")]
check("K1 the engine's id builder: letter << 16 | N", ids == [0x630000, 0x6E0001, 0x770002], str([hex(i) for i in ids]))

def arm(t):
    if t == 0x2ED840: return (1, 1, 1)
    k = m = r = None
    for x in cs.disasm(d[off(t):off(t) + 40], t):
        mm = re.match(r"(e[a-d]x), (0x[0-9a-f]+|\d+)$", x.op_str)
        if x.mnemonic == "mov" and mm:
            v = int(mm.group(2), 0)
            if mm.group(1) == "edx": k = v
            elif mm.group(1) == "ecx": m = v
        if x.mnemonic == "lea" and x.op_str.startswith("eax, [rdx"):
            mm = re.search(r"rdx ([+-]) (0x[0-9a-f]+|\d+)", x.op_str); r = ("+-".index(mm.group(1)), int(mm.group(2), 0))
        if x.mnemonic == "xor" and x.op_str == "eax, eax": r = 0
        if x.mnemonic == "ret": break
    if isinstance(r, tuple): r = k + r[1] if r[0] == 0 else k - r[1]
    return (k, m, r)
head = ["%s %s" % (x.mnemonic, x.op_str) for x in dis(0x2ED6F0, 0x34)]
table = {}
for L in range(0x43, 0x43 + 0x35):
    t = BASE + struct.unpack_from("<i", d, off(BASE + 0x1CD854) + d[off(BASE + 0x1CD888) + L - 0x43] * 4)[0]
    if t != 0x2ED840: table[chr(L)] = arm(t)
WANT = {"c": (14, 25), "n": (19, 25), "s": (23, 25), "m": (34, 11), "b": (22, 2), "g": (13, 2),
        "C": (15, 1), "N": (20, 1), "S": (24, 1), "M": (18, 1), "t": (25, 1), "w": (16, 1)}
check("K2 002ED6F0's jump table: letter -> (kind, stride); each arm returns stride-1; default kind 1",
      head[:4] == ["movzx r10d, cx", "mov r9, rdx", "shr ecx, 0x10", "movzx eax, cl"] and "add eax, -0x43" in head
      and {L: v[:2] for L, v in table.items()} == WANT and all(v[2] == v[1] - 1 for v in table.values())
      and arm(0x2ED840) == (1, 1, 1), str({L: v[:2] for L, v in table.items()}))

ld = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in dis(0x2E6700, 381)}
check("K3 the loader: node id +0x14 -> 002ED6F0(id, &kind, &index) -> 0032E400(kind, index)",
      ld.get(0x2E6739) == "mov edi, dword ptr [rbx + 0x14]" and ld.get(0x2E6753) == "mov ecx, edi"
      and ld.get(0x2E674E) == "lea r8, [rsp + 0x50]" and ld.get(0x2E6755) == "lea rdx, [rsp + 0x58]"
      and ld.get(0x2E675A) == "call 0x2ed6f0" and ld.get(0x2E675F) == "mov ecx, dword ptr [rsp + 0x58]"
      and ld.get(0x2E6773) == "movsxd rdx, eax" and ld.get(0x2E6776) == "call 0x32e400")

fl = (PS2 / "image/ff12/ch/bin/filelistlocalin.bin").read_bytes()
fsecs = struct.unpack_from("<38I", fl, 0)
def sec(k):
    s = fsecs[k]; c = struct.unpack_from("<I", fl, s)[0]
    return [fl[o:fl.index(b"\0", o)].decode("latin1") if o else "" for o in struct.unpack_from("<%dI" % c, fl, s + 4)]
base = lambda p: p.split("\\")[-1]
num = lambda p: re.match(r"h?[a-z](\d{4})", base(p)).group(1)
bad = []
for L, (k, m) in WANT.items():
    e = sec(k)
    if len(e) % m: bad.append((L, "length")); continue
    for j in range(0, len(e), m):
        blk = e[j:j + m]
        if not blk[0].endswith(".cm") or any(not p.endswith(".ca") for p in blk[1:]) or len({num(p) for p in blk}) != 1:
            bad.append((L, j)); break
check("K4 every decoded kind tiles into stride-sized blocks: .cm head, .ca rest, one model number per block (M's list is empty)",
      not bad, str(bad))

b = (PS2 / "add_motion/highmodelreplace.bin").read_bytes()
w = struct.unpack_from("<%dI" % (len(b) // 4), b, 0)
i = 0; recs = []
while w[i] != 0xFFFFFFFF:
    idw = w[i]; i += 3; reps = []
    while w[i] != 0xFFFFFFFF:
        reps.append(w[i]); i += 2
    i += 1; recs.append((idw, reps))
def resolve(mid):
    k, m = WANT[chr(mid >> 16)]
    return sec(k)[m * (mid & 0xFFFF)]
ok = 0
for idw, reps in recs:
    src = resolve(idw); rs = [resolve(r) for r in reps]
    if src.endswith(".cm") and all(p.endswith(".cm") for p in rs) and all(num(p) == num(src) for p in rs): ok += 1
check("K5 the engine's rule resolves all 22 records to .cm files of one model number", len(recs) == 22 and ok == 22,
      "(%d / 22), e.g. %s -> %s" % (ok, base(resolve(recs[0][0])), base(resolve(recs[0][1][0]))))
print("FAILS", fails)
sys.exit(1 if fails else 0)
