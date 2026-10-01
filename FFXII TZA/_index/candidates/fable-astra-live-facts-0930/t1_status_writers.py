"""T1 / OV-33 (i): writer set of the read-layer status dword 0215EFF4 (FABLE reader, 2026-09-29).
Run from this directory:  python t1_status_writers.py > t1_status_writers.out
Every sweep prints its positive control first; a sweep whose control is absent is marked VOID."""
import json, os, struct, bisect
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG
T, CELL = 0x0215EFF4, 0x01F82CC0
RB = tk.BASE
def line(x, k=None, extra=""):
    s = "%08X  %-8s %-46s [%s]" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address))
    if k is not None:
        s += "  %s size=%d" % ("STORE" if tk.is_store(x, k) else "read/form", x.operands[k].size)
    return s + extra
def covers(t, size, want): return t <= want < t + max(size, 1)
fails = 0
def check(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)

print("== A. rip-relative references whose access covers 0215EFF4 (raw .text sweep, not function-list bounded)")
h, raw = tk.rip_refs(T - 16, T + 4)
known = {0x002DF719, 0x002DF75F, 0x002DF808, 0x002DF838, 0x0046DFE7, 0x0046E0E0}
found = set()
for x, k, t in h:
    sz = x.operands[k].size if x.mnemonic != "lea" else 1
    if t == T or covers(t, sz, T):
        found.add(x.address); print("  " + line(x, k, "  -> %08X" % t))
print("  raw-only (unverified) hits:", [("%08X" % p, "%08X" % t) for p, t in raw])
check("A-control", known <= found, "the six known rip references (4 lea by the issuers, 2 reads) are all found: %s" % sorted("%08X" % a for a in known - found))
check("A", all(not tk.is_store(x, k) for x, k, t in h if x.address in found), "no rip-relative STORE covers 0215EFF4")

print("\n== B. image-base-relative displacements [reg + (VA - 0x120000)] in the window 0215EE00..0215F200 (disp 0x203EE00..0x203F200)")
hb, rawb = tk.disp_refs(0x203EE00, 0x203F200)
for x, k, v in hb:
    t = v + RB
    print("  " + line(x, k, "  -> base+disp = %08X%s" % (t, "  (indexed)" if x.operands[k].mem.index else "")))
print("  raw-only (unverified) disp hits:", len(rawb), [("%08X" % p, "%08X" % (v + RB), tk.fname(p)) for p, v in rawb][:20])
check("B-control", any(x.address == 0x002DF7BF for x, k, v in hb), "the known image-base-relative read 002DF7BF [r15+rbx*8+0x203f000] is found by the same detector")
direct = [(x, k, v) for x, k, v in hb if not x.operands[k].mem.index and covers(v + RB, x.operands[k].size, T)]
check("B", not direct, "no non-indexed image-base-relative access covers 0215EFF4: %d" % len(direct))
hbs = [(x, k, v) for x, k, v in hb if tk.is_store(x, k)]
print("  image-base-relative STORES in the window:", [line(x, k) for x, k, v in hbs])

print("\n== C. stored absolute pointers (DIR64 relocations and raw unaligned qwords) into 0215EE00..0215F000 and to the cell 01F82CC0")
rp = tk.reloc_ptrs(0x0215EE00, 0x0215F000) + tk.reloc_ptrs(CELL, CELL + 8)
print("  reloc pointers:", [("%08X" % a, "%08X" % q) for a, q in rp])
rq = tk.raw_q(0x0215EE00, 0x0215F000) + tk.raw_q(CELL, CELL + 8)
print("  raw qwords:", [("%08X" % a, "%08X" % q, s) for a, q, s in rq])
ctl = tk.reloc_ptrs(0x00793EB0, 0x00793EB1)
check("C-control", any(a == 0x01CB2508 for a, q in ctl), "reloc sweep finds the vtable 01CB2508 slot 0 -> 00793EB0: %s" % [("%08X" % a) for a, q in ctl])
check("C", not rp and not rq, "no stored pointer to 0215EE00..0215EFFF or to 01F82CC0 anywhere in the file")

print("\n== D. the pointer cell 01F82CC0: every rip reference (raw sweep), and image-base-relative forms")
hc, rawc = tk.rip_refs(CELL - 8, CELL + 8)
for x, k, t in hc:
    if covers(t, x.operands[k].size, CELL): print("  " + line(x, k, "  -> %08X" % t))
print("  raw-only:", [("%08X" % p, "%08X" % t) for p, t in rawc])
hcb, _ = tk.disp_refs(CELL - RB - 8, CELL - RB + 8)
print("  image-base-relative forms of the cell:", [line(x, k) for x, k, v in hcb])
cell_refs = [x.address for x, k, t in hc if covers(t, x.operands[k].size, CELL)]
check("D-control", {0x001D6D70, 0x001D6D7E, 0x001D6DCD, 0x001D6FED} <= set(cell_refs), "the load 001D6D70, clear 001D6D7E and stores 001D6DCD/001D6FED are found")
check("D", len(cell_refs) == 4 and not hcb, "exactly four references, no image-base-relative form: %s" % ["%08X" % a for a in cell_refs])

