"""SWE2-AUDIT-SPEC independent checks for RC-4 (rc4b-capture-residue-0930), 2026-09-30. Image only.
D1  every verified [reg(+index)+0xDAC] access image-wide (disp32; 0xDAC cannot be a disp8), stores classified by source.
    Control: the record's five writers 00185020 (0), 00187891/001878B3/001878D5/001878E5 (3,4,0,7) must appear.
D2  every verified access with displacement 0xCB8 (the vector index): stores and their source.
D3  assumption 1: vtables 00D49930 / 00D498F0 / 00D49910 - slot 2 (vt+0x10) and the RTTI class name via the COL.
"""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
def classify(x, k):
    op = x.operands[k]
    wr = tk.is_store(x, k)
    src = None
    if wr:
        others = [o for i, o in enumerate(x.operands) if i != k]
        if x.mnemonic.startswith("mov") and others:
            o = others[0]
            src = ("imm %d" % o.imm) if o.type == X86_OP_IMM else ("reg " + x.reg_name(o.reg) if o.type == X86_OP_REG else "mem")
        else:
            src = x.mnemonic
    return wr, op.size, src
for tag, disp in (("D1", 0xDAC), ("D2", 0xCB8)):
    hits, raw = tk.disp_refs(disp, disp + 1)
    st = []; rd = 0
    for x, k, v in hits:
        wr, sz, src = classify(x, k)
        if wr: st.append((x.address, sz, src, x.mnemonic + " " + x.op_str, tk.owner(x.address)[0]))
        else: rd += 1
    print("%s disp 0x%X: verified accesses %d (stores %d, other %d), raw-only candidates %d" % (tag, disp, len(hits), len(st), rd, len(raw)))
    for a, sz, src, t, o in st:
        print("  store %08X in %08X size %d src %-10s | %s" % (a, o or 0, sz, src, t))
    if tag == "D1":
        want = {0x185020, 0x187891, 0x1878B3, 0x1878D5, 0x1878E5}
        print("  CONTROL five known writers present:", want <= {a for a, *_ in st})
def cls_name(vt):
    col = tk.u64(vt - 8)
    if col is None: return None
    sig, off_, cd, td_rva = struct.unpack_from("<IIII", tk.d, tk.off(col))
    td = td_rva + tk.BASE
    o = tk.off(td + 16); s = tk.d[o:o + 80].split(b"\0")[0]
    return s.decode(errors="replace")
for vt in (0xD49930, 0xD498F0, 0xD49910):
    print("D3 vtable %08X slot2 %08X slot0 %08X class %s" % (vt, tk.u64(vt + 0x10), tk.u64(vt), cls_name(vt)))
