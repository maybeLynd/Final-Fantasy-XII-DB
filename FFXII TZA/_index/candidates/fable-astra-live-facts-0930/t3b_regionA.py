"""T3b / OV-5 / OV-8 (d), bounded remainder (FABLE reader, 2026-09-29).  python t3b_regionA.py > t3b_regionA.out
Region A = active image 02164280 + 0x52DD4..0x5359B = state 021B290C + 0x4748..0x4F0F = 021B7054..021B781B.
S1  the save-file load copy into the active image (kind-9 storage packet)
S2  what runs after load: rebase bodies and the post-load lazy body 00233C10, call tree depth 3, scanned for any
    region-A writer shape (registry reference, disp 0x4748..0x4F0F store, call to a known region-A writer)
S3  0030FAA0 / 0030FBE0: every store and the handler route
S4  controlled sweeps of region A: image-base-relative (any base), rip-relative, absolute-VA; bulk control 002370D3"""
import json, os
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM
fails = 0
def check(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def at(a):
    fn, _ = tk.owner(a)
    for y in tk.fdis(fn):
        if y.address == a: return y
def show(a, note=""):
    y = at(a); print("  %08X  %-8s %-48s [%s] %s" % (a, y.mnemonic, y.op_str, tk.fname(a), note)); return y
IDX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(tk.__file__)), "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "tools", "rawcalls.json")))
A_LO, A_HI = 0x021B7054, 0x021B781C

print("== S1. the load copy (kind-9 storage packet)")
for a, n in ((0x005810BC, "dest = active image getter"), (0x005810EA, "packet kind 9"), (0x00581113, "packet +0x48 dest = rsi"),
             (0x00581117, "packet +0x50 size 0x56690"), (0x0058111E, "enqueue"), (0x0058218A, "queue dispatch: kind 9 arm"),
             (0x003BB477, "02B40EF0 = dest"), (0x003BB47E, "02B40EF8 = size"), (0x003BA874, ""), (0x003BA87B, ""), (0x003BA882, "read, state 6"),
             (0x003BA8A1, ""), (0x003BA8AE, "read, state 15"), (0x008625A4, "wrapper -> inner read"), (0x00866A46, "byte from backing store [01F44D40]"),
             (0x00866A4D, "BYTE STORE into dest")):
    show(a, n)
tbl = [0x120000 + tk.u32(0x0058220C + 4 * i) for i in range(13)]
check("S1-table", tbl[9] == 0x0058218A, "queue kind table 0058220C slot 9 = %08X" % tbl[9])
kind9 = []
for s in IDX.get("582540", []):
    s = int(s, 16); fn, _ = tk.owner(s)
    for y in tk.fdis(fn):
        if s - 0x60 <= y.address < s and y.mnemonic == "mov" and y.operands[0].type == X86_OP_MEM and y.operands[1].type == X86_OP_IMM and y.operands[1].imm == 9 and y.operands[0].size == 4:
            kind9.append((s, y.address))
print("  every EnqueueOperation site with a kind-9 immediate within 0x60 bytes before it:", [("%08X" % s, "%08X" % a) for s, a in kind9])
check("S1", [s for s, a in kind9] == [0x0058111E], "exactly one kind-9 enqueuer, 0058111E in SaveLoad_ControllerTransitionStateMachine")
w = IDX.get("3BB440", []); print("  callers of the kind-9 acceptance 003BB440:", w)
r = IDX.get("866A00", []); print("  callers of the inner read 00866A00:", r, "; of the wrapper 00862590:", IDX.get("862590", []))

print("\n== S2. after load: rebase bodies and the post-load lazy body, call tree depth 3")
WRITERS = {0x002FD150: "packed handler", 0x003008A0: "item modify (-> descriptor +0x48)", 0x003047F0: "zeroing loop", 0x002370C0: "state memset",
           0x00861EC0: "memset", 0x00861EBA: "memcpy", 0x002EF650: "full reset", 0x002EF5F0: "full clear"}
def scan(root, depth):
    seen = set(); hits = []; frontier = [(root, 0)]
    while frontier:
        f, dd = frontier.pop()
        if f in seen or tk.fsize(f) is None: continue
        seen.add(f)
        for y in tk.fdis(f):
            if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"):
                t = int(y.op_str, 16)
                if t in WRITERS: hits.append((f, y.address, "calls %08X %s" % (t, WRITERS[t])))
                elif tk.fsize(t) and dd < depth and not (f <= t < f + tk.fsize(f)): frontier.append((t, dd + 1))
            for k, op in enumerate(y.operands):
                if op.type != X86_OP_MEM: continue
                if op.mem.base and y.reg_name(op.mem.base) == "rip":
                    tt = y.address + y.size + op.mem.disp
                    if 0x01EEBCC0 <= tt < 0x01EEC1E8: hits.append((f, y.address, "registry ref %08X" % tt))
                    if A_LO <= tt < A_HI: hits.append((f, y.address, "rip into region A"))
                elif 0x4748 <= op.mem.disp <= 0x4F0F and tk.is_store(y, k):
                    hits.append((f, y.address, "store disp %#x: %s %s" % (op.mem.disp, y.mnemonic, y.op_str)))
    return seen, hits
