"""refsweep.py LO [HI] [--control SITE ...] - raw, function-list-independent reference sweep to [LO, HI).

(a) rip-relative: every byte offset i in .text is read as a rel32; for trailing-immediate sizes k in
    {0,1,2,4} the target va(i)+4+k+rel is tested; each candidate is confirmed by decoding an instruction
    that starts at i-1..i-12, ends at i+4+k, and has a rip memory operand resolving into the range.
(b) RVA / image-base-relative disp32 (target-0x120000) and absolute VA dword anywhere in the image.
(c) 64-bit absolute VA qword in .rdata/.data (pointer tables).
--control SITE: an instruction address that MUST appear in (a); the script counts a FAIL if missing.
Prints each hit with its owning listed function (or 'unlisted') and a FAILS count.
"""
import sys, struct, bisect, argparse
from array import array
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
ap = argparse.ArgumentParser()
ap.add_argument("lo"); ap.add_argument("hi", nargs="?")
ap.add_argument("--control", nargs="*", default=[])
ap.add_argument("--quiet-abs", action="store_true")
a = ap.parse_args()
lo = int(a.lo, 16); hi = int(a.hi, 16) if a.hi else lo + 1
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((nm, BASE + va, vs, ro, rs))
funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError): pass
funcs.sort(); fstarts = [f[0] for f in funcs]
def owner(va):
    k = bisect.bisect_right(fstarts, va) - 1
    if k >= 0 and funcs[k][0] <= va < funcs[k][0] + funcs[k][2]: return f"{funcs[k][0]:08X} {funcs[k][1]}"
    return "unlisted"
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0
text = [s for s in secs if s[0] == ".text"][0]
_, tva, tvs, tro, trs = text
tb = d[tro:tro + min(tvs, trs)]
cands = set()
L, H = lo - tva - 8, hi - tva - 4          # rel + i + 4 + k in [lo-tva, hi-tva), k in 0..4
for al in range(4):
    seg = tb[al:]; seg = seg[:len(seg) // 4 * 4]
    arr = array("i", seg)
    for j, r in enumerate(arr):
        v = r + 4 * j + al
        if L <= v < H:
            i = al + 4 * j
            for k in (0, 1, 2, 4):
                if lo <= tva + i + 4 + k + r < hi: cands.add((i, k))
byend = {}
for (i, k) in sorted(cands):
    if True:
        for st in range(i - 1, max(i - 13, -1), -1):
            ins = next(md.disasm(d[tro + st:tro + st + 16], tva + st, 1), None)
            if ins is None or ins.address + ins.size != tva + i + 4 + k: continue
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base and ins.reg_name(op.mem.base) == "rip":
                    t = ins.address + ins.size + op.mem.disp
                    if lo <= t < hi: byend[ins.address + ins.size] = (ins.address, t, ins.mnemonic, ins.op_str)  # earliest start wins (REX kept)
rip_hits = set(byend.values())
print(f"== refsweep [{lo:08X},{hi:08X})")
print(f"(a) rip-relative confirmed: {len(rip_hits)}")
for s, t, m, o in sorted(rip_hits):
    print(f"  {s:08X}  -> {t:08X}  {m} {o}   [{owner(s)}]")
sites = {h[0] for h in rip_hits}
for c in a.control:
    ok = int(c, 16) in sites
    print(f"  CONTROL {c}: {'PASS' if ok else 'FAIL'}")
    fails += 0 if ok else 1
# (b) dword RVA and absolute VA anywhere in the file image
nb = 0
for (nm, sva, svs, sro, srs) in secs:
    raw = d[sro:sro + min(svs, srs)]
    for val, label in ((lo - BASE, "rva/disp32"), (lo, "abs32")):
        for vv in range(val, val + (hi - lo)):
            pat = struct.pack("<I", vv & 0xFFFFFFFF)
            p = raw.find(pat)
            while p >= 0:
                nb += 1
                if not a.quiet_abs or nm == ".text":
                    ctx = ""
                    if nm == ".text":
                        for st in range(p - 1, max(p - 12, -1), -1):
                            ins = next(md.disasm(raw[st:st + 16], sva + st, 1), None)
                            if ins and ins.address < sva + p < ins.address + ins.size and ins.address + ins.size >= sva + p + 4:
                                ctx = f"{ins.address:08X} {ins.mnemonic} {ins.op_str} [{owner(ins.address)}]"; break
                    print(f"  (b) {label} {vv:08X} in {nm} at {sva + p:08X} {ctx}")
                p = raw.find(pat, p + 1)
print(f"(b) dword hits: {nb}")
nc = 0
for (nm, sva, svs, sro, srs) in secs:
    if nm not in (".rdata", ".data", "_RDATA"): continue
    raw = d[sro:sro + min(svs, srs)]
    for vv in range(lo, hi):
        pat = struct.pack("<Q", vv); p = raw.find(pat)
        while p >= 0:
            nc += 1; print(f"  (c) qword {vv:08X} in {nm} at {sva + p:08X}"); p = raw.find(pat, p + 1)
print(f"(c) qword pointer hits: {nc}")
print(f"FAILS {fails}")
