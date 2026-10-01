"""SWE2-AUDIT-SPEC independent check for SD-41 (2026-09-30).
R1  near-value immediates: every dword in .text whose value lies within +-0x10000 of either stamp and that decodes as an
    instruction immediate/displacement (a range/order compare such as `cmp eax, stamp-1` would show here; the author's
    F1 searches only the exact bytes).
R2  the jcc that consumes the one compare at 00233C4D (equality vs order).
R3  the getters' raw callers and the first instructions after each call (does a caller order-compare the returned value).
Control: R1 must find the four known exact sites (sensitive: a sweep that decoded nothing would print 0).
"""
import sys, json, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_IMM, X86_OP_MEM
STAMPS = [0x20050223, 0x05071901]
t0, tsz = tk.TVA, tk.TRS
data = tk.d[tk.TRO:tk.TRO + tsz]
hits = []
for pos in range(0, len(data) - 4):
    v = struct.unpack_from("<I", data, pos)[0]
    for s in STAMPS:
        if abs(v - s) <= 0x10000:
            a = t0 + pos
            for back in range(1, 11):
                try:
                    ins = list(tk.md.disasm(tk.d[tk.TRO + pos - back:tk.TRO + pos - back + 15], a - back, 1))
                except Exception:
                    ins = []
                if not ins or ins[0].size < back + 4:
                    continue
                x = ins[0]
                vals = [op.imm & 0xFFFFFFFF for op in x.operands if op.type == X86_OP_IMM] + \
                       [op.mem.disp & 0xFFFFFFFF for op in x.operands if op.type == X86_OP_MEM]
                if v in vals:
                    hits.append((x.address, "%s %s" % (x.mnemonic, x.op_str), hex(v), tk.fname(x.address)))
                    break
hits = sorted(set(hits))
print("R1 near-value decoded uses: %d" % len(hits))
for h in hits:
    print("   %08X  %-40s value %s  in %s" % h)
print("R2 after 00233C4D:")
for x in tk.dis(0x00233C4D, 0x00233C4D + 16):
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
rc = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
for g in (0x002EF2A0, 0x00235E90):
    sites = rc.get("%X" % g, [])
    print("R3 getter %08X raw call sites: %d" % (g, len(sites)))
    for s in sites:
        s = int(s, 16)
        seq = list(tk.dis(s, s + 24))
        print("   %08X in %s: %s" % (s, tk.fname(s), " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in seq[:4])))
