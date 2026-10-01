"""SWE2-AUDIT-SPEC independent re-derivation for ASTRA special-action-override-domain (2026-09-30).
Uses tk.py (section-aware, raw sweeps) - not the packet's capture driver or prover.
 D1 constructor store width at 001CCC06 and the object register
 D2 the control arm 001D2DD3..001D2DFA executed by a small interpreter over its own decoded instructions, states -1..9
 D3 setter 002F7A00 / initializer 002F79E0 identity, the 16 constant bytes at 00D0F9E0, the .data value at 01EEBAF0
 D4 callers of the setter/initializer: raw E8/E9/jcc/jmp-rel, rawcalls.json, rip address-taken, DIR64 relocations
 D5 every rip/image-base reference to the index cell 01EEBAF0 and the word array 022BE930 (writes vs reads)
 D6 image-wide [reg+disp32] stores overlapping +0xAE0..+0xAE3 (any base register: a candidate superset of writers)
"""
import sys, struct, json, pathlib
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))

def show(x): return "%08X %s %s" % (x.address, x.mnemonic, x.op_str)

print("D1 constructor")
ins = [x for x in tk.dis(0x001CCB20, 0x001CCFDA)]
for x in ins:
    if x.address in (0x001CCB42, 0x001CCC06): print("  ", show(x), "size", x.size)
st = next(x for x in ins if x.address == 0x001CCC06)
m = st.operands[0]
print("   store width", m.size, "disp", hex(m.mem.disp), "base", st.reg_name(m.mem.base), "imm", hex(st.operands[1].imm))
print("   bytes covered +0x%X..+0x%X; imm high dword = %d" % (m.mem.disp, m.mem.disp + m.size - 1, (st.operands[1].imm >> 32) & 0xFFFFFFFF))
# does rdi change between 1CCB42 and 1CCC06, and any later access to +0xADC..+0xAE3 in the fragment
redef = [show(x) for x in ins if 0x001CCB42 < x.address < 0x001CCC06 and x.op_str.startswith(("rdi,", "edi,")) and x.mnemonic not in ("cmp", "test")]
later = [show(x) for x in ins if x.address > 0x001CCC06 and any(o.type == 3 and 0xAD5 <= o.mem.disp <= 0xAE3 for o in x.operands)]
print("   rdi redefinitions between:", redef or "none")
print("   later +0xAD5..+0xAE3 accesses in 001CCB20..001CCFDA:", later or "none")

print("D2 control arm interpreter (bl!=0 = decrement branch)")
arm = {x.address: x for x in tk.dis(0x001D2DD3, 0x001D2DFF)}
for a in sorted(arm): print("  ", show(arm[a]))
def run(state, bl):
    mem = state; eax = None; ecx = None; pc = 0x001D2DD3; flags = None; n = 0
    while pc != 0x001D2DFA:
        n += 1
        if n > 50: raise RuntimeError("loop")
        x = arm[pc]; mn, ops = x.mnemonic, x.op_str; nxt = pc + x.size
        if mn == "mov" and ops == "eax, dword ptr [rdi + 0xae0]": eax = mem
        elif mn == "mov" and ops == "ecx, dword ptr [rdi + 0xae0]": ecx = mem
        elif mn == "mov" and ops == "dword ptr [rdi + 0xae0], eax": mem = eax
        elif mn == "test" and ops == "bl, bl": flags = ("z", bl == 0)
        elif mn == "test" and ops == "eax, eax": flags = ("le0", eax)
        elif mn == "cmp": flags = ("cmp", eax, x.operands[1].imm)
        elif mn == "dec" and ops == "eax": eax -= 1
        elif mn == "inc" and ops == "eax": eax += 1
        elif mn == "dec" and ops == "ecx": ecx -= 1
        elif mn == "je": nxt = x.operands[0].imm if flags[1] else nxt
        elif mn == "jle": nxt = x.operands[0].imm if flags[1] <= 0 else nxt
        elif mn == "jge": nxt = x.operands[0].imm if flags[1] >= flags[2] else nxt
        elif mn == "jmp": nxt = x.operands[0].imm
        else: raise RuntimeError("unmodelled " + show(x))
        pc = nxt
    return mem, ecx
for s in range(-1, 10):
    r0 = run(s, 0); r1 = run(s, 1)
    print("   state %2d: inc-branch -> field %2d index %2d | dec-branch -> field %2d index %2d" % (s, r0[0], r0[1], r1[0], r1[1]))
ok = all(0 <= run(s, b)[0] <= 8 and -1 <= run(s, b)[1] <= 7 for s in range(9) for b in (0, 1))
print("   closed on 0..8 with index -1..7:", ok)

