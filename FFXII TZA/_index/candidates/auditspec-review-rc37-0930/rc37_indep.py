"""rc37_indep.py - SWE2-AUDIT-SPEC independent checks for rc37-refused-read-0930 (and SWE2-DATA rc28-callback-0930).
Static, read-only. Uses tk.py (raw .text sweeps, not the function list) and the raw call index.
  R1  who issues reads: raw callers of 0046E030 / 002DF780 / 002DF6C0 (is the pump the only issuer?)
  R2  every access to the status slot 0215EFF4 and the pointer global 01F82CC0: rip-relative AND image-base-relative
      (disp32 = VA-0x120000 with a non-rip base), with access width and read/write; plus stored pointers (relocs).
  R3  is 0215EFF4 inside file data or the zero-initialised virtual tail?
  R4  00364380 whole body; any read of r8/r8d.
  R5  0032E370 body (the error helper): the -1 test and the call.
  R6  the sheet allocation route 00365810 -> 002497E0 / 00249810: first-level callees (which allocator is reached).
"""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_IMM
rc = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def callers(a):
    return rc.get("%X" % a, [])
for t in (0x0046E030, 0x002DF780, 0x002DF6C0, 0x00364380, 0x0032E370, 0x0032E330):
    cs = callers(t)
    print("R1 raw callers of %08X: %d %s" % (t, len(cs), sorted(set(tk.fname(int(c, 16)) for c in cs))))
for lo in (0x0215EFF4, 0x01F82CC0):
    hi = lo + 4 if lo == 0x0215EFF4 else lo + 8
    refs, raw = tk.rip_refs(lo, hi)
    print("R2 rip refs to %08X: %d (raw-only %d)" % (lo, len(refs), len(raw)))
    for x, k, tgt in refs:
        a = x.address
        print("   %08X %-6s %-40s w=%d store=%s  %s" % (a, x.mnemonic, x.op_str[:40], tk.memsize(x, k), tk.is_store(x, k), tk.fname(a)))
    dr = tk.disp_refs(lo - tk.BASE, hi - tk.BASE)
    print("R2 image-base-relative refs to %08X: %d verified %s, raw-only %d" % (lo, len(dr[0]), ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x, k, v in dr[0]], len(dr[1])))
    rp = tk.reloc_ptrs(lo, hi)
    print("R2 stored absolute pointers (relocs) to %08X: %d" % (lo, len(rp)))
va, vs, rs, ro = tk.secs[tk.sec_of(0x0215EFF4)]
print("R3 0215EFF4 section %s va %08X rawsize %#x virtsize %#x -> %s" % (tk.sec_of(0x0215EFF4), va, rs, vs,
      "virtual tail (zero-init)" if 0x0215EFF4 - va >= rs else "file-backed, initial dword %#x" % tk.u32(0x0215EFF4)))
body = tk.dis(0x00364380, 0x0036439A)
print("R4 00364380: " + "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in body))
print("R4 reads r8: %s" % any("r8" in i.op_str for i in body))
for i in tk.dis(0x0032E370, 0x0032E3A0):
    print("R5 %08X %s %s" % (i.address, i.mnemonic, i.op_str))
for f in (0x00365810, 0x002497E0, 0x00249810):
    sz = tk.fsize(f) or 0x80
    cl = [(i.address, i.op_str) for i in tk.dis(f, f + sz) if i.mnemonic in ("call", "jmp") and i.operands[0].type == X86_OP_IMM]
    print("R6 %08X (size %s) direct calls/jumps: %s" % (f, tk.fsize(f), ["%08X->%s" % (a, o) for a, o in cl][:14]))