for root in (0x00238A80, 0x0030B6A0, 0x00233C10):
    seen, hits = scan(root, 3)
    print("  root %08X: %d functions reached; region-A-writer shapes: %d" % (root, len(seen), len(hits)))
    for f, a, why in hits: print("     %08X in %s: %s" % (a, tk.fname(f), why))
seen, hits = scan(0x0023AF50, 3)
check("S2-control", any("state memset" in h[2] for h in hits) or any("zeroing loop" in h[2] for h in hits),
      "the same scan rooted at Inventory_InitializePrimaryStateFromAuthoredTable 0023AF50 finds a region-A writer: %s" % sorted(set(h[2] for h in hits))[:6])

print("\n== S3. 0030FAA0 (restore) / 0030FBE0 (snapshot): every non-stack store, and the handler route")
for fn in (0x0030FAA0, 0x0030FBE0):
    for y in tk.fdis(fn):
        for k, op in enumerate(y.operands):
            if op.type == X86_OP_MEM and tk.is_store(y, k) and not (op.mem.base and y.reg_name(op.mem.base) == "rsp"):
                inA = 0x4748 <= op.mem.disp <= 0x4F0F
                print("  %08X %-6s %-46s [%s] disp=%#x %s" % (y.address, y.mnemonic, y.op_str, tk.fname(y.address), op.mem.disp, "IN REGION A" if inA else ""))
        for y2 in tk.fdis(fn):
            if y2.mnemonic == "call" and y2.op_str.startswith("0x"): pass
print("  registry descriptor handler slot +0x48 (file bytes; rows 0-2 = classes 5/6/7):")
for i in range(3):
    b = 0x01EEBCC0 + i * 0x58
    print("    row %d %08X: +0=%#x +0x18=%#x +0x28=%#x +0x3C=%#x  +0x48 -> %08X" % (i, b, tk.u32(b), tk.u32(b + 0x18), tk.u32(b + 0x28), tk.u32(b + 0x3C), tk.u64(b + 0x48)))
rs = [a for a, q in tk.reloc_ptrs(0x002FD150, 0x002FD151)]
print("  stored pointers to 002FD150:", ["%08X" % a for a in rs])
check("S3-control", {0x01EEBD08, 0x01EEBD60, 0x01EEBDB8} <= set(rs), "reloc sweep finds the three +0x48 slots holding 002FD150")
st48, _ = tk.rip_refs(0x01EEBCC0, 0x01EEC1E8)
w48 = [x for x, k, t in st48 if tk.is_store(x, k)]
print("  rip-relative stores into the registry:", ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in w48])
for a, n in ((0x00300943, "descriptor +0x48"), (0x00300950, "r9d = channel"), (0x00300957, "r8d = abs/rel"), (0x0030095D, "edx = value"), (0x00300960, "call handler")):
    show(a, n)

print("\n== S4. controlled sweeps of region A 021B7054..021B781B")
hb, rawb = tk.disp_refs(A_LO - 0x120000, A_HI - 0x120000)
print("  image-base-relative (any base/index):", ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x, k, v in hb], "; unverified byte matches:", len(rawb))
hc, _ = tk.disp_refs(0x203F000, 0x203F001)
check("S4-ibr-control", any(x.address == 0x002DF7BF for x, k, v in hc), "the detector finds 002DF7BF [r15+rbx*8+0x203f000]")
hblk, _ = tk.disp_refs(0x02164280 - 0x120000, 0x021BA910 - 0x120000)
print("  image-base-relative into the WHOLE active image 02164280..021BA90F: %d (so no in-block control exists; the out-of-block control above stands)" % len(hblk))
check("S4-ibr", not hb, "no image-base-relative operand into region A")
hr, _ = tk.rip_refs(A_LO - 16, A_HI)
hr = [(x, k, t) for x, k, t in hr if t < A_HI and t + max(x.operands[k].size, 1) > A_LO]
check("S4-rip", not hr, "no rip-relative access overlaps region A: %s" % ["%08X" % x.address for x, k, t in hr])
ha, _ = tk.abs_refs(A_LO, A_HI)
ha = [(x, v) for x, v in ha if tk.owner(x.address)[0] is not None]
check("S4-abs", not ha, "no absolute-VA form into region A: %s" % ["%08X" % x.address for x, v in ha])
check("S4-reloc", not tk.reloc_ptrs(A_LO, A_HI), "no stored qword pointer into region A")
y = show(0x002370C4); z = show(0x002370CD); show(0x002370D3)
base = 0x4E68C; lo, hi = base, base + z.operands[1].imm
check("S4-bulk-control", lo <= 0x52DD4 and hi >= 0x5359C, "002370D3 memset([02EBF190]=image+%#x, 0, %#x) covers image %#x..%#x, which contains region A 0x52DD4..0x5359B" % (base, z.operands[1].imm, lo, hi))
print("\nFAILS", fails)
