"""T2 / PC-1: can the FF12CONFIG override dwords 01E02804 / 01E02810 be written by any route in the image?
(FABLE reader, 2026-09-29).  Run from this directory:  python t2_pc1_override.py > t2_pc1_override.out
Routes the 2026-09-27 census (pc1-pointer-store) did not cover: raw .text sweeps not bounded by the function list,
image-base-relative forms with ANY base register over a 0x300-byte window, stored pointers up to 0x200 below the
targets (a table base that could be indexed into them), absolute 32-bit VA forms, and every rip-relative address
formation in 01E02700..01E02900 followed to the stores made through it."""
import struct
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG
TG = (0x01E02804, 0x01E02810)
RB = tk.BASE
fails = 0
def check(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def line(x, k=None):
    s = "%08X  %-9s %-46s [%s]" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address))
    if k is not None: s += "  %s size=%d" % ("STORE" if tk.is_store(x, k) else "read", x.operands[k].size)
    return s
def hits_target(t, size): return [g for g in TG if t <= g < t + max(size, 1)]

print("== .data bytes 01E027F0..01E0281F (file):")
for a in range(0x01E027F0, 0x01E02820, 16):
    print("  %08X  %s" % (a, " ".join("%08X" % tk.u32(a + i) for i in range(0, 16, 4))))

print("\n== S1. rip-relative accesses covering either target (raw .text sweep, any width, bases up to 16 bytes below)")
h, raw = tk.rip_refs(0x01E027F0, 0x01E02814)
cov = [(x, k, t) for x, k, t in h if x.mnemonic != "lea" and hits_target(t, x.operands[k].size)]
for x, k, t in cov: print("  " + line(x, k) + "  -> %08X covers %s" % (t, ["%08X" % g for g in hits_target(t, x.operands[k].size)]))
print("  raw-only (unverified):", [("%08X" % p, "%08X" % t) for p, t in raw])
check("S1-control", {0x00408CC3, 0x00408DCB} <= {x.address for x, k, t in cov}, "the known reads 00408CC3 (01E02804) and 00408DCB (01E02810) are found by this sweep")
check("S1", all(not tk.is_store(x, k) for x, k, t in cov), "no rip-relative store covers either target; accesses: %s" % ["%08X" % x.address for x, k, t in cov])

print("\n== S2. image-base-relative displacements, any base / index register, disp in [0x1CE2600, 0x1CE2900) (= VA 01E02600..01E02900)")
hb, rawb = tk.disp_refs(0x1CE2600, 0x1CE2900)
for x, k, v in hb: print("  " + line(x, k) + "  -> %08X" % (v + RB))
print("  raw-only (unverified disp32 byte matches):", [("%08X" % p, "%08X" % (v + RB), tk.fname(p)) for p, v in rawb])
hc, _ = tk.disp_refs(0x203F000, 0x203F001)
check("S2-control", any(x.address == 0x002DF7BF for x, k, v in hc), "the same detector finds the image-base-relative read 002DF7BF [r15+rbx*8+0x203f000]")
check("S2", not hb, "no image-base-relative operand into 01E02600..01E028FF: %d" % len(hb))

print("\n== S3. stored absolute pointers: DIR64 relocations and raw unaligned qwords anywhere in the file into [01E02604, 01E02814)")
rp = tk.reloc_ptrs(0x01E02604, 0x01E02814); rq = tk.raw_q(0x01E02604, 0x01E02814)
print("  reloc:", [("%08X" % a, "%08X" % q) for a, q in rp]); print("  raw qwords:", [("%08X" % a, "%08X" % q, s) for a, q, s in rq])
dv = {"%08X" % g: (tk.d.count(struct.pack("<I", g)), tk.d.count(struct.pack("<I", g - RB))) for g in TG}
print("  raw dword counts (VA, RVA) anywhere in the file:", dv)
ctl = tk.reloc_ptrs(0x00793EB0, 0x00793EB1)
check("S3-control", any(a == 0x01CB2508 for a, q in ctl), "the reloc sweep finds the vtable 01CB2508 slot 0 -> 00793EB0")
check("S3", not rp and not rq, "no stored qword pointer into [01E02604, 01E02814)")

print("\n== S4. absolute 32-bit VA forms (imm32 / disp32 equal to a VA in 01E02600..01E02900), owned code only")
ha, rawa = tk.abs_refs(0x01E02600, 0x01E02900)
ha = [(x, v) for x, v in ha if tk.owner(x.address)[0] is not None]
for x, v in ha: print("  %s -> %08X" % (line(x), v))
hc2, _ = tk.abs_refs(0x02000000, 0x02000001)
check("S4-control", any(x.address == 0x001A14E6 for x, v in hc2), "the same detector finds the imm32 0x02000000 at 001A14E6")
st4 = [(x, v) for x, v in ha if x.operands and x.operands[0].type == X86_OP_MEM and tk.is_store(x, 0)]
print("  note: a disp32 in this range with an image-base register (e.g. rdx = lea 00120000) is an image-base-relative access to VA+0x120000, not to this window")
check("S4", not st4, "no absolute-VA-form STORE in 01E02600..01E028FF (hits, all reads: %s)" % ["%08X" % x.address for x, v in ha])

print("\n== S5. every rip-relative ADDRESS FORMATION (lea) into 01E02700..01E02900, register followed to the stores made through it")
hl, _ = tk.rip_refs(0x01E02700, 0x01E02900)
leas = [(x, k, t) for x, k, t in hl if x.mnemonic == "lea"]
def fam(r):
    m = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp"}
    if r in m: return m[r]
    if r.startswith("r") and r[-1] in "dwb" and r[1:-1].isdigit(): return r[:-1]
    return r
