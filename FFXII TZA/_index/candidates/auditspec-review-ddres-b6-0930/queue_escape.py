"""queue_escape.py - SWE2-AUDIT-SPEC independent census of where a request-slot pointer can leave the queue module.

Module = 0032E000..0032ED80 (every instruction decoded by textcache.py, .pdata ranges and gap leaves alike). Pool
022C31C0 + 64 x 0x80 (to 022C51C0), then the list record and the gap to 022C51F0.

  P  every reference to 022C31C0..022C51F0 image-wide: rip-relative (decoded), image-base-relative disp32 (decoded
     or straddle), relocated abs64 pointers; owners outside the module listed
  D  every memory operand in the module with displacement 0 (any width, with or without an index register, non-rsp,
     non-rip) - the reader census Z1 restricted to qword / no-index
  X  every direct call / jmp out of the module: target, and for rcx/rdx/r8/r9 the last linear writer before the site
     in the same owner (stop at a call); and whether the target reads that register before writing it in its first
     straight-line block (approximate: linear decode to the first branch/ret)
  R  module functions whose return value (rax at ret) is a slot pointer: the ret sites and rax's last writer
  S  stores of a register into non-stack memory outside the pool in the module (a slot pointer published elsewhere)
Control for D: 0032E153 add [rbx], rax must appear; for X: 0032E0F1 call 0046E030 must appear.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
import textcache as TC  # noqa: E402

LO, HI = 0x0032E000, 0x0032ED80
PLO, PHI = 0x022C31C0, 0x022C51F0
T = TC.load()
M = [x for x in T if LO <= x[0] < HI and x[2] != "int3"]
print("module instructions", len(M))

# ---- P
rr = I.rip_refs(PLO, PHI)
print("P rip-relative operands into the pool/list/gap: %d" % len(rr))
out = [(i.address, I.txt(i)) for i in rr if not (LO <= i.address < HI)]
print("P   outside the module:", [("%08X" % a, t) for a, t in out])
ib = I.ib_refs(PLO, PHI)
print("P image-base-relative disp32 candidates: %d" % len(ib))
for a, i in ib:
    print("P   dword at %08X  decoded-as %s" % (a, ("%08X %s" % (i.address, I.txt(i))) if i else "straddle/none"))
ab = I.abs64_refs(PLO, PHI)
print("P relocated abs64 pointers into the range: %d %s" % (len(ab), [("%08X->%08X" % x) for x in ab]))
# control: the pump's jump table image-base displacement 0x20E2D0 (= 0032E2D0 - IB)
ctl = I.ib_refs(0x0032E2D0, 0x0032E2D1)
print("P control ib_refs(0032E2D0):", [("%08X" % a, I.txt(i) if i else None) for a, i in ctl])

# ---- D
print("D displacement-0 memory operands in the module (any width, any index), excluding rsp/rip bases:")
pat0 = re.compile(r"(byte|word|dword|qword|xmmword) ptr \[(r\w+)( \+ (r\w+)(\*\d)?)?\]")
for a, s, m, o, w in M:
    for mm in pat0.finditer(o):
        base = mm.group(2)
        if base in ("rsp", "rip"):
            continue
        print("D   %06X %-6s %-40s [%s]" % (a, m, o, w))
print("D control 0032E153 present:", any(a == 0x0032E153 for a, *_ in M))

# ---- X
REGS = {"rcx": ("rcx", "ecx", "cx", "cl"), "rdx": ("rdx", "edx", "dx", "dl"), "r8": ("r8", "r8d", "r8w", "r8b"),
        "r9": ("r9", "r9d", "r9w", "r9b")}


def writes(m, o, names):
    if m in ("cmp", "test", "push", "call", "jmp") or m.startswith("j"):
        return False
    first = o.split(",")[0].strip()
    return first in names


def reads_before_write(t):
    """registers of REGS the target reads before writing, in its first straight-line block (approximate)."""
    o = I.off(t)
    seq = list(I.md.disasm(I.raw[o:o + 0x200], t))
    done, used = set(), set()
    for i in seq:
        ops = i.op_str
        parts = [p.strip() for p in ops.split(",")]
        for r, names in REGS.items():
            if r in done or r in used:
                continue
            srcs = parts[1:] if len(parts) > 1 else []
            first = parts[0] if parts else ""
            rd_src = any(re.search(r"\b(%s)\b" % "|".join(names), p) for p in srcs)
            rd_mem = "[" in first and re.search(r"\b(%s)\b" % "|".join(names), first)
            rd_rmw = first in names and i.mnemonic not in ("mov", "movzx", "movsx", "movsxd", "lea", "pop", "xor") and \
                     not (i.mnemonic == "xor" and len(parts) == 2 and parts[0] == parts[1])
            if i.mnemonic in ("cmp", "test") and re.search(r"\b(%s)\b" % "|".join(names), ops):
                rd_src = True
            if rd_src or rd_mem or rd_rmw:
                used.add(r)
            elif first in names:
                done.add(r)
        if i.mnemonic in ("ret", "jmp", "call") or i.mnemonic.startswith("j"):
            break
    return sorted(used)


sites = []
for k, (a, s, m, o, w) in enumerate(M):
    if m not in ("call", "jmp") and not m.startswith("j"):
        continue
    if not o.startswith("0x"):
        continue
    t = int(o, 16)
    if LO <= t < HI:
        continue
    args = {}
    for r, names in REGS.items():
        v = None
        for j in range(k - 1, max(-1, k - 30), -1):
            aa, ss, mm_, oo, ww = M[j]
            if ww != w:
                break
            if mm_ == "call":
                v = "(clobbered by call at %06X)" % aa
                break
            if writes(mm_, oo, names):
                v = "%06X %s %s" % (aa, mm_, oo)
                break
        args[r] = v
    sites.append((a, m, t, w, args))
print("X direct transfers out of the module: %d sites, %d targets" % (len(sites), len({s[2] for s in sites})))
print("X control 0032E0F1 -> 0046E030 present:", any(a == 0x0032E0F1 and t == 0x0046E030 for a, m, t, w, _ in sites))
RBW = {}
for a, m, t, w, args in sites:
    if t not in RBW:
        RBW[t] = reads_before_write(t)
    used = RBW[t]
    print("X %06X %-4s %08X  target reads-before-write %s" % (a, m, t, used))
    for r in used:
        print("X        %-3s <- %s" % (r, args[r]))

# ---- R
print("R ret sites in the module and rax's last linear writer:")
for k, (a, s, m, o, w) in enumerate(M):
    if m != "ret":
        continue
    v = None
    for j in range(k - 1, max(-1, k - 25), -1):
        aa, ss, mm_, oo, ww = M[j]
        if ww != w:
            break
        if mm_ == "call":
            v = "call %s at %06X" % (oo, aa)
            break
        if writes(mm_, oo, ("rax", "eax", "ax", "al")) or (mm_ in ("sete", "setne") and oo == "al"):
            v = "%06X %s %s" % (aa, mm_, oo)
            break
    print("R   %06X [%s] rax <- %s" % (a, w, v))

# ---- S
print("S register stores to non-stack memory in the module (candidate publications):")
for a, s, m, o, w in M:
    if m != "mov":
        continue
    mm = re.match(r"^qword ptr \[(.+)\], (r\w+)$", o)
    if not mm or mm.group(1).startswith("rsp") or mm.group(1).startswith("r11"):
        continue
    print("S   %06X %s   [%s]" % (a, o, w))
