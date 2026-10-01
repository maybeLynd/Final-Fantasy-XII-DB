"""SWE2-AUDIT-SPEC independent re-derivation for ASTRA special-action-override-label-binding (2026-09-30).
tk.py decode, not the packet's capture/reducer.
 L1 emulate 001D03E1..001D04D1: track register immediates/rip loads, apply every [rdi+disp] store into a byte map
    over +0xAE4..+0xC03 (nine 32-byte slots); report each slot's written prefix up to the first written NUL,
    unwritten bytes left as '?'; and list every instruction in the span that is a branch/call/ret
 L2 the object register: rdi at 001D03C3 and any rdi redefinition before 001D04D1
 L3 the formatter switch: guard (lea/cmp/ja), the dispatch instruction and its table base, the byte before the
    table (ret), the 294 entries, which item ids reach 001CE9AA; one-past entry decoded as a control
 L4 the item-182 arm 001CE9AA..: stride, base +0xAE4, sign extension, no clamp before use; r15 writes in the formatter
 L5 the format literal at 008FFAE0 and the word table 00D0F9E0 (state k -> word k-1)
"""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
def show(x): return "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
FAM = {}
for fam, names in {"a": "rax eax ax al", "c": "rcx ecx cx cl", "d": "rdx edx dx dl", "r8": "r8 r8d r8w r8b",
                   "r9": "r9 r9d r9w r9b", "x0": "xmm0", "x1": "xmm1"}.items():
    for n in names.split(): FAM[n] = fam

print("L1/L2 initializer 001D03E1..001D04D1")
span = [x for x in tk.dis(0x001D03E1, 0x001D04F0) if x.address <= 0x001D04D1]
print("   instructions %d, first %08X last %08X" % (len(span), span[0].address, span[-1].address))
flow = [show(x) for x in span if x.mnemonic.startswith("j") or x.mnemonic in ("call", "ret")]
print("   branch/call/ret inside:", flow or "none")
rdi_def = [show(x) for x in tk.dis(0x001D03C3, 0x001D04F0) if x.address <= 0x001D04D1 if x.operands and x.operands[0].type == X86_OP_REG
           and x.reg_name(x.operands[0].reg) in ("rdi", "edi") and x.mnemonic not in ("cmp", "test", "push")]
print("   rdi definitions 001D03C3..001D04D1:", rdi_def)
regs = {}; slots = [dict() for _ in range(9)]; stores = 0; other = []
for x in span:
    ops = x.operands
    if len(ops) == 2 and ops[0].type == X86_OP_REG:
        dst = x.reg_name(ops[0].reg); f = FAM.get(dst)
        if f and x.mnemonic in ("mov", "movabs") and ops[1].type == X86_OP_IMM:
            regs[f] = ops[1].imm & ((1 << (8 * ops[0].size)) - 1)
        elif f and x.mnemonic in ("mov", "movsd", "movzx", "movss", "movups", "movdqu", "movdqa") and ops[1].type == X86_OP_MEM and x.reg_name(ops[1].mem.base) == "rip":
            a = x.address + x.size + ops[1].mem.disp; n = ops[1].size
            regs[f] = int.from_bytes(tk.d[tk.off(a):tk.off(a) + n], "little")
        elif f:
            regs.pop(f, None)
    if len(ops) == 2 and ops[0].type == X86_OP_MEM and x.reg_name(ops[0].mem.base) == "rdi":
        disp, n = ops[0].mem.disp, ops[0].size
        if not (0xAE4 <= disp < 0xC04):
            other.append(show(x)); continue
        if ops[1].type == X86_OP_IMM: v = ops[1].imm & ((1 << (8 * n)) - 1)
        else: v = regs[FAM[x.reg_name(ops[1].reg)]] & ((1 << (8 * n)) - 1)
        stores += 1
        for k, byte in enumerate(v.to_bytes(n, "little")):
            off = disp - 0xAE4 + k; s, loc = divmod(off, 32)
            if loc in slots[s] and slots[s][loc] != byte: raise RuntimeError("conflict")
            slots[s][loc] = byte
print("   stores into +0xAE4..+0xC03: %d; [rdi+disp] stores elsewhere: %s" % (stores, other or "none"))
for s, m in enumerate(slots):
    txt = ""; term = None
    for k in range(32):
        if k not in m: txt += "?"; continue
        if m[k] == 0: term = k; break
        txt += chr(m[k])
    written = sorted(m)
    print("   slot %d (+0x%X): %-16r NUL at %s; bytes written %d (last written offset %s); unwritten after NUL: %d" % (
        s, 0xAE4 + 32 * s, txt, term, len(m), written[-1] if written else None, 32 - len(m)))

print("L3 formatter switch")
f = list(tk.fdis(0x001CD100)) if tk.owner(0x001CD141)[0] == 0x001CD100 else None
o, how = tk.owner(0x001CD141); print("   owner of 001CD141:", "%08X" % o, how, tk.fname(o))
body = {x.address: x for x in tk.dis(o, 0x001CFCEC)}
for a in sorted(body):
    if 0x001CD130 <= a <= 0x001CD1E0: print("  ", show(body[a]))
print("   byte at 001CFCEB = %02X; last decoded before table: %s" % (tk.d[tk.off(0x001CFCEB)], show(body[max(a for a in body if a < 0x001CFCEC)])))
tab = [tk.u32(0x001CFCEC + 4 * i) + 0x120000 for i in range(295)]
arm = [i for i in range(294) if tab[i] == 0x001CE9AA]
print("   entries 294, distinct targets %d, all inside owner: %s" % (len(set(tab[:294])), all(o <= t < 0x001CFCEC for t in tab[:294])))
print("   index(es) reaching 001CE9AA: %s -> item id(s) %s (item = index + 1 by the lea eax,[r13-1])" % (arm, [i + 1 for i in arm]))
print("   one-past entry 295th dword = %08X (+base)" % tab[294], "inside owner code:", o <= tab[294] < 0x001CFCEC)

print("L4 item-182 arm")
for a in sorted(body):
    if 0x001CE9AA <= a < 0x001CE9C9: print("  ", show(body[a]))
for a in sorted(body):
    if 0x001CD57F <= a <= 0x001CD58A or 0x001CD4FF <= a <= 0x001CD51C: print("  ", show(body[a]))
r15w = [show(body[a]) for a in sorted(body) if body[a].operands and body[a].operands[0].type == X86_OP_REG
        and body[a].reg_name(body[a].operands[0].reg) in ("r15", "r15d") and body[a].mnemonic not in ("cmp", "test", "push")]
print("   r15 definitions in the owner (linear decode):", r15w)

print("L5 constants")
s = tk.d[tk.off(0x008FFAE0):tk.off(0x008FFAE0) + 32].split(b"\0")[0]
print("   008FFAE0:", s)
print("   00D0F9E0 words:", list(struct.unpack("<8H", tk.d[tk.off(0x00D0F9E0):tk.off(0x00D0F9E0) + 16])))
