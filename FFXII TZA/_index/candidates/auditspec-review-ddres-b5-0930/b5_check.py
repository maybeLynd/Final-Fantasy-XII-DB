"""b5_check.py - SWE2-AUDIT-SPEC independent checks on fcb301f83 (chse slot 3, lmap P5). Static, reads only.
K1  raw sweep of .text for E8/E9 rel32 AND 0F 8x rel32 (jcc tail jumps, which chse_slot3.py T10 does not scan) to
    002ED910 / 002ED950, plus DIR64 relocations and unaligned raw qwords holding either VA (T10 scans aligned only).
K2  002ED910's full body (slot-3 read form), and 0037B4D0 from its 002ED910 call to the 0036F0F0 call.
K3  003C1680 around the +0x0C read 003C17A2: the kind test that precedes it (P5's kind-0-only reading).
Control: K1 must re-find 0037B85B (call 002ED910) and 002E6152 (call 002ED950)."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def sweep(targets):
    t = tk.d[tk.TRO:tk.TRO + tk.TRS]; out = []
    for i in range(len(t) - 6):
        b = t[i]
        if b in (0xE8, 0xE9):
            v = tk.TVA + i + 5 + struct.unpack_from("<i", t, i + 1)[0]
            if v in targets: out.append((tk.TVA + i, "call" if b == 0xE8 else "jmp", v))
        elif b == 0x0F and 0x80 <= t[i + 1] <= 0x8F:
            v = tk.TVA + i + 6 + struct.unpack_from("<i", t, i + 2)[0]
            if v in targets: out.append((tk.TVA + i, "jcc", v))
    return out
T = {0x002ED910, 0x002ED950}
s = sweep(T)
print("K1 raw E8/E9/jcc sites=%d" % len(s))
for a, k, v in s:
    print("   %08X %-4s -> %08X owner %08X" % (a, k, v, tk.owner(a)[0] or 0))
print("K1 control 0037B85B and 002E6152 present: %s" % ({0x0037B85B, 0x002E6152} <= {a for a, k, v in s}))
for v in sorted(T):
    print("K1 %08X dir64=%d raw_q=%d" % (v, len(tk.reloc_ptrs(v, v + 1)), len(tk.raw_q(v, v + 1))))
print("K2 002ED910 body:")
for x in tk.fdis(0x002ED910):
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("K2 0037B4D0 0037B850..0037B8A0:")
for x in tk.fdis(0x0037B4D0):
    if 0x0037B850 <= x.address < 0x0037B8A0: print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("K3 003C1680 003C1740..003C17C0:")
for x in tk.fdis(0x003C1680):
    if 0x003C1740 <= x.address < 0x003C17C0: print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
