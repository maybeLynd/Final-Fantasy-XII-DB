"""SWE2-AUDIT-SEM: every rel32 call/jmp to the 02B59D48 pointer-pair setter 003DFE60 and to its reader 003DFD00,
with the constant ecx (index) at each site. Also a whole-.text byte scan for any other instruction that indexes
02B59D48 (already covered by the rip sweep: only 003DFA5F/003DFD03/003DFE63)."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\bucket0930")
import img, reqsites as R, wrappers as W
for tgt in (0x003DFE60, 0x003DFD00):
    sites = R.refs.get(tgt, [])
    print("target %08X: %d rel32 references" % (tgt, len(sites)))
    for c, kind in sites:
        k = W.const_regs(R.decode_back(c, 12))
        tail = list(img.md.disasm(img.rd(c - 12, 17), c - 12))
        print("   %08X %s ecx=%s  | %s" % (c, kind, hex(k["rcx"]) if "rcx" in k else "?", " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in tail[-3:])))