reach = []
callee_seen = {}
def callee_check(c, regs, t):
    """one level: stores in the callee through the argument register before that register is overwritten"""
    key = (c, tuple(sorted(regs)))
    if key in callee_seen: return
    ins = tk.fdis(c) if tk.fsize(c) else []
    live = set(regs); out = []
    for y in ins:
        for kk, op in enumerate(y.operands):
            if op.type == X86_OP_MEM and op.mem.base and fam(y.reg_name(op.mem.base)) in live and tk.is_store(y, kk):
                out.append("%08X %s %s" % (y.address, y.mnemonic, y.op_str))
                if op.mem.index or hits_target(t + op.mem.disp, op.size): reach.append((y.address, t + op.mem.disp, op.size, "callee"))
        if y.operands and y.operands[0].type == X86_OP_REG and fam(y.reg_name(y.operands[0].reg)) in live and y.mnemonic not in ("test", "cmp", "push"):
            live.discard(fam(y.reg_name(y.operands[0].reg)))
        if not live or y.mnemonic in ("ret", "jmp", "call"): break
    callee_seen[key] = out
    print("       callee %08X, arg %s: stores through it before overwrite/call/ret: %s" % (c, sorted(regs), out or "none"))
for x, k, t in leas:
    fn, _ = tk.owner(x.address); ins = tk.fdis(fn); r0 = fam(x.reg_name(x.operands[0].reg))
    live = {r0}; print("  %s -> %08X" % (line(x), t))
    on = False
    for y in ins:
        if y.address == x.address: on = True; continue
        if not on: continue
        for kk, op in enumerate(y.operands):
            if op.type == X86_OP_MEM and op.mem.base and fam(y.reg_name(op.mem.base)) in live:
                sz = op.size; lo = t + op.mem.disp
                tag = "STORE" if tk.is_store(y, kk) else "read"
                idx = " +index" if op.mem.index else ""
                print("     %s %s: [%08X, +%d)%s" % (tag, line(y), lo, sz, idx))
                if tag == "STORE" and (op.mem.index or hits_target(lo, sz)): reach.append((y.address, lo, sz, idx))
        if y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == X86_OP_MEM and y.operands[1].type == X86_OP_REG and fam(y.reg_name(y.operands[1].reg)) in live:
            print("     ESCAPES (stored as a pointer): %s" % line(y))
        if y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == X86_OP_REG and y.operands[1].type == X86_OP_REG and fam(y.reg_name(y.operands[1].reg)) in live:
            live.add(fam(y.reg_name(y.operands[0].reg)))
        elif y.operands and y.operands[0].type == X86_OP_REG and fam(y.reg_name(y.operands[0].reg)) in live and y.mnemonic not in ("test", "cmp", "push"):
            live.discard(fam(y.reg_name(y.operands[0].reg)))
        if y.mnemonic in ("call", "ret", "jmp") or not live:
            if y.mnemonic == "call" and live & {"rcx", "rdx", "r8", "r9"}:
                print("     PASSED TO CALL: %s (live %s)" % (line(y), sorted(live)))
                if y.op_str.startswith("0x"): callee_check(int(y.op_str, 16), live & {"rcx", "rdx", "r8", "r9"}, t)
            break
callee_check(0x004B9A10, {"rcx"}, 0)
check("S5-callee-control", any("004B9A20" in z for z in callee_seen.get((0x004B9A10, ("rcx",)), [])), "the one-level callee check finds 004B9A10's store 004B9A20 movss [rcx+0xc] when told rcx is the pointer")
check("S5-control", {0x001AF5EA, 0x001AF606} <= {x.address for x, k, t in leas}, "the known address-takes 001AF5EA (01E027F0) and 001AF606 (01E027F4) are found")
check("S5", not reach, "no store through a formed address reaches a target or is indexed: %s" % reach)

print("\n== S6. the escaped pointers: 001AF470's registry slots +0x3BE8 (01E027F0) and +0x40C0 (01E027F4)")
print("  (a) every other instruction with displacement 0x3BE8 / 0x40C0 / 0x3B00 (raw disp sweep over .text):")
for lo in (0x3BE8, 0x40C0, 0x3B00):
    hs, _ = tk.disp_refs(lo, lo + 1)
    for x, k, v in hs: print("     %s" % line(x, k))
print("  (b) the consumer 001CA600 (rbx = 001B1C00() + 0x3B00 at 001CA63F): loads of slot +0xE8 / +0x5C0 and the store through each")
ins = tk.fdis(0x001CA600)
for i, y in enumerate(ins):
    for kk, op in enumerate(y.operands):
        if op.type == X86_OP_MEM and op.mem.base and y.reg_name(op.mem.base) == "rbx" and op.mem.disp in (0xE8, 0x5C0) and not op.mem.index:
            print("     %s" % line(y, kk))
            for z in ins[i + 1:i + 4]:
                for q, o2 in enumerate(z.operands):
                    if o2.type == X86_OP_MEM and o2.mem.base and z.reg_name(o2.mem.base) == y.reg_name(y.operands[0].reg):
                        print("        -> %s disp=%#x" % (line(z, q), o2.mem.disp))
lb = [y for y in ins if y.mnemonic == "lea" and "0x3b00" in y.op_str]
check("S6-control", any(y.address == 0x001CA63F for y in lb), "the consumer's registry base 001CA63F lea rbx,[rax+0x3b00] is found")
print("\nFAILS", fails)
