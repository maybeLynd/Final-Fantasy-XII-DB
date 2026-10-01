"""sd163_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the SD-163 review (2026-09-30).

Not the author's checker: ov31_indep.py loader (sha256 asserted), full linear decode of 007A1CD0 (its .pdata extent
[007A1CD0, 007A2134)) with a small register tracker:
  A  every call through [rax/r10 + disp] after a load of the interface [02EA9508]: slot, the r8 / r9 argument
     (rip-loaded qword cells) at the call, and the store that consumes the returned pointer
  B  the digital handle cells used and the analog handle cells used -> are the two sets disjoint, what is each range
  C  the analog x/y offsets and scale constants per store
  D  rip-relative references image-wide to 02EA9508 .. 02EA95A8 (who writes the handle cells / the interface)
  E  007A15A0 linear decode (the per-binding step)
"""
import os, re, struct, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

ins = T.dis(0x007A1CD0, 0x007A2134)
assert ins[-1].address == 0x007A2133 and ins[-1].mnemonic == "ret"


def ripcell(i):
    for m, sz in T.mem_ops(i):
        if m.base == T.X86_REG_RIP:
            return i.address + i.size + m.disp
    return None


def f32(va):
    return struct.unpack("<f", T.rd(va, 4))[0]


regs = {}          # reg name -> rip cell it was loaded from
calls = []
pending = None
for i in ins:
    op = i.op_str
    m = re.match(r"(r\d+|r[a-z]{2})d?, qword ptr \[rip \+ 0x[0-9a-f]+\]$", op)
    if i.mnemonic == "mov" and m:
        regs[op.split(",")[0]] = ripcell(i)
    cm = re.match(r"qword ptr \[(rax|r10) \+ (0x[0-9a-f]+)\]$", op)
    if i.mnemonic == "call" and cm:
        pending = dict(site=i.address, slot=int(cm.group(2), 16), r8=regs.get("r8"), r9=regs.get("r9"), use=[])
        calls.append(pending)
        continue
    if pending is not None and len(pending["use"]) < 4 and ("[rax" in op) and i.mnemonic in ("movzx", "movss"):
        pending["use"].append("%08X %s %s" % (i.address, i.mnemonic, op))
    sm = re.match(r"(byte|dword) ptr \[rbx \+ (0x[0-9a-f]+)\], (cl|eax)$", op)
    if pending is not None and i.mnemonic == "mov" and sm:
        pending["store"] = "%s +%s" % (sm.group(1), sm.group(2))
    if i.mnemonic == "mulss":
        pending["scale"] = f32(ripcell(i))

print("A  vtable calls in 007A1CD0 (slot disp, r8 cell, r9 cell -> use -> store):")
cnt = collections.Counter()
for c in calls:
    cnt[c["slot"]] += 1
    print("   %08X  +0x%02X  r8=%s r9=%s  use=%s  store=%s  scale=%s" % (
        c["site"], c["slot"], "%08X" % c["r8"] if c["r8"] else "-", "%08X" % c["r9"] if c["r9"] else "-",
        c["use"][:1], c.get("store", "-"), c.get("scale", "-")))
print("   slot counts: %s" % ", ".join("+0x%02X x%d" % (k, v) for k, v in sorted(cnt.items())))

dig = [c["r9"] for c in calls if c["slot"] == 0x48]
ana = [c["r9"] for c in calls if c["slot"] == 0x60]
print("B  digital handle cells: %d calls, %d distinct, min %08X max %08X, contiguous qwords: %s" % (
    len(dig), len(set(dig)), min(dig), max(dig), sorted(set(dig)) == list(range(min(dig), max(dig) + 8, 8))))
print("   analog handle cells: %s ; overlap with digital: %s" % (sorted("%08X" % a for a in set(ana)), sorted(set(dig) & set(ana))))
print("   controller handle (r8) in every +0x48/+0x60 call: %s" % sorted(set("%08X" % c["r8"] for c in calls if c["slot"] in (0x48, 0x60))))

print("D  rip references to 02EA9500..02EA95B0 image-wide (writes marked W):")
for a, mn, op, sz in T.rip_refs(0x02EA9500, 0x02EA95B0):
    w = "W" if (mn.startswith("mov") and op.split(",")[0].strip().startswith(("qword ptr [rip", "dword ptr [rip", "byte ptr [rip"))) else " "
    print("   %s %08X  %s %s" % (w, a, mn, op))

print("E  007A15A0:")
for i in T.dis(0x007A15A0, 0x007A1640):
    print("   %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    if i.mnemonic == "ret":
        break
