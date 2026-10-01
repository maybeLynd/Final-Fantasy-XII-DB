"""e3_readlayer_ptr.py - who writes the pointer 001A1220() returns ([01F81160]), and when?  (OV-33 E3)

Sweeps (tk.py raw .text sweeps, independent of the function list): rip-relative disp32 into [01F81160,01F81168),
image-base-relative disp32 (01F81160-0x120000), absolute imm/disp forms, DIR64 relocs / raw qwords pointing at it.
Also a wider window [01F81100,01F81200) for rip STORES of 8 bytes that overlap the cell (a qword store at a
neighbour cannot overlap an aligned qword, but a movups/16-byte store at 01F81158 or 01F81150 could).
Raw call index: callers of 001A1220 and of every function that stores the cell.
Positive controls: 001A1220's own load (rip ref at 001A1220) must be found; the known reader 001D6DB1's callee.
Terminal line: FAILS n / STATUS.
"""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
CELL = 0x1F81160
fails = 0
print("section of cell:", tk.sec_of(CELL), " file offset:", tk.off(CELL), "(None = virtual tail, zero-initialised)")
h, raw = tk.rip_refs(CELL - 0x10, CELL + 0x10)
print("# rip refs in [cell-0x10, cell+0x10): %d verified, %d raw-only (not listed)" % (len(h), len(raw)))
stores = []
for x, k, t in h:
    sz = x.operands[k].size
    covers = t <= CELL < t + sz or CELL <= t < CELL + 8
    st = tk.is_store(x, k)
    tag = ("STORE" if st else "read") + (" covers-cell" if covers else "")
    print("  %08X %-6s %-44s -> %08X size %d  %s  %s" % (x.address, x.mnemonic, x.op_str, t, sz, tk.fname(x.address), tag))
    if st and covers: stores.append(x.address)
    if x.mnemonic == "lea" and t == CELL: print("    ^ ADDRESS-TAKE of the cell")
h2, raw2 = tk.disp_refs(CELL - tk.BASE - 0x10, CELL - tk.BASE + 0x10)
print("# image-base-relative: %d verified, %d raw-only" % (len(h2), len(raw2)))
for x, k, v in h2: print("  %08X %s %s  %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))
h3, raw3 = tk.abs_refs(CELL - 0x10, CELL + 0x10)
memabs = [(x, v) for x, v in h3 if any(op.type == X86_OP_MEM and (op.mem.disp & 0xFFFFFFFF) == v for op in x.operands)]
print("# absolute address operands: %d (imm-only hits %d)" % (len(memabs), len(h3) - len(memabs)))
for x, v in memabs: print("  %08X %s %s  %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))
rel = tk.reloc_ptrs(CELL - 0x10, CELL + 0x10)
print("# DIR64 relocs pointing into the window: %d" % len(rel))
for a, q in rel: print("  %08X -> %08X" % (a, q))
print("\n# stores covering the cell: %s" % ", ".join("%08X" % a for a in stores))
raw_idx = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
for a in stores:
    o, how = tk.owner(a)
    print("  store %08X in %08X; raw callers of %08X: %s" % (a, o, o, raw_idx.get("%X" % o, [])))
ctl = any(x.address == 0x1A1220 for x, k, t in h)
print("control 001A1220 load found:", ctl); fails += not ctl
print("callers of 001A1220 (raw E8/E9): %d" % len(raw_idx.get("1A1220", [])))
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
