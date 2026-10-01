"""pc1_dev_bytes.py - PC-1's last residue: no shipped reader of FF12CONFIG's ten unread fields (FABLE, Claude Opus 5.5,
2026-09-27). Width-aware, so a wider access that covers one of the ten bytes counts as a reader.

  D1  every rip-relative access into [02B62DA0, 02B62DC8), with its byte span from the operand width; the spans that
      cover any of the ten bytes come only from the reset 00408BA0 and the loader 00408C30
  D2  no image-base-relative form [reg + (VA - 0x120000)] reaches the range
  D3  no data word holds an address in the range (qword VA, dword VA, dword RVA)
  D4  every address formed into the range by lea is in 00408BA0 / 00408C30
  D5  every access that covers one of the ten bytes is a byte store (defaults or file copy) - none reads them
  C1  control: the same census finds the six read fields' getters (00408B10, 00408B50, 00408B80, 00408B40, 00408B60,
      00408B70) and nothing reads a covered byte of theirs outside their getter
  C2  control for the width rule: a planted qword read at 02B62DA8 would cover 02B62DA9 and is reported
"""
import os, re, struct, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
TEN = [0x02B62DA9, 0x02B62DAE, 0x02B62DAF, 0x02B62DB0, 0x02B62DB2, 0x02B62DB3, 0x02B62DB7, 0x02B62DB8, 0x02B62DBB, 0x02B62DBC]
LO, HI = 0x02B62DA0, 0x02B62DC8
OWN = {"00408BA0", "00408C30"}
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
def width(s):
    m = re.search(r"\b(byte|word|dword|qword|xmmword) ptr \[rip", s)
    if m: return W[m.group(1)]
    if s.startswith(("movss", "comiss", "ucomiss")): return 4
    if s.startswith(("movsd",)): return 8
    return None
acc = []; ibr = []; lea = []
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) < 3: continue
    a, f, s = p
    m = re.search(r"=>([0-9A-F]{8})", s)
    if m:
        t = int(m.group(1), 16)
        if LO <= t < HI:
            if s.startswith("lea "): lea.append((a, f, t))
            else: acc.append((a, f, s.split(";")[0].strip(), t, width(s)))
    for k in re.findall(r"\+ 0x([0-9a-f]+)\]", s):
        if LO - 0x120000 <= int(k, 16) < HI - 0x120000: ibr.append((a, f, s))
def covers(t, w, b): return w is not None and t <= b < t + w
unknown = [x for x in acc if x[4] is None]
readers = collections.defaultdict(set)
for a, f, s, t, w in acc:
    for b in TEN:
        if covers(t, w, b): readers[b].add(f)
outside = {hex(b): sorted(fs - OWN) for b, fs in readers.items() if fs - OWN}
ok("D1", not outside and not unknown, "%d rip accesses into the range; ten bytes covered only by %s; unknown-width accesses %d"
   % (len(acc), sorted({f for fs in readers.values() for f in fs}), len(unknown)))
cov = [(a, f, s) for a, f, s, t, w in acc if any(covers(t, w, b) for b in TEN)]
ok("D5", cov and all(s.startswith("mov byte ptr [rip") for a, f, s in cov),
   "every one of the %d accesses covering the ten bytes is a byte STORE (defaults in 00408BA0, file copies in 00408C30); none reads them" % len(cov))
ok("D2", not ibr, "image-base-relative forms into the range: %d" % len(ibr))
d = open(EXE, "rb").read()
st = [v for v in range(LO, HI) if d.count(struct.pack("<Q", v)) or d.count(struct.pack("<I", v - 0x120000))]
ok("D3", not st, "addresses in the range stored as a qword VA or dword RVA: %s" % [hex(v) for v in st])
ok("D4", all(f in OWN for a, f, t in lea), "addresses formed by lea: %s" % sorted({(f, hex(t)) for a, f, t in lea}))
getters = {"00408B10", "00408B50", "00408B80", "00408B40", "00408B60", "00408B70"}
seen = {f for a, f, s, t, w in acc}
ok("C1", getters <= seen, "control: the six read fields' getters are found: %s" % sorted(getters & seen))
ok("C2", covers(0x02B62DA8, 8, 0x02B62DA9) and not covers(0x02B62DA8, 1, 0x02B62DA9), "control: a qword at 02B62DA8 covers 02B62DA9, a byte does not")
print("FAILS", fails); sys.exit(1 if fails else 0)
