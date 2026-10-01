"""SWE2-AUDIT-SPEC independent re-derivation for ASTRA preassignment packet (451897b9d). Read-only on the EXE.
1 getter bodies 006372A0 / 006373D0; 2 registration 005EEB20 arg flow into 00632D80 and its +70/+78/F0/F4 stores;
3 0063E410 recomputation loop; 4 the 0059C700 preclear window and every write to r13 inside 0059C700 (liveness of the
zero from 0059CC38); 5 0060F3D0 / 0060F280 / 0060EFE0 / 005F03A0 bodies; 6 .pdata coverage of the no-pdata spans;
7 raw callers (E8/E9 + jcc) of 0063E410, 006372A0, 005F03A0; 8 the modular identity checked exhaustively on a
32-bit sample grid plus boundary values (a symbolic argument is written in REVIEW.md)."""
import sys, os, struct, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\takebacks"))
import tk
def lin(lo, hi, tag):
    print("== " + tag)
    for x in tk.dis(lo, hi): print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
def rng(e, lo, hi, tag):
    print("== " + tag)
    for x in tk.fdis(e):
        if lo <= x.address <= hi: print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
print("EXE ok:", tk.u32(0x0016D680) is not None)
lin(0x006372A0, 0x006372A8, "006372A0 (8 bytes)")
lin(0x006373D0, 0x00637420, "006373D0 head")
rng(0x005EEB20, 0x005EEB50, 0x005EEBC8, "005EEB20 registration to 00632D80")
lin(0x00632D80, 0x00632E78, "00632D80 constructor (linear, no pdata)")
lin(0x0063E410, 0x0063E48C, "0063E410 recomputation (linear, no pdata)")
for a in (0x00632D80, 0x00632E71, 0x0063E410, 0x0063E487, 0x006372A0):
    print("owner(%08X) =" % a, tk.owner(a))
rng(0x0059C700, 0x0059CC30, 0x0059CCA2, "0059C700 offset window")
# every instruction in 0059C700 that writes r13 / r13d / r13w / r13b
ins = list(tk.fdis(0x0059C700))
print("0059C700 decoded", len(ins), "insns, range %08X..%08X" % (ins[0].address, ins[-1].address))
w13 = [x for x in ins if x.op_str.split(",")[0].strip() in ("r13", "r13d", "r13w", "r13b") and x.mnemonic not in ("cmp", "test", "push")]
for x in w13: print("  writes r13: %08X %s %s" % (x.address, x.mnemonic, x.op_str))
calls = [x for x in ins if x.mnemonic == "call" and 0x0059CC38 <= x.address < 0x0059CD14]
print("calls between 0059CC38 and 0059CD14:", ["%08X %s" % (x.address, x.op_str) for x in calls])
lin(0x0060F3D0, 0x0060F3EA, "0060F3D0")
lin(0x0060F280, 0x0060F290, "0060F280")
lin(0x0060EFE0, 0x0060F048, "0060EFE0 setter")
lin(0x005F03A0, 0x005F03A6, "005F03A0 head"); lin(0x005F0407, 0x005F0408, "005F0407")
RAW = json.load(open(os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json")))
for t in (0x0063E410, 0x006372A0, 0x005F03A0, 0x0060EFE0):
    print("rawcalls %08X:" % t, RAW.get("%X" % t))
TVA, TRS, TRO = tk.TVA, tk.TRS, tk.TRO
text = tk.d[TRO:TRO + TRS]
def rawx(t):
    hits = []
    for i in range(len(text) - 6):
        b = text[i]
        if b in (0xE8, 0xE9):
            if TVA + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t: hits.append("%08X%s" % (TVA + i, "c" if b == 0xE8 else "j"))
        elif b == 0x0F and 0x80 <= text[i + 1] <= 0x8F:
            if TVA + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == t: hits.append("%08Xjcc" % (TVA + i))
    return hits
for t in (0x0063E410, 0x006372A0, 0x005F03A0):
    h = rawx(t); print("raw E8/E9/jcc -> %08X: %d %s" % (t, len(h), " ".join(h[:30])))
# modular identity sext32((8 - F4) mod 2^32) == 8  <=>  F4 == 0
def sext32(v): v &= 0xffffffff; return v - (1 << 32) if v & 0x80000000 else v
bad = [f for f in list(range(-70000, 70000)) + [0x7fffffff, -0x80000000, 0xffffffff, 8, -8, 0x80000008]
       if (sext32(8 - f) == 8) != ((f & 0xffffffff) == 0)]
print("identity counterexamples on grid:", len(bad))
