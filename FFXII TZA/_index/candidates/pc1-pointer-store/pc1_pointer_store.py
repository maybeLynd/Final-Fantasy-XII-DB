"""pc1_pointer_store.py - PC-1's pointer-store clause, static (FABLE, Claude Opus 5.5, 2026-09-27).

Can 01E02804 / 01E02810 (the FF12CONFIG loader's override dwords, -1 in .data) be written through a pointer?
  S1  rip-relative references: every one is a read in the loader 00408C30 (the known 1 + 3)
  S2  image-base-relative forms [reg + (VA - 0x120000)] for any address in [01E02800, 01E02820): none
  S3  stored pointers: no qword VA, dword VA or dword RVA of either address (or of 01E02800) anywhere in the file
  S4  formed pointers near them: every lea / mov that forms an address in [01E02780, 01E02820) - listed; none reaches
      the two dwords by a displacement the same body applies
  C2  control for S2's detector: the image-base-relative form it looks for occurs elsewhere ([rbx + 0x29ca030])
  C3  control for S3's detector: a known stored pointer (the function address in the vtable 01CB2508's slot 0) is found
Reads the capstone listing (Y1P_CACHE) and the shipping image (FFXII_EXE).
"""
import os, re, struct, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
T = (0x01E02804, 0x01E02810)
rip = collections.defaultdict(list); near = []; ibr = []; ctl_ibr = 0
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) < 3: continue
    a, f, s = p
    m = re.search(r"=>([0-9A-F]{8})", s)
    if m:
        t = int(m.group(1), 16)
        if t in T: rip[t].append((a, f, s))
        if 0x01E02780 <= t < 0x01E02820 and (s.startswith("lea ") or s.startswith("mov r") and "ptr" not in s.split(",")[1] if "," in s else False):
            near.append((a, f, s))
        if 0x01E02780 <= t < 0x01E02820 and s.startswith("lea "): near.append((a, f, s))
    for k in re.findall(r"\+ 0x([0-9a-f]+)\]", s):
        v = int(k, 16)
        if 0x01E02800 - 0x120000 <= v < 0x01E02820 - 0x120000: ibr.append((a, f, s))
        if v == 0x29ca030: ctl_ibr += 1
reads = all(("[rip" in s and not s.split(",")[0].strip().startswith(("mov dword ptr", "mov qword ptr", "mov word ptr", "mov byte ptr"))) for t in T for a, f, s in rip[t])
ok("S1", len(rip[T[0]]) == 1 and len(rip[T[1]]) == 3 and reads and all(f == "00408C30" for t in T for a, f, s in rip[t]),
   "rip references: 01E02804 %d, 01E02810 %d, all reads in 00408C30: %s" % (len(rip[T[0]]), len(rip[T[1]]), [a for t in T for a, f, s in rip[t]]))
ok("S2", not ibr, "image-base-relative forms into [01E02800, 01E02820): %d" % len(ibr))
ok("C2", ctl_ibr > 0, "control: the detector finds [reg + 0x29ca030] %d times" % ctl_ibr)
d = open(EXE, "rb").read()
cnt = {hex(v): (d.count(struct.pack("<Q", v)), d.count(struct.pack("<I", v)), d.count(struct.pack("<I", v - 0x120000))) for v in (0x01E02800,) + T}
ok("S3", all(c == (0, 0, 0) for c in cnt.values()), "stored qword VA / dword VA / dword RVA: %s" % cnt)
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
o = pe + 24 + opt; slot0 = None
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); r = 0x01CB2508 - 0x120000
    if va <= r < va + rs: slot0 = struct.unpack_from("<Q", d, ra + r - va)[0]
    o += 40
ctl = d.count(struct.pack("<Q", slot0)) if slot0 else 0
ok("C3", ctl > 0, "control: the vtable 01CB2508's slot 0, the function %s, is found stored as a qword %d time(s)" % (hex(slot0 or 0), ctl))
uniq = sorted(set(near))
ok("S4", all(int(re.search(r"=>([0-9A-F]{8})", s).group(1), 16) not in T for a, f, s in uniq),
   "addresses formed in [01E02780, 01E02820): %s" % [(a, f, s.split(";")[1].strip()) for a, f, s in uniq])
print("FAILS", fails); sys.exit(1 if fails else 0)
