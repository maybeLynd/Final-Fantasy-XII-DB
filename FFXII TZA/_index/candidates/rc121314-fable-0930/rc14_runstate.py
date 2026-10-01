# rc14_runstate.py - RC-14: does any code move an actor resource entry's +0x11 run state (1 filed -> 2 runnable) besides
# the known writers? Entries are 0x14-byte records at [actor+0xA0] + idx*0x14 (the scheduling page, section 2.5).
# A displacement sweep misses a pointer pre-advanced to +0x11 (the promotion loop does `add rax, 0x11` ... `mov byte
# [rax], 2`), so the census is structural:
#   ENTRY-DERIVING function = loads a qword from [.. + 0xa0] AND walks/indexes with the 0x14 stride
#                             (`add r, 0x14`, or `lea r, [r + r*4]` used as an *4 index);
#   in those functions, list every BYTE store (a) at displacement 0x11, (b) of the constant 2 through any base,
#   (c) through a register that the function advanced by 0x11 (`add r, 0x11` / `lea r, [x + 0x11]`).
# Controls (page section 2.5): the promotion store 003DBB35 (form c), the insert 003DB7A0, UnlinkEntryAndMarkFree's stores
# 003DC1A4 / 003DC1B0 and the start 003DBE68 must all be found.
import os, re, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
BS = re.compile(r"^byte ptr \[(r\w+)(?: \+ (r\w+)\*(\d))?(?: \+ (0x[0-9a-f]+|\d+))?\], (\w+)$")
hits = collections.defaultdict(list)
nderiv = 0
for fn, size in sorted(funcs.items()):
    o = off(fn)
    if o is None or size > 0x10000:
        continue
    ins = list(md.disasm(bytes(d[o:o + size]), fn))
    txt = [(i.mnemonic + " " + i.op_str) for i in ins]
    has_a0 = any(re.search(r"qword ptr \[r\w+ \+ 0xa0\]", t) for t in txt)
    stride = any(re.match(r"add r\w+, 0x14$", t) for t in txt) or any(re.match(r"lea r\w+, \[(r\w+) \+ \1\*4\]$", t) for t in txt)
    if not (has_a0 and stride):
        continue
    nderiv += 1
    adv = set()
    for i in ins:
        t = i.mnemonic + " " + i.op_str
        m = re.match(r"add (r\w+), 0x11$", t) or re.match(r"lea (r\w+), \[r\w+(?: \+ r\w+\*\d)? \+ 0x11\]$", t)
        if m:
            adv.add(m.group(1))
        if i.mnemonic != "mov":
            continue
        m = BS.match(i.op_str)
        if not m or m.group(1) in ("rsp", "rbp"):
            continue
        disp = int(m.group(4), 0) if m.group(4) else 0
        val = m.group(5)
        why = []
        if disp == 0x11:
            why.append("disp 0x11")
        if val in ("2", "0x2"):
            why.append("stores 2")
        if disp == 0 and m.group(1) in adv:
            why.append("base advanced by 0x11")
        if why:
            hits[fn].append("%08X %s %s [%s]" % (i.address, i.mnemonic, i.op_str, ", ".join(why)))
print("entry-deriving functions: %d; with a candidate store: %d" % (nderiv, len(hits)))
allsites = " ".join(" ".join(v) for v in hits.values())
print("CONTROLS:", {c: (c in allsites) for c in ("003DBB35", "003DC1A4", "003DC1B0", "003DBE68")},
      "| insert 003DB7A0 listed:", 0x003DB7A0 in hits)
for fn in sorted(hits):
    for h in hits[fn]:
        print("%08X  %s" % (fn, h))