print("\n== E. stores through the register loaded from the cell (per loading function; register followed to overwrite / call / ret)")
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
def fam(r):
    m = {"eax": "rax", "ax": "rax", "al": "rax", "ecx": "rcx", "cx": "rcx", "cl": "rcx", "edx": "rdx", "dx": "rdx", "dl": "rdx"}
    return m.get(r, r[:-1] if r.startswith("r") and r[-1] in "dwb" and r[1:-1].isdigit() else r)
for x, k, t in hc:
    if not covers(t, x.operands[k].size, CELL) or tk.is_store(x, k) or x.mnemonic != "mov": continue
    fn, _ = tk.owner(x.address); ins = tk.fdis(fn)
    live = {fam(x.reg_name(x.operands[0].reg))}
    print("  load %08X in %s -> %s" % (x.address, tk.fname(x.address), live))
    started = False
    for y in ins:
        if y.address == x.address: started = True; continue
        if not started: continue
        for kk, op in enumerate(y.operands):
            if op.type == X86_OP_MEM and op.mem.base and fam(y.reg_name(op.mem.base)) in live:
                print("     %s" % line(y, kk, "  disp=%#x" % op.mem.disp))
        if y.mnemonic == "mov" and y.operands[0].type == X86_OP_REG and y.operands[1].type == X86_OP_REG and fam(y.reg_name(y.operands[1].reg)) in live:
            live.add(fam(y.reg_name(y.operands[0].reg))); print("     copy %s" % line(y))
        elif y.operands and y.operands[0].type == X86_OP_REG and fam(y.reg_name(y.operands[0].reg)) in live and y.mnemonic not in ("test", "cmp"):
            live.discard(fam(y.reg_name(y.operands[0].reg))); print("     overwritten %s" % line(y))
        if y.mnemonic in ("call", "ret") or not live:
            print("     end at %s" % line(y)); break

print("\n== F. what can be stored INTO the cell: every store's source, and every caller of the two storers (raw E8/E9 + address-takes)")
idx = json.load(open(os.path.join(os.path.dirname(tk.__file__), "..", "pub140-scratch", "tools", "rawcalls.json")))
for fnaddr, slot in ((0x001D6D90, 0x20), (0x001D6FB0, 0x28), (0x001D6D70, None)):
    sites = [int(a, 16) for a in idx.get("%X" % fnaddr, [])]
    lr, _ = tk.rip_refs(fnaddr, fnaddr + 1)
    rel = tk.reloc_ptrs(fnaddr, fnaddr + 1)
    print("  %08X: E8/E9 sites %s; rip address-takes %s; stored pointers %s" % (fnaddr, ["%08X" % s for s in sites],
          [line(x) for x, k, t in lr], ["%08X" % a for a, q in rel]))
    if slot is None: continue
    for s in sites:
        fn, _ = tk.owner(s); ins = tk.fdis(fn)
        pre = [y for y in ins if s - 0x40 <= y.address < s]
        st = [y for y in pre if y.mnemonic == "mov" and y.operands[0].type == X86_OP_MEM and y.reg_name(y.operands[0].mem.base) == "rsp" and y.operands[0].mem.disp == slot]
        for y in st:
            src = y.reg_name(y.operands[1].reg) if y.operands[1].type == X86_OP_REG else y.op_str
            lea = [z for z in pre if z.address < y.address and z.mnemonic == "lea" and z.operands[0].type == X86_OP_REG and z.reg_name(z.operands[0].reg) == src]
            print("     call %08X: arg slot [rsp+%#x] <- %s  | %s" % (s, slot, line(y), line(lea[-1]) if lea else "?"))
check("F-control", True, "(see the four call sites above: 002DF735/002DF777/002DF821/002DF853)")

print("\n== G. address formation BELOW the target: lea / rip bases in 0215E000..0215EFF4 (for bulk/loop writes that could run into it)")
hg, _ = tk.rip_refs(0x0215E000, T)
for x, k, t in hg:
    if x.mnemonic == "lea": print("  " + line(x, None, "  -> %08X  (gap to target %#x)" % (t, T - t)))
print("\n== H. absolute 32-bit VA forms (imm32 / base-less or based disp32 equal to the VA itself; the PE has no DYNAMIC_BASE)")
ha, _ = tk.abs_refs(0x0215EE00, 0x0215F200)
hb2, _ = tk.abs_refs(CELL - 8, CELL + 8)
ha = [(x, v) for x, v in ha + hb2 if tk.owner(x.address)[0] is not None]
print("  hits in owned code:", ["%08X %s %s -> %08X [%s]" % (x.address, x.mnemonic, x.op_str, v, tk.fname(x.address)) for x, v in ha])
hc2, _ = tk.abs_refs(0x02000000, 0x02000001)
check("H-control", any(x.address == 0x001A14E6 for x, v in hc2), "the same detector finds the imm32 0x02000000 at 001A14E6 (mov edx, 0x2000000)")
check("H", not ha, "no absolute-VA form of 0215EE00..0215F1FF or of the cell")
print("\nFAILS", fails)
