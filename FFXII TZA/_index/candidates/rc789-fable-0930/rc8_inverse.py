# rc8_inverse.py - RC-8: can anything but the constructor store the shadow singleton's cascade count (+0x13C)?
# The object is a singleton: 001F0810 / 001F0850 allocate 0xB08 bytes (00210EC0), construct it with 001EF2D0 and store
# the pointer in the global 01F82EA8; 001F0850 is also the get-or-create. There is no vtable, so a writer must hold a
# pointer that came from 01F82EA8 (a load of the cell, or the getter's return), possibly passed as an argument.
# Census:
#   H  = functions that load qword [01F82EA8] (rip-relative) or call 001F0850 / 001F0810 (raw E8/E9 index);
#   H1 = H plus every direct callee of an H function (one hop: covers the object passed as an argument once);
#   W  = functions with a non-stack store covering dword +0x13C (rc8_writes.py's rule, rsp/rbp-frame stores removed);
# Report W & H1, then each such store with the function's pointer sources, for reading.
# Controls: the constructor 001EF2D0 must be in H1 (callee of 001F0850) and its store 001EF389 must be in W & H1.
import os, re, json, bisect, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
CELL = 0x01F82EA8
GETTERS = {0x001F0850, 0x001F0810}
fl = sorted(funcs)
def owner(a):
    k = bisect.bisect_right(fl, a) - 1
    return fl[k] if k >= 0 and a < fl[k] + funcs[fl[k]] else None
raw = json.load(open("tools/rawcalls.json"))
callees = collections.defaultdict(set)
getter_callers = set()
for tgt, sites in raw.items():
    t = int(tgt, 16)
    for s in sites:
        ow = owner(int(s, 16))
        if ow is None:
            continue
        callees[ow].add(t)
        if t in GETTERS:
            getter_callers.add(ow)
W = {}
cell_loaders = set()
ST = re.compile(r"^(dword|qword|xmmword) ptr \[(r\w+) \+ 0x(1[23][0-9a-f])\],")
for fn, size in sorted(funcs.items()):
    o = off(fn)
    if o is None or size > 0x10000:
        continue
    for i in md.disasm(bytes(d[o:o + size]), fn):
        m = re.search(r"qword ptr \[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
        if m and i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) == CELL:
            cell_loaders.add(fn)
        if i.mnemonic.startswith("mov") or i.mnemonic in ("add", "sub", "inc", "dec", "or", "and", "xor"):
            m2 = ST.match(i.op_str)
            if m2 and m2.group(2) not in ("rsp", "rbp"):
                w = {"dword": 4, "qword": 8, "xmmword": 16}[m2.group(1)]
                o2 = int(m2.group(3), 16)
                if o2 <= 0x13C < o2 + w:
                    W.setdefault(fn, []).append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
H = cell_loaders | getter_callers
import sys
HOPS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
H1 = set(H)
frontier = set(H)
for _ in range(HOPS):
    nxt = set()
    for f in frontier:
        nxt |= callees[f]
    nxt -= H1
    H1 |= nxt
    frontier = nxt
print("H: cell loaders %d, getter callers %d; H1 (with callees to %d hops) %d functions" % (len(cell_loaders), len(getter_callers), HOPS, len(H1)))
print("W: non-stack +0x13C store functions %d (stores %d)" % (len(W), sum(len(v) for v in W.values())))
print("CONTROL ctor 001EF2D0 in H1:", 0x001EF2D0 in H1, "| its store in W:", any("001EF389" in s for s in W.get(0x001EF2D0, [])))
both = sorted(set(W) & H1)
print("W & H1: %d functions" % len(both))
for f in both:
    why = ("loads cell" if f in cell_loaders else "") + (" calls getter" if f in getter_callers else "") + (" callee of H" if f not in H else "")
    print("  %08X [%s]: %s" % (f, why.strip(), "; ".join(W[f])))
