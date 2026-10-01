"""SWE2-AUDIT-SPEC independent re-derivation of the OV29 title member-notification route (read-only on the image).
Own decode with tk.py (section-aware, function list + .pdata owners), raw call index rawcalls.json, raw rip sweeps.
Run from anywhere: python mn_indep.py > mn_indep.out
"""
import sys, os, json, struct
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, ROOT + r"\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(ROOT + r"\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def A(v): return v if isinstance(v, int) else v.address
def body(e):
    return list(tk.fdis(e))
def show(e, lo=None, hi=None, filt=None):
    for x in body(e):
        if lo is not None and not (lo <= x.address < hi): continue
        if filt and not filt(x): continue
        print("   %08X %-7s %s" % (x.address, x.mnemonic, x.op_str))
def calls(e):
    return [(x.address, x.op_str) for x in body(e) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")]

print("== S1 393FF0: direct call/jmp targets (owner %s, size %s)" % (tk.fname(0x393FF0), tk.fsize(0x393FF0)))
for a, t in calls(0x393FF0): print("   %08X -> %s" % (a, t))
for f in ("2493D0", "249320"):
    print("   raw callers of %s: %d; includes 393FF0 sites: %s" % (f, len(RAW.get(f, [])), [s for s in RAW.get(f, []) if tk.owner(int(s, 16)) and tk.owner(int(s, 16))[0] == 0x393FF0] if isinstance(tk.owner(0x393FF0), tuple) else [s for s in RAW.get(f, []) if 0x393FF0 <= int(s, 16) < 0x393FF0 + tk.fsize(0x393FF0)]))

print("== S2 factories 2493D0 / 249320 -> common 249210")
for e in (0x2493D0, 0x249320):
    print("  %08X size %s calls %s" % (e, tk.fsize(e), [(hex(a), t) for a, t in calls(e)]))
print("   raw callers of 249210: %d" % len(RAW.get("249210", [])))

print("== S3 249210 descriptor build (lea targets, stores, 32E620, +0x18)")
for x in body(0x249210):
    s = x.op_str
    if x.mnemonic == "lea" and "rip" in s:
        tgt = x.address + x.size + int(s.split("rip")[1].strip(" +]").replace("- ", "-").replace(" ", ""), 0) if False else None
    if (x.mnemonic in ("lea", "call", "inc") or ("[rsp + 0x3" in s or "[rsp + 0x4" in s or "[rbx]" in s)):
        extra = ""
        for op in x.operands:
            if op.type == 3 and op.mem.base == 41:  # X86_REG_RIP
                extra = " -> %08X" % (x.address + x.size + op.mem.disp)
        print("   %08X %-7s %s%s" % (x.address, x.mnemonic, s, extra))

print("== S4 2495C0 completion body (full)")
show(0x2495C0)
print("   size", tk.fsize(0x2495C0))

print("== S5 who forms 2495C0 / 248700 as an address (raw rip sweep, all .text)")
for tgt in (0x2495C0, 0x248700):
    rr, raw = tk.rip_refs(tgt, tgt + 1)
    print("  %08X: %d verified rip refs %s; raw-only %d; reloc ptrs %d" % (tgt, len(rr), ["%08X in %s" % (A(r[0]), tk.fname(A(r[0]))) for r in rr], len(raw), len(tk.reloc_ptrs(tgt, tgt + 1))))

print("== S6 separate watcher factory 2491B0 / handler 248700 / 2494F0")
print("  2491B0 calls", [(hex(a), t) for a, t in calls(0x2491B0)])
print("  248700 calls", [(hex(a), t) for a, t in calls(0x248700)])
print("  2494F0 owner", tk.fname(0x2494F0), "size", tk.fsize(0x2494F0))
show(0x2494F0, filt=lambda x: x.mnemonic == "call")
print("  24947D owner", tk.fname(0x24947D), " 24955D owner", tk.fname(0x24955D))

print("== S7 controller 582860: guard deriving the jump table")
e = 0x582860
bs = body(e)
for i, x in enumerate(bs):
    if x.mnemonic == "cmp" and x.op_str.endswith(", 0x12"):
        for y in bs[max(0, i - 3): i + 8]:
            print("   %08X %-7s %s" % (y.address, y.mnemonic, y.op_str))
print("  last instruction of the decoded body:", "%08X %s" % (bs[-1].address, bs[-1].mnemonic), " fsize", tk.fsize(e))
ents = [tk.u32(0x582F54 + 4 * k) for k in range(19)]
print("  table 582F54 x19 (rva -> va):", " ".join("%d:%08X" % (k, v + 0x120000) for k, v in enumerate(ents)))
print("  entry 20 (past bound):", "%08X" % (tk.u32(0x582F54 + 4 * 19) + 0x120000))
