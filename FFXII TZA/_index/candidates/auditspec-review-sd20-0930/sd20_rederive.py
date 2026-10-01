"""sd20_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-20 (2026-09-30).
Independent of retool.py's function-list scan: raw E8/E9 sweep of .text for the factory, rawcalls.json cross-check,
DIR64 relocations to the factory (pointer-table uses), every raw rip-relative reference to the interface vtable, and
where each caller's own parent is referenced from (vtable slots?)."""
import sys, json, struct, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"
FACT = 0x007AEA20; VT = 0x01CB5218

def raw_branches(target):
    out = []
    t = tk.d[tk.TRO:tk.TRO + tk.TRS]
    for op in (0xE8, 0xE9):
        i = t.find(bytes([op]))
        while i >= 0:
            if i + 5 <= len(t):
                rel = struct.unpack_from("<i", t, i + 1)[0]
                src = tk.TVA + i
                if src + 5 + rel == target:
                    out.append(("call" if op == 0xE8 else "jmp", src))
            i = t.find(bytes([op]), i + 1)
    # jcc rel32 0F 8x
    i = t.find(b"\x0f")
    while i >= 0:
        if i + 6 <= len(t) and 0x80 <= t[i + 1] <= 0x8F:
            rel = struct.unpack_from("<i", t, i + 2)[0]
            if tk.TVA + i + 6 + rel == target:
                out.append(("jcc", tk.TVA + i))
        i = t.find(b"\x0f", i + 1)
    return out

def ow(a):
    o, k = tk.owner(a)
    return ("%08X" % o + ("" if k == "listed" else "/" + k)) if o else "none"

rc = json.load(open(RAW))
print("factory %08X raw branches:" % FACT)
for k, a in raw_branches(FACT):
    print("  %s %08X owner %s" % (k, a, ow(a)))
print("rawcalls.json callers:", sorted("%08X" % int(x, 16) for x in rc.get("%X" % FACT, [])))
print("relocs -> factory:", ["%08X" % p for p in tk.reloc_ptrs(FACT, FACT + 1)])
refs, rawonly = tk.rip_refs(VT, VT + 8)
print("rip refs to interface vtable %08X: %d verified, %d raw-only" % (VT, len(refs), len(rawonly)))
for x, k, tgt in refs:
    print("  %08X %s %s  owner %s" % (x.address, x.mnemonic, x.op_str, ow(x.address)))
print("relocs -> interface vtable:", ["%08X" % p for p in tk.reloc_ptrs(VT, VT + 8)])
# the 5th-argument store before each call: last write to [rsp + 0x20] in the caller before the call site
for f, site in ((0x007B9050, 0x007B91E7), (0x007DCE20, 0x007DCF92), (0x007EBAD0, 0x007ED332)):
    last = None
    for x in tk.dis(f, site):
        if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rsp + 0x20],"):
            last = x
    print("caller %08X arg5 store before %08X: %s" % (f, site, "%08X %s %s" % (last.address, last.mnemonic, last.op_str) if last else None))
# who references each caller and each caller's parent (vtable slots / calls)
for f in (0x007B9050, 0x007DCE20, 0x007EBAD0, 0x007A4930, 0x007DCD70, 0x007B5D20):
    br = raw_branches(f)
    rl = tk.reloc_ptrs(f, f + 1)
    print("%08X (%s): branches %s relocs %s" % (f, tk.fname(f), ["%s %08X/%s" % (k, a, ow(a)) for k, a in br][:6], ["%08X" % p for p in rl]))
# independent RTTI read (not retool): [vt-8] -> COL; sig 1; COL+0x0C type-descriptor RVA; name at TD+0x10
def rtti(vt):
    col = tk.u64(vt - 8)
    if not col or tk.u32(col) != 1: return None
    td = tk.BASE + tk.u32(col + 0x0C)
    o = tk.off(td + 0x10)
    return tk.d[o:o + 120].split(b"\0")[0].decode("latin1")
for vt in (0x01CB5218, 0x01CB5238, 0x01CB7B20, 0x01CB92A8):
    print("RTTI %08X %s" % (vt, rtti(vt)))
