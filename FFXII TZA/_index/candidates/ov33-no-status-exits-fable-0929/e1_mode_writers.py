"""e1_mode_writers.py - writers of the arena-11 mode bytes 02ADD930..02ADD933 that gate 0024AC30's kind-35 request
(0037B330 returns [02ADD930], or 4 when [02ADD931] != 0).  (OV-33 E1 route condition)
Sweeps rip / image-base-relative / absolute forms; lists every store and the raw callers of each storing function.
Positive control: 0037B458 (the store in 0037B450) must be listed.
Terminal line: FAILS n / STATUS.
"""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
LO, HI = 0x2ADD930, 0x2ADD934
raw_idx = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
fails = 0; stores = []
h, raw = tk.rip_refs(LO, HI)
print("# rip refs: %d verified, %d raw-only" % (len(h), len(raw)))
for x, k, t in h:
    st = tk.is_store(x, k)
    print("  %08X %-6s %-40s -> %08X  %s  %s" % (x.address, x.mnemonic, x.op_str, t, tk.fname(x.address), "STORE" if st else ""))
    if st: stores.append(x.address)
h2, raw2 = tk.disp_refs(LO - tk.BASE, HI - tk.BASE)
print("# image-base-relative: %d verified" % len(h2))
for x, k, v in h2: print("  %08X %s %s %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))
h3, raw3 = tk.abs_refs(LO, HI)
m3 = [(x, v) for x, v in h3 if any(op.type == X86_OP_MEM and (op.mem.disp & 0xFFFFFFFF) == v for op in x.operands)]
print("# absolute address operands: %d" % len(m3))
print("\n# storing functions and their raw callers:")
for o in sorted(set(tk.owner(a)[0] for a in stores)):
    print("  %08X %s  callers: %s" % (o, tk.names.get(o, "?"), raw_idx.get("%X" % o, [])))
ok = 0x37B458 in stores; print("control 0037B458 listed:", ok); fails += not ok
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
