"""queue_escape2.py - follow-ups to queue_escape.py.

  1. the 33 rip-relative operands into 022C31C0..022C51F0: address, instruction, target, and whether the target is a
     slot's +0 (022C31C0 + k*0x80) read by a non-lea
  2. every rip-relative STORE in the module and its target (a slot pointer published outside the pool/list record?)
  3. external callers (E8/E9/jcc raw + relocated pointers) of every module entry, and for the two entries that return
     a pool pointer (0032E450 returns 022C31C0 in rax; 0032E990 returns the popped slot) whether a caller outside the
     module exists
  4. the callees that may receive a stale slot pointer in rcx (0046DD50 at 0032E2A0, 003EADD0 at 0032E29B,
     003EB050 at 0032EA99 with rcx = slot 63 + 0x68 left by 0032E450): full .pdata body, first read or write of
     rcx/ecx/cx/cl
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
import textcache as TC  # noqa: E402

LO, HI = 0x0032E000, 0x0032ED80
PLO, PHI = 0x022C31C0, 0x022C51F0
T = TC.load()
M = [x for x in T if LO <= x[0] < HI and x[2] != "int3"]


def rip_target(a, s, o):
    mm = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", o)
    if not mm:
        return None
    d = int(mm.group(2), 16) * (1 if mm.group(1) == "+" else -1)
    return a + s + d


print("1 rip-relative operands into the pool / list record / gap:")
for i in I.rip_refs(PLO, PHI):
    t = [i.address + i.size + op.mem.disp for _, op in I.mem_ops(i) if op.mem.base == I.X86_REG_RIP][0]
    tag = ""
    if PLO <= t < 0x022C51C0:
        k, r = divmod(t - PLO, 0x80)
        tag = "slot %d +0x%X" % (k, r)
        if r == 0 and i.mnemonic != "lea":
            tag += "  <-- slot +0 accessed directly"
    else:
        tag = "list/gap +0x%X from 022C51C0" % (t - 0x022C51C0)
    print("   %08X %-44s -> %08X  %s" % (i.address, I.txt(i), t, tag))

print("2 rip-relative stores in the module:")
for a, s, m, o, w in M:
    if m.startswith("mov") and o.startswith(("qword ptr [rip", "dword ptr [rip", "byte ptr [rip", "word ptr [rip")):
        t = rip_target(a, s, o)
        print("   %06X %-44s -> %08X %s" % (a, m + " " + o, t, "inside pool/list/gap" if PLO <= t < PHI else "OUTSIDE"))

print("3 external callers of module entries:")
entries = sorted({int(w.split(":")[-1], 16) for a, s, m, o, w in M} | {a for a, s, m, o, w in M
                  if a in (0x0032E020, 0x0032E030, 0x0032E3F0, 0x0032E450, 0x0032E990, 0x0032EA50, 0x0032EAE0,
                           0x0032EC20, 0x0032EC40, 0x0032ECE0, 0x0032ED20, 0x0032ED70)})
for e in entries:
    cs = I.calls_to(e)
    ext = [(s, k) for s, k in cs if not (LO <= s < HI)]
    ab = I.abs64_refs(e, e + 1)
    print("   %08X  sites %d, outside the module %d %s; relocated pointers %s" % (
        e, len(cs), len(ext), [("%08X %s" % x) for x in ext][:8], [("%08X" % a) for a, _ in ab]))

print("4 stale-rcx callees:")
for t in (0x0046DD50, 0x003EADD0, 0x003EB050):
    f = I.func_of(t)
    seq = I.body(f) if f == t else I.dis(t, t + 0x200)
    first = None
    for i in seq:
        if re.search(r"\b(rcx|ecx|cx|cl)\b", i.op_str):
            first = "%08X %s" % (i.address, I.txt(i))
            break
    print("   %08X (.pdata root %s): %d instructions; first rcx use: %s" % (t, "%08X" % f if f else None, len(seq), first))
