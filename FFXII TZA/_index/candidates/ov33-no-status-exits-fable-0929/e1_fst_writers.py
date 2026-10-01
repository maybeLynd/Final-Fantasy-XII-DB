"""e1_fst_writers.py - who addresses the in-memory FST 02EC3EE0 [0xC8320 bytes], and does anything but the boot fread write it?

Forms swept (tk.py, raw .text byte sweeps, not bounded by the function list):
  rip-relative disp32 into the range; image-base-relative disp32 (VA - 0x120000) into the range;
  absolute imm32/disp32 into the range; DIR64 relocations / raw qwords pointing into it.
For every hit: the owner function and whether the instruction is a store.
Positive controls: 002DF96D (lea in 002DF960, the size reader) and 002DF7B0 (image-base-relative cmp in 002DF780).
Raw-only candidates (a matching dword with no instruction decoding its disp field on the owner boundary) are counted, not listed.
Terminal line: FAILS n / STATUS.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
LO, HI = 0x2EC3EE0, 0x2EC3EE0 + 0xC8320
fails = 0; seen = []
h, raw = tk.rip_refs(LO, HI)
print("# rip-relative: %d verified, %d raw-only" % (len(h), len(raw)))
for x, k, t in h:
    st = tk.is_store(x, k)
    print("  %08X %-6s %-40s -> %08X  %s  %s" % (x.address, x.mnemonic, x.op_str, t, tk.fname(x.address), "STORE" if st else ""))
    seen.append(x.address)
for p, t in raw[:0]: print("  raw-only disp at %08X -> %08X in %s" % (p, t, tk.fname(p)))
h2, raw2 = tk.disp_refs(LO - tk.BASE, HI - tk.BASE)
print("# image-base-relative: %d verified, %d raw-only" % (len(h2), len(raw2)))
for x, k, v in h2:
    print("  %08X %-6s %-40s  %s  %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address), "STORE" if tk.is_store(x, k) else ""))
    seen.append(x.address)
for p, v in raw2[:0]: print("  raw-only %08X value %08X in %s" % (p, v, tk.fname(p)))
h3, raw3 = tk.abs_refs(LO, HI)
print("# absolute imm/disp: %d verified, %d raw-only" % (len(h3), len(raw3)))
from capstone.x86 import X86_OP_MEM
memabs = [(x, v) for x, v in h3 if any(op.type == X86_OP_MEM and (op.mem.disp & 0xFFFFFFFF) == v for op in x.operands)]
immabs = [(x, v) for x, v in h3 if (x, v) not in memabs]
owners = {}
for x, v in immabs: owners.setdefault(tk.fname(x.address), 0); owners[tk.fname(x.address)] += 1
print("  as a MEMORY displacement (absolute address form): %d" % len(memabs))
for x, v in memabs: print("    %08X %s %s  %s  %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address), "STORE" if tk.is_store(x, 0) else ""))
print("  as an arithmetic immediate only (not an address operand): %d, by owner: %s" % (len(immabs), owners))
rel = tk.reloc_ptrs(LO, HI)
print("# DIR64 relocs into range: %d" % len(rel))
for a, q in rel: print("  %08X -> %08X" % (a, q))
# how the lea sites use the pointer: print the lea-owner windows
for c in (0x2DF96D, 0x2DF7B0):
    ok = c in seen; print("control %08X found: %s" % (c, ok)); fails += not ok
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
