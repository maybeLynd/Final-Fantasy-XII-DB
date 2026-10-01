"""sd20_parents.py - SWE2-AUDIT-SPEC: what `this` each factory caller's parent passes (does a constructor or a
class vtable reach the object in the parent?). Prints the calls in each parent and the instructions before the edge."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
CTORS = {0x007B8E50: "ExternalSourceVoice ctor", 0x007DC730: "HCAMixerVoice ctor", 0x007EA050: "Voice ctor"}
VTS = {0x01CB5238: "ExternalSourceVoice vt", 0x01CB7B20: "HCAMixerVoice vt", 0x01CB92A8: "Voice vt"}
for parent, edge in ((0x007A4930, 0x007A49C1), (0x007DCD70, 0x007DCE07), (0x007B5D20, 0x007B5E20)):
    ins = tk.fdis(parent)
    print("parent %08X size %s, edge %08X" % (parent, tk.fsize(parent), edge))
    for x in ins:
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if t in CTORS: print("  %08X %s -> %s" % (x.address, x.mnemonic, CTORS[t]))
        if "rip" in x.op_str and x.mnemonic == "lea":
            for k, op in enumerate(x.operands):
                if op.type == tk.X86_OP_MEM:
                    t = x.address + x.size + op.mem.disp
                    if t in VTS: print("  %08X lea -> %s" % (x.address, VTS[t]))
    idx = [x.address for x in ins].index(edge)
    for x in ins[max(0, idx - 8):idx + 1]:
        print("    %08X %s %s" % (x.address, x.mnemonic, x.op_str))
# which listed functions call each constructor (raw E8 sweep via rawcalls-like scan)
import struct
t = tk.d[tk.TRO:tk.TRO + tk.TRS]
for c, nm in CTORS.items():
    sites = []
    i = t.find(b"\xe8")
    while i >= 0:
        if i + 5 <= len(t) and tk.TVA + i + 5 + struct.unpack_from("<i", t, i + 1)[0] == c:
            sites.append(tk.TVA + i)
        i = t.find(b"\xe8", i + 1)
    print("%s %08X raw callers: %s" % (nm, c, ["%08X/%08X" % (s, tk.owner(s)[0] or 0) for s in sites]))
