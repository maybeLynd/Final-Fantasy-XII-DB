"""sdreaders_indep.py - SWE2-AUDIT-SPEC independent checks for sd7-slot15-callers-0930 and sd40-42-header-readers-0930
(OPUS, c7551f2de). Static, read-only; tk.py raw sweeps + the raw call index, not the author's value-flow engine.

SD-7:
  V1  008C5760 + 0x78 and base vtable 01CB2508 + 0x78 (the shared stub).
  V2  every rel32 E8 / E9 / 0F 8x in .text whose target is 0017D1A0 (raw byte sweep, jcc included) + raw call index.
  V3  every stored qword equal to 0017D1A0 (reloc table and unaligned raw qword scan of the whole file).
  V4  code that names the vtable or its slot-15 entry directly (rip refs into 008C5760..008C5860 and to 008C57D8).
  V5  every `call`/`jmp qword [reg + 0x78]` (disp8 or disp32, any base/index, REX or not) in .text, found by raw
      opcode sweep and verified by decoding on the owner's instruction boundary; count, and how many fall in
      00790000-007A8000.
SD-40/42:
  H1  rip-relative and image-base-relative accesses whose target is one of the four fields (+0x48, +0x4C, +0x58, +0x60,
      each 4 or 8 bytes wide) of the four header images, with width and read/write. (Direct global addressing only;
      the author's census covers pointer flow.)
"""
import sys, json, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM
rc = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
T = 0x0017D1A0
print("V1 008C5760+0x78 = %08X ; 01CB2508+0x78 = %08X" % (tk.u64(0x008C5760 + 0x78) or 0, tk.u64(0x01CB2508 + 0x78) or 0))
d, TVA, TRS, TRO = tk.d, tk.TVA, tk.TRS, tk.TRO
hits = []
for o in range(TRO, TRO + TRS - 5):
    b = d[o]
    if b in (0xE8, 0xE9):
        va = TVA + (o - TRO)
        if va + 5 + struct.unpack_from("<i", d, o + 1)[0] == T: hits.append(("%08X" % va, "E8" if b == 0xE8 else "E9"))
    elif b == 0x0F and 0x80 <= d[o + 1] <= 0x8F:
        va = TVA + (o - TRO)
        if va + 6 + struct.unpack_from("<i", d, o + 2)[0] == T: hits.append(("%08X" % va, "0F%02X" % d[o + 1]))
print("V2 raw rel32 call/jmp/jcc to 0017D1A0: %s ; raw call index: %s" % (hits, rc.get("17D1A0")))
print("V3 relocated qwords = 0017D1A0: %s ; raw unaligned qwords: %s" % (
    ["%08X" % a for a, q in tk.reloc_ptrs(T, T + 1)], ["%08X %s" % (a, s) for a, q, s in tk.raw_q(T, T + 1)]))
refs, raw = tk.rip_refs(0x008C5760, 0x008C5860)
print("V4 rip refs into vtable 008C5760..+0x100: %d %s" % (len(refs), ["%08X %s %s -> %08X" % (x.address, x.mnemonic, x.op_str, t) for x, k, t in refs][:12]))
# V5
cands = set()
for o in range(TRO, TRO + TRS - 8):
    if d[o] != 0xFF: continue
    m = d[o + 1]; mod, reg, rm = m >> 6, (m >> 3) & 7, m & 7
    if reg not in (2, 4) or mod not in (1, 2): continue
    p = o + 2 + (1 if rm == 4 else 0)
    disp = d[p] if mod == 1 else struct.unpack_from("<I", d, p)[0]
    if disp == 0x78:
        va = TVA + (o - TRO)
        cands.add(va); cands.add(va - 1)  # possible REX prefix
sites = {}
for va in sorted(cands):
    for s in (va, va - 1):
        pass
for va in sorted(cands):
    o = tk.off(va)
    x = next(tk.md.disasm(d[o:o + 15], va, 1), None)
    if x is None or x.mnemonic not in ("call", "jmp"): continue
    op = x.operands[0]
    if op.type != X86_OP_MEM or op.mem.disp != 0x78 or tk.md.reg_name(op.mem.base) == "rip": continue
    own, how = tk.owner(va)
    if own is not None:
        b = tk.boundaries(va) if hasattr(tk, "boundaries") else None
        if b is not None and va not in b: continue
    sites[va] = (x.mnemonic, x.op_str, own)
fw = [a for a in sites if 0x00790000 <= a < 0x007A8000]
print("V5 call/jmp qword [reg+0x78] sites on instruction boundaries: %d in %d owners; in 00790000-007A8000: %d %s" % (
    len(sites), len(set(v[2] for v in sites.values())), len(fw), ["%08X" % a for a in fw]))
print("V5 unowned sites: %s" % ["%08X" % a for a, v in sites.items() if v[2] is None][:10])
# H1
IMGS = {"active": 0x02164280, "capture": 0x021BA940, "third": 0x02211000, "backup": 0x022676C0}
for nm, b in IMGS.items():
    lo, hi = b + 0x48, b + 0x68
    r, rr = tk.rip_refs(lo, hi)
    dr, dr_raw = tk.disp_refs(lo - tk.BASE, hi - tk.BASE)
    rows = []
    for x, k, t in r:
        rows.append("%08X %s %s [+%#x w%d %s] %s" % (x.address, x.mnemonic, x.op_str, t - b, tk.memsize(x, k), "W" if tk.is_store(x, k) else "R", tk.fname(x.address)))
    for x, k, v in dr:
        rows.append("%08X %s %s [ib +%#x w%d %s] %s" % (x.address, x.mnemonic, x.op_str, v + tk.BASE - b, tk.memsize(x, k), "W" if tk.is_store(x, k) else "R", tk.fname(x.address)))
    print("H1 %s %08X fields +0x48..+0x67: rip %d, image-base %d, raw-only %d/%d" % (nm, b, len(r), len(dr), len(rr), len(dr_raw)))
    for s in rows: print("   " + s)