print("D3 setter / initializer / constants")
for a, e in ((0x002F7A00, 0x002F7A07), (0x002F79E0, 0x002F79F1)):
    for x in tk.dis(a, e):
        t = ""
        for o in x.operands:
            if o.type == 3 and x.reg_name(o.mem.base) == "rip": t = " -> %08X size %d" % (x.address + x.size + o.mem.disp, o.size)
        print("  ", show(x), t)
raw16 = tk.d[tk.off(0x00D0F9E0):tk.off(0x00D0F9E0) + 16]
w = list(struct.unpack("<8H", raw16))
print("   00D0F9E0 section", tk.sec_of(0x00D0F9E0), "bytes", raw16.hex(), "words", w, "any in 511..534:", any(511 <= v <= 534 for v in w))
print("   01EEBAF0 section", tk.sec_of(0x01EEBAF0), "file offset", tk.off(0x01EEBAF0), "value", tk.u32(0x01EEBAF0))
print("   022BE930 section", tk.sec_of(0x022BE930), "file offset", tk.off(0x022BE930))

print("D4 callers")
blob = tk.d[tk.TRO:tk.TRO + min(tk.TVS, tk.TRS)]
def rel_sites(t):
    out = []
    for i in range(len(blob) - 6):
        a = tk.TVA + i; c = blob[i]
        if c in (0xE8, 0xE9) and a + 5 + struct.unpack_from("<i", blob, i + 1)[0] == t: out.append(("%s" % ("call" if c == 0xE8 else "jmp"), a))
        if c == 0x0F and 0x80 <= blob[i + 1] <= 0x8F and a + 6 + struct.unpack_from("<i", blob, i + 2)[0] == t: out.append(("jcc32", a))
        if (0x70 <= c <= 0x7F or c == 0xEB) and a + 2 + struct.unpack_from("<b", blob, i + 1)[0] == t: out.append(("rel8", a))
    return out
for t in (0x002F7A00, 0x002F79E0):
    rs = rel_sites(t)
    verified = []
    for kind, a in rs:
        xs = list(tk.dis(a, a + 8))
        if xs and xs[0].address == a and xs[0].operands and xs[0].operands[0].type == 2 and xs[0].operands[0].imm == t:
            b = tk.boundaries(a)
            verified.append("%s %08X in %s%s" % (kind, a, tk.fname(a), "" if (b is None or a in b) else " (off-boundary)"))
    rr, rraw = tk.rip_refs(t, t + 1)
    rel = tk.reloc_ptrs(t, t + 1)
    print("   %08X rel-branch sites (verified): %s" % (t, verified))
    print("   %08X rawcalls.json: %s | rip address-taken: %s | raw-only: %d | DIR64 relocs: %d" % (
        t, RAW.get("%X" % t), ["%08X %s" % (x.address, x.mnemonic) for x, k, tt in rr], len(rraw), len(rel)))

print("D5 index cell and word array references")
for lo, hi, nm in ((0x01EEBAF0, 0x01EEBAF4, "index 01EEBAF0"), (0x022BE930, 0x022BE940, "words 022BE930")):
    rr, rraw = tk.rip_refs(lo - 12, hi)
    rr = [(x, k, t) for x, k, t in rr if t + x.operands[k].size > lo and t < hi]
    dr, draw = tk.disp_refs(lo - 12 - 0x120000, hi - 0x120000)
    dr = [(x, k, v) for x, k, v in dr if x.operands[k].type == 3]
    rel = tk.reloc_ptrs(lo, hi)
    print("   %s: rip %d, image-base-relative %d, relocs %d, raw-only %d/%d" % (nm, len(rr), len(dr), len(rel), len(rraw), len(draw)))
    for x, k, t in rr:
        print("      %s  [%s size %d]  in %s" % (show(x), "W" if tk.is_store(x, k) else "R", x.operands[k].size, tk.fname(x.address)))
    for x, k, v in dr:
        print("      IB %s  [%s]  in %s" % (show(x), "W" if tk.is_store(x, k) else "R", tk.fname(x.address)))

print("D6 image-wide stores overlapping +0xAE0..+0xAE3 (disp32, any base)")
dr, draw = tk.disp_refs(0x0AD0, 0x0AE4)
stores = []
for x, k, v in dr:
    o = x.operands[k]
    if o.type != 3 or x.reg_name(o.mem.base) == "rip": continue
    if not tk.is_store(x, k): continue
    if o.mem.disp + o.size > 0xAE0 and o.mem.disp < 0xAE4:
        stores.append(x)
owners = {}
for x in stores: owners.setdefault(tk.fname(x.address), []).append(x)
print("   %d stores in %d functions" % (len(stores), len(owners)))
for f, xs in sorted(owners.items()):
    print("     %s: %s" % (f, "; ".join(show(x) for x in xs[:4]) + (" ..." if len(xs) > 4 else "")))
