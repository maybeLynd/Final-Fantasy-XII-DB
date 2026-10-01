"""The shared 0x60 bank descriptor has one description (OPUS, 2026-09-27).

RenderResourceEntryBank is the descriptor 0051F9F0 builds; its route EMBEDs it at +0x00 of RenderStrideC0Bank and
RenderModelInstanceContainer. Those two also carried 20 rows each over the same bytes, and the copies had drifted: the
shared code's reading (liveHead, liveCount, the relocatable handles, ...) lived only on RenderModelInstanceContainer's
copy, while the child said 'DISCOVERED, split INHERITED'. check_embed_overlap reported both as NAMED duplications.
  B1 the descriptor is one constructor's: 0051F9F0 is called from exactly three sites with rowStride 0x50 / 0xC0 /
     0x260 and bankShift 5 (00409F38, 0046E285, 00477F0A), and it writes the fields the rows cite (0051FA2C qword -1
     at +0x40, 0051FA3F +0x08, 0051FA43 +0x10, 0051FA47 word +0x24, 0051FA84 +0x48, 0051FA8E +0x4C, 0051FB03 +0x28)
  B2 the shared readers are generic: 0051F6B0 / 0051F7A0 read +0x20 / +0x22 / +0x24 of whatever descriptor they get
  S  REGRESSION: RenderResourceEntryBank carries 20 rows over +0x00..+0x5F, liveHead SEMANTICALLY IDENTIFIED and
     elementBlock a generic void*; each owner has ONE row below +0x60, at +0x00, 0x60 bytes, ctype RenderResourceEntryBank
     (FAILS before the merge)
  E  check_embed_overlap lists neither owner (only BattleStatsRecord <- GambitConfig remains)
Not claimed: anything about the owners' tails (+0x60 on).
"""
import os, re, struct, subprocess, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.dirname(os.path.dirname(DB))
d = open(os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return {x.address: x for x in cs.disasm(d[off(a):off(a) + size], a)}
args = sys.argv[1:]
FIELDS = args[args.index("--fields") + 1] if "--fields" in args else os.path.join(DB, "_types", "fields.tsv")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
ctor = dis(0x51F9F0, 0x200)
want = {0x51FA2C: "qword ptr [rcx + 0x40], 0xffffffffffffffff", 0x51FA3F: "qword ptr [rcx + 8], rdi",
        0x51FA43: "qword ptr [rcx + 0x10], rax", 0x51FA47: "word ptr [rcx + 0x24], r14w", 0x51FA84: "dword ptr [rbx + 0x48], edx",
        0x51FA8E: "dword ptr [rbx + 0x4c], r8d", 0x51FB03: "qword ptr [rbx + 0x28], rax"}
sites = {0x409F38: (0x409F10, "edx, 0x50"), 0x46E285: (0x46E250, "edx, 0xc0"), 0x477F0A: (0x477EE0, "edx, 0x260")}
ok_sites = True
for s, (f, stride) in sites.items():
    xs = dis(f, s - f + 5)
    pre = [x.op_str for a, x in sorted(xs.items()) if a < s][-8:]
    ok_sites &= xs.get(s) is not None and xs[s].op_str == "0x51f9f0" and stride in pre and any(p.startswith("r8d, ") for p in pre)
check("B1 one constructor, three call sites (strides 0x50 / 0xC0 / 0x260), and the cited stores",
      ok_sites and all(ctor.get(a) is not None and ctor[a].op_str == o for a, o in want.items()))
r6 = [x.op_str for x in dis(0x51F6B0, 0x60).values()]; r7 = [x.op_str for x in dis(0x51F7A0, 0x40).values()]
check("B2 the shared readers take any descriptor (+0x20 / +0x22 / +0x24 through rcx / rbx)",
      "eax, word ptr [rcx + 0x24]" in r6 and "word ptr [rcx + 0x22], ax" in r6 and "word ptr [rcx + 0x22], 0" in r7)
rows = {}
for l in open(FIELDS, encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    try: rows.setdefault(c[0], {})[int(c[1], 16)] = c
    except (ValueError, IndexError): pass
ch = {o: c for o, c in rows.get("RenderResourceEntryBank", {}).items() if o < 0x60}
own_ok = all(sorted(o for o in rows.get(t, {}) if o < 0x60) == [0] and rows[t][0][2] == "96" and rows[t][0][4] == "RenderResourceEntryBank"
             for t in ("RenderStrideC0Bank", "RenderModelInstanceContainer"))
check("S one description: the child's 20 rows carry the shared reading; each owner has one 0x60 row",
      len(ch) == 20 and ch.get(0x40, [""] * 7)[6] == "SEMANTICALLY IDENTIFIED" and ch.get(0x28, [""] * 5)[4] == "void*" and own_ok)
out = subprocess.run([sys.executable, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts", "check_embed_overlap.py")],
                     capture_output=True, text=True, cwd=ROOT).stdout
m = re.search(r"PARENTS DESCRIBING BYTES A DECLARED CHILD ALREADY CLAIMS: (\d+)", out)
check("E check_embed_overlap no longer lists either owner", m is not None and "RenderStrideC0Bank" not in out.split("CLEAN")[0]
      and "RenderModelInstanceContainer" not in out.split("CLEAN")[0], "(%s reported)" % (m.group(1) if m else "?"))
print("FAILS", fails)
sys.exit(1 if fails else 0)
